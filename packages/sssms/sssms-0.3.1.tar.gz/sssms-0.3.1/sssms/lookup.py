import requests 
from typing import List, Dict
import json
from bs4 import BeautifulSoup
import os
from functools import wraps
from .prx import prx
cookies = {
    'PHPSESSID': 'jm5prvd8ct4iqk7np61mi6pfku',
    '__cf_bm': 'n0g5zqggjWOeyTJzbTzI4ztUZMvJGOjrOePo0qHtupw-1721829708-1.0.1.1-OH.ZB6f1NUaEMAK8Pa0F5dEVjSFMIq8RR3yuDw81DV_sD2lpar_QSwBO74WfBCvykCncfcPZYllg0Qm_.t7uKw',
    'cf_clearance': '7__XQGNPkr3zyafKYLeUKsjC6LQ_bCli28mLvjW2aAA-1721827259-1.0.1.1-KbH.H8Nmkjy0iiXw0AJgZ3fs9ZxHzbXqiSTxqzYYB3WRvrGvn9SeOvQmgkpbsgQJBQ4I0Cpv3CxTutCuo5Nf0A',
    '_ga': 'GA1.2.16528444.1721827261',
    '_gid': 'GA1.2.738335994.1721827262',
    '_gat': '1',
    '__gads': 'ID=652a96df5f1fc503:T=1721827261:RT=1721827261:S=ALNI_Mbjj-prHW9lBxlHvuV5f_sX6Er4pQ',
    '__gpi': 'UID=00000a48e4d9731d:T=1721827261:RT=1721827261:S=ALNI_MY3TK6MsJmfCuivExvJ7pF0Dwdmyg',
    '__eoi': 'ID=449bbecfed5f1702:T=1721827261:RT=1721827261:S=AA-AfjbmPCDQWO2MQRm_ZfO_39R5',
    '_ga_4JSC4GJHB3': 'GS1.2.1721827263.1.0.1721827263.0.0.0',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://freecarrierlookup.com',
    'Connection': 'keep-alive',
    'Referer': 'https://freecarrierlookup.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
}
def lookup(cc:int=1, phone:int=None, cookies:Dict=cookies, headers:Dict=headers) -> Dict:
    '''Lookup carrier information for a phone number'''
    proxy = os.environ.get('sssmsproxy')
    proxies = {
        'http': proxy,
        'https': proxy
    } if proxy is not None else None
    def parse(html):
        soup = BeautifulSoup(html, 'html.parser')
        return {
                    **{key: soup.find('strong', string=f'{key}:').find_next('p').text for key in ['Phone Number', 'Carrier', 'Is Wireless']},
                    'gateways': {
                        'SMS': soup.find('strong', string='SMS Gateway Address:').find_next('p').text,
                        'MMS': soup.find('strong', string='MMS Gateway Address:').find_next('p').text
                    }
                }
    data = {
                'test': '456Tabo', 
                'sessionlogin': '1', 
                'cc': str(cc),
                'phonenum': str(phone)
            }
    try: 
        response = requests.post('https://freecarrierlookup.com/getcarrier_free.php', headers=headers, cookies=cookies, data=data, proxies=proxies) if proxies is not None else requests.post('https://freecarrierlookup.com/getcarrier_free.php', headers=headers, cookies=cookies, data=data)
        if response.status_code == 200:return parse(response.json()['html'])
        else:raise Exception(f"Failed to retrieve carrier information: {response.text}")
    except Exception as e:
        print(response.text)
        raise e


def cache(cachepath:str=os.path.join(os.path.dirname(__file__), 'lookupcache.json')):
    '''Cache lookup results'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not os.path.exists(cachepath):open(cachepath, 'w').write('{}')
            with open(cachepath, 'r') as f:
                cache = json.load(f)
            if kwargs['phone'] in cache: return cache[kwargs['phone']]
            result = func(*args, **kwargs)
            cache[kwargs['phone']] = result
            with open(cachepath, 'w') as f:
                json.dump(cache, f)
            return result
        return wrapper
    return decorator

