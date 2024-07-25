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

console = Console()
proxproc = None

def safeload():
    try:
        return config.load()
    except FileNotFoundError:
        return None

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
    
    if not noproxy and cfg and 'proxy' in cfg:
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
@click.option('--cc', default=1, help='Country code')
@click.option('--phone', help='Phone number')
def lookup(cc, phone):
    with Progress() as progress:
        task = progress.add_task("[cyan]Looking up...", total=100)
        result = lkp(cc=cc, phone=phone)
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
    
    def asemail(to, message, from_, port):
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = 'Message'
        msg['From'] = from_
        msg['To'] = lkp(to)['gateways']['SMS']
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

    asemail(to, message, from_, port)

if __name__ == "__main__":
    cli()