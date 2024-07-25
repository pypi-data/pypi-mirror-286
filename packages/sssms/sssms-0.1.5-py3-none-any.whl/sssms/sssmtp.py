import yaml
import os

class SMTP:
    '''SMTP server lookup based on email provider'''
    def __init__(self):
        self.config = os.path.join(os.path.dirname(__file__), 'config.yaml')
        self.common = {
                'smtp.gmail.com': ['gmail', 'googlemail'],
                'smtp.mail.yahoo.com': ['yahoo', 'ymail', 'rocketmail'],
                'smtp-mail.outlook.com': ['outlook', 'hotmail', 'live', 'msn'],
                'smtp.aol.com': ['aol', 'aim'],
                'smtp.mail.me.com': ['icloud', 'me', 'mac'],
                'smtp.protonmail.com': ['protonmail', 'pm'],
                'smtp.zoho.com': ['zoho'],
                'smtp.yandex.com': ['yandex'],
                'smtp.gmx.com': ['gmx'],
                'smtp.mail.com': ['mail'],
            }
        self.__config__()

    def __config__(self):
        if os.path.exists(self.config):
            with open(self.config, 'r') as f:
                config = yaml.safe_load(f)
            self.common.update(config.get('smtp', {}).get('providers', {})) if config.get('smtp') else None


    def __save__(self):
        with open(self.config, 'r') as f:
            config = yaml.safe_load(f)
        if 'smtp' not in config:
            config['smtp'] = {}
        config['smtp']['providers'] = self.common
        with open(self.config, 'w') as f:
            yaml.dump(config, f)

    def __addnew__(self, server, domains):
        if isinstance(domains, str):
            domains = [domains]
        if server in self.common:
            self.common[server].extend(domains)
            self.common[server] = list(set(self.common[server]))  
        else:
            self.common[server] = domains
        self.__save__()

    def __remove__(self, server):
        if server in self.common:
            del self.common[server]
            self.__save__()

    def __call__(self, email: str) -> str:
        domain = email.split('@')[-1].split('.')[0].lower()
        for server, domains in self.common.items():
            if domain in domains:
                return server
        raise ValueError('Unsupported email provider')

    def __providers__(self):
        return list(set([domain for domains in self.common.values() for domain in domains]))