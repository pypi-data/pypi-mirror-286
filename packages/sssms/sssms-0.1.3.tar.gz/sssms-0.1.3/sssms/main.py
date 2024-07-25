'''self-service SMS via email'''

from lookup import lookup as lkp, cache
from prx import prx
import config
from sssmtp import SMTP
import os
import smtplib
from email.message import EmailMessage
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
import click

console = Console()

# Load configuration
try:
    cfg = config.load()
except FileNotFoundError:
    console.print("Config file not found. Creating a new one...", style="yellow")
    config.create()
    cfg = config.load()

# Apply cache decorator if enabled
if cfg['cache']['lookups']:
    lkp = cache(cfg['cache']['path'])(lkp)

@click.group()
@click.option('--noproxy', is_flag=True, default=False, help='Disable proxy')
def cli(noproxy):
    if not noproxy:
        proxy(cfg['proxy']['host'], cfg['proxy']['port'])

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

@cli.command()
@click.option('--host', default=None, help='Host to run proxy on')
@click.option('--port', default=None, help='Port to run proxy on')
def proxy(host, port):
    host = host or cfg['proxy']['host']
    port = port or cfg['proxy']['port']
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Starting proxy...", total=100)
            prx(host, port)
            progress.update(task, advance=100)
        console.print(Panel(f"Proxy running on {host}:{port}", title="Proxy Status", border_style="green"))
    except Exception as e:
        console.print(Panel(f"Failed to start proxy: {e}", title="Error", border_style="red"))

if __name__ == "__main__":
    cli()