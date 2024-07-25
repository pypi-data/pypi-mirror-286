import subprocess as sp
import os
from rich.console import Console
console = Console()

def prx(host:str='0.0.0.0', port:int=8899, printout=False):
    '''Start a proxy server'''
    stdout = sp.PIPE if printout else sp.DEVNULL
    sp.Popen(['proxy', '--hostname', host, '--port', str(port)], shell=True, stdout=stdout, stderr=sp.PIPE)
    os.environ['sssmsproxy'] = f'{host}:{port}' if host != '0.0.0.0' else f'localhost:{port}'
    console.print(f'Proxy Running | Addresses: {host} | Port: {port}', style='bold green')

if __name__ == '__main__':
    prx()