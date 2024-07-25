class SMTP:
    '''SMTP server lookup based on email provider'''
    common = {
        'gmail.com': 'smtp.gmail.com',
        'yahoo.com': 'smtp.mail.yahoo.com',
        'outlook.com': 'smtp-mail.outlook.com',
        'hotmail.com': 'smtp-mail.outlook.com',
        'aol.com': 'smtp.aol.com',
        'icloud.com': 'smtp.mail.me.com',
        'protonmail.com': 'smtp.protonmail.com',
        'zoho.com': 'smtp.zoho.com',
        'yandex.com': 'smtp.yandex.com',
        'gmx.com': 'smtp.gmx.com',
        'mail.com': 'smtp.mail.com',
    }
    def __call__(self, email:str) -> str:
        if email.split('@')[-1] in self.common:return self.common[email.split('@')[-1]]
        raise ValueError('Unsupported email provider')