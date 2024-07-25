import yaml
import os
import platform
import subprocess
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import secrets
from pathlib import Path
import ast
from sssmtp import SMTP

def __key__():
    '''Generate or load encryption key for config file'''
    def __sysconf__():
        return ast.literal_eval(f"__import__('pathlib').Path.home() / '.{['bash', 'zsh'][platform.system() != 'Windows' and 'zsh' in os.environ.get('SHELL', '')]}rc'")
    def __reload__():
        os.system(f"{'source' if platform.system() != 'Windows' else 'call'} {__sysconf__()}")
    PREFIX, keyvar, saltvar = 'SSSMS', f'{PREFIX}secret', f'{PREFIX}salt'
    derivative = lambda p, s: base64.urlsafe_b64encode(PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=s, iterations=100000).derive(p.encode()))
    if keyvar not in os.environ or saltvar not in os.environ:
        key = derivative(input("Enter a secret key for config encryption: "), secrets.token_bytes(16))
        os.environ[keyvar], os.environ[saltvar] = key.decode(), base64.b64encode(secrets.token_bytes(16)).decode()
        with open(__sysconf__(), 'a') as f: f.write(f'\nexport {keyvar}="{os.environ[keyvar]}"\nexport {saltvar}="{os.environ[saltvar]}"')
        __reload__()
    return os.environ[keyvar].encode()

def load(path:str=None):
    '''Load configuration from file'''
    if not path:path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.exists(path):
        with open(path, 'r') as f:content = yaml.safe_load(f)
        if 'credentials' in content and 'password' in content['credentials']:content['credentials']['password'] = Fernet(__key__()).decrypt(content['credentials']['password'].encode()).decode()
        return content
    raise FileNotFoundError('Config file not found')

def create(prxhost:str='0.0.0.0', prxport:int=8899, email:str=None, password:str=None, cachelookups:bool=True, cachepath:str=None, server:str=None):
    '''Create a new configuration file'''
    path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not cachepath:cachepath=os.path.join(os.path.dirname(__file__), 'lookupcache.json')
    if not os.path.exists(path):
        if not email:email = input('Please provide the default email to send from: ')
        if not password:password = input('Please provide the default email password: ')        
        if not server:server = SMTP()(email)
        __key__()
        content = {
            'proxy': {
                'host': prxhost,
                'port': prxport
            },
            'credentials': {
                'email': email,
                'password': Fernet(__key__()).encrypt(password.encode()).decode()
            }, 
            'cache': {
                'lookups': cachelookups,
                'path': cachepath
            }, 
            'smtp': {
                'server': server
            }
        }
        with open(path, 'w') as f:
            yaml.dump(content, f)
        print(f"Config file created at {path}")
    else:
        print("Config file already exists. Use 'load()' to read it or delete the existing file to create a new one.")

if __name__ == "__main__":
    create()