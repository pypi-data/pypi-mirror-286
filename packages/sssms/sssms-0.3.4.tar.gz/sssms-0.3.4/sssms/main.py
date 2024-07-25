import os
import atexit
import signal
import subprocess
from .lookup import lookup as lkp, cache
from .prx import prx
from . import config
from .sssmtp import SMTP
import smtplib
from email.message import EmailMessage
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
import click
import getpass
from functools import reduce, partial
from typing import Callable, Dict, Any
import yaml
from operator import itemgetter

console = Console()

def safeload():
    try:
        return config.load()
    except FileNotFoundError:
        return None

def compose(*functions: Callable) -> Callable:
    return reduce(lambda f, g: lambda x: f(g(x)), functions)

def updatenest(d: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
    *path, last = key.split('.')
    return reduce(lambda acc, k: {**acc, k: {**acc.get(k, {}), last: value} if k == path[-1] else acc.get(k, {})}, path, d)

'''def maskinfo(cfg: Dict[str, Any]) -> Dict[str, Any]:
    return {k: {sk: '******' if sk in {'password', 'key'} else sv for sk, sv in v.items()} if isinstance(v, dict) else v for k, v in cfg.items()}'''

cfg = safeload()

# Apply cache decorator if enabled
if cfg and cfg.get('cache', {}).get('lookups'):
    lkp = cache(cfg['cache']['path'])(lkp)

# Register the prx.kill function to be called at exit
atexit.register(prx.kill)

# Also handle SIGTERM
signal.signal(signal.SIGTERM, lambda signum, frame: prx.kill())

@click.group()
@click.option('--noproxy', is_flag=True, default=False, help='Disable proxy')
@click.pass_context
def cli(ctx, noproxy):
    ctx.ensure_object(dict)
    ctx.obj['noproxy'] = noproxy
    
    if cfg is None and ctx.invoked_subcommand != 'init':
        console.print("Config file not found. Run 'sssms init' to create one.", style="yellow")
        ctx.exit()
    
    if not noproxy and cfg and 'proxy' in cfg and ctx.invoked_subcommand not in ['init', 'conf']:
        prx.start(cfg['proxy']['host'], cfg['proxy']['port'])

@cli.command()
@click.option('--cachelookups', is_flag=True, help='Enable lookup caching')
@click.option('--cachepath', help='Path to lookup cache file')
@click.option('--server', help='SMTP server')
@click.option('--secret', help='Secret key for config encryption')
@click.option('--showpass', is_flag=True, help='Show password as it is typed')
def init(cachelookups=False, cachepath=None, server=None, secret=None, showpass=False):
    """Initialize the configuration file"""
    if cfg:
        console.print("Config file already exists. Use 'load()' to read it or delete the existing file to create a new one.", style="yellow")
        return

    email = input('Please provide the default email to send from: ')
    if showpass:
        password = input('Please provide the default email password: ')
        if not secret:
            secret = input('Enter a secret key for config encryption: ')
    else:
        password = getpass.getpass('Please provide the default email password: ')
        if not secret:
            secret = getpass.getpass('Enter a secret key for config encryption: ')

    try:
        config.create(email=email, password=password, secret_key=secret, cachelookups=cachelookups, cachepath=cachepath, server=server)
        console.print("Config file created successfully.", style="green")
    except Exception as e:
        console.print(f"Failed to create config file: {str(e)}", style="red")

@cli.command()
@click.option('--delete', is_flag=True, help='Delete the configuration file')
@click.option('--show', is_flag=True, help='Show the configuration')
@click.option('--path', is_flag=True, help='Show the path to the configuration file')
@click.option('--email', help='Change email address')
@click.option('--password', help='Change email password')
@click.option('--secret', help='Change secret key')
@click.option('--cachelookups', type=bool, help='Enable/disable lookup caching')
@click.option('--cachepath', help='Path to lookup cache file')
@click.option('--server', help='SMTP server')
def conf(**kwargs):
    """Manage configuration with style and sophistication"""
    if kwargs['delete']:
        config.delete()
        console.print("Configuration file deleted successfully.", style="green")
        return

    if kwargs['path']:
        console.print(f"Configuration file path: {config.__showpath__()}", style="cyan")
        return

    if kwargs['show']:
        try:
            cfg = config.load()
            console.print(Panel(yaml.dump(cfg), title="Current Configuration", expand=False))
        except FileNotFoundError:
            console.print("No configuration file found.", style="yellow")
        return

    updates = {}
    for key in ['email', 'password', 'secret', 'cachelookups', 'cachepath', 'server']:
        if kwargs[key] is not None:
            updates[key] = kwargs[key]

    if updates:
        try:
            config.update(**updates)
            console.print("Configuration updated successfully.", style="green")
        except Exception as e:
            console.print(f"Failed to update configuration: {str(e)}", style="red")
    else:
        console.print("No updates specified. Use --help to see available options.", style="yellow")

@cli.command()
@click.option('--cc', default=1, help='Country code')
@click.option('--phone', help='Phone number')
def lookup(cc, phone):
    if cfg['proxy']:
        proxy = f"{cfg['proxy']['host']}:{cfg['proxy']['port']}"
    with Progress() as progress:
        task = progress.add_task("[cyan]Looking up...", total=100)
        result = lkp(cc=cc, phone=phone, proxy=proxy)
        progress.update(task, advance=100)
    console.print(Panel.fit(str(result), title="Lookup Result", border_style="green"))

@cli.command()
@click.argument('message')
@click.option('--cc', default=1, help='Country code')
@click.option('--to', help='Phone number to send message to')
@click.option('--from', 'from_', default=None, help='Email to send message from')
@click.option('--port', default=587, help='SMTP port')
def send(message, cc, to, from_, port):
    if not from_:
        from_ = cfg['credentials']['email']
    
    def asemail(cc, to, message, from_, port):
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = 'Message'
        msg['From'] = from_
        msg['To'] = lkp(cc=cc, phone=to)['gateways']['SMS']
        server = cfg.get('smtp', {}).get('server') if cfg.get('smtp') else SMTP()(from_)
        try:
            with Progress() as progress:
                task = progress.add_task("[cyan]Sending email...", total=100)
                with smtplib.SMTP(server, port) as server:
                    server.starttls()
                    server.login(from_, cfg['credentials']['password'])
                    progress.update(task, advance=50)
                    server.send_message(msg)
                    progress.update(task, advance=50)
            console.print(Panel("Message sent successfully", title="Success", border_style="green"))
        except Exception as e:
            console.print(Panel(f"Failed to send message: {e}", title="Error", border_style="red"))

    asemail(cc, to, message, from_, port)

if __name__ == "__main__":
    cli()