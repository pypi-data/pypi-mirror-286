import subprocess as sp
import atexit
import signal
import os
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
console = Console()

class prx:
    proc = None
    proxy = None
    @classmethod
    def start(cls, host, port):
        try:
            with Progress() as progress:
                task = progress.add_task("[cyan]Starting proxy...", total=100)
                cls.proc = sp.Popen(['proxy', '--hostname', host, '--port', str(port)])
                progress.update(task, advance=100)
            console.print(Panel(f"Proxy running on {host}:{port}", title="Proxy Status", border_style="green"))
            cls.proxy = f'{host}:{port}' if host != '0.0.0.0' else f'localhost:{port}'
        except Exception as e:
            console.print(Panel(f"Failed to start proxy: {e}", title="Error", border_style="red"))
    @classmethod
    def kill(cls):
        if cls.proc is not None:
            console.print("Stopping proxy...", style="yellow")
            cls.proc.terminate()
            cls.proc.wait()
            sp.Popen(['lsof -ti :8899 | xargs kill -9'])
            console.print("Proxy stopped.", style="green")

# Register the prx.kill function to be called at exit
atexit.register(prx.kill)

# Also handle SIGTERM
signal.signal(signal.SIGTERM, lambda signum, frame: prx.kill())

if __name__ == '__main__':
    prx.start('0.0.0.0', 8899)
