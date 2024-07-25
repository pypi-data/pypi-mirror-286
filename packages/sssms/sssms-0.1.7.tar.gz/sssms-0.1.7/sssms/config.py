import yaml
import os
import platform
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import secrets
from pathlib import Path
from .sssmtp import SMTP
import sys

def __key__(secret_key):
    '''Generate encryption key for config file'''
    salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode()))
    return key, base64.b64encode(salt).decode()

def __sysconf__():
    home = Path.home()
    if platform.system() == 'Windows':
        return home / '.bashrc'
    elif 'zsh' in os.environ.get('SHELL', ''):
        return home / '.zshrc'
    else:
        return home / '.bashrc'

def load(path:str=None):
    '''Load configuration from file'''
    if not path:
        path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = yaml.safe_load(f)
        if 'credentials' in content and 'password' in content['credentials']:
            key = base64.urlsafe_b64decode(content['encryption']['key'])
            content['credentials']['password'] = Fernet(key).decrypt(content['credentials']['password'].encode()).decode()
        return content
    raise FileNotFoundError('Config file not found')

def create(prxhost:str='0.0.0.0', prxport:int=8899, email:str=None, password:str=None, cachelookups:bool=True, cachepath:str=None, server:str=None, secret_key:str=None):
    '''Create a new configuration file'''
    path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not cachepath:
        cachepath = os.path.join(os.path.dirname(__file__), 'lookupcache.json')
    if not os.path.exists(path):
        smtp = SMTP()
        if not email or not password or not secret_key:
            raise ValueError("Email, password, and secret key are required")
        if not server:
            try:
                server = smtp(email)
            except ValueError:
                print("Couldn't automatically determine your email provider.")
                print("Supported providers:", ", ".join(smtp.__providers__()))
                provider = input('Please clarify your email provider from the list above, or enter a new SMTP server: ')
                if provider not in smtp.__providers__():
                    smtp.__addnew__(provider, input('Please provide the domain(s) associated with this provider: '))
                if '@' in provider:
                    provider = provider.split('@')[-1].split('.')[0].lower()
                else:
                    try:
                        server = smtp(f'user@{provider}.com')
                    except ValueError:
                        print("Invalid provider. Please try again with a different provider.")
                        sys.exit(1)
        
        key, salt = __key__(secret_key)
        content = {
            'proxy': {
                'host': prxhost,
                'port': prxport
            },
            'credentials': {
                'email': email,
                'password': Fernet(key).encrypt(password.encode()).decode()
            }, 
            'cache': {
                'lookups': cachelookups,
                'path': cachepath
            }, 
            'smtp': {
                'server': server,
                'providers': smtp.common
            },
            'encryption': {
                'key': key.decode(),
                'salt': salt
            }
        }
        with open(path, 'w') as f:
            yaml.dump(content, f)
        print(f"Config file created at {path}")
    else:
        print("Config file already exists. Use 'load()' to read it or delete the existing file to create a new one.")

if __name__ == "__main__":
    create()