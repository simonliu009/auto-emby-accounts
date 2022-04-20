import json
import logging as log
from logging.handlers import RotatingFileHandler
import random
import string
import sys
from datetime import datetime
from os import mkdir, path

import requests

log_level = 3
timeout = 10

# When set true, if the script finds a user that already exists,
# the script will attempt to change the policy of that user,
# and add the emby connect account to that user.
overwrite = False

# The url to your Emby server
emby_base_url = 'https://pornemby.club:443'

# Login info for an account on your Emby server that has admin privileges
# Username
emby_uname = 'SimonLiu009'
# Password
emby_passwd = 'Act8935PornEmby'

switcher = {
    4: log.DEBUG,
    3: log.INFO,
    2: log.WARNING,
    1: log.ERROR,
    0: log.CRITICAL
}

# dir = path.split(path.abspath(__file__))
dir = path.dirname(path.realpath(__file__)) 
# dir = dir[0]
log_path = f'./logs'
if not path.exists(log_path):
    mkdir(log_path)

#log setup
logfile =f'{log_path}/{path.basename(path.splitext(__file__)[0])}.log'
print('logfile:',logfile)

log.basicConfig(
    filename=logfile,
    level=switcher.get(log_level, log.DEBUG),
    datefmt="%Y-%m-%d %H:%M:%S",
    # format='%(asctime)s - %(levelname)s - %(message)s'
    format = "[%(asctime)-15s %(filename)s:%(lineno)d %(funcName)s] %(message)s"
    )
# cons = log.StreamHandler()
log = log.getLogger('mylog')
handler = RotatingFileHandler(logfile,"a",4096, 2, "utf-8")
# fmt = log.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
# handler.setFormatter(fmt)
# log.addHandler(handler)
handler.setLevel(switcher.get(log_level))

log.addHandler(handler)
# log.debug('Started script!')


# out_file = f'{dir}/out.' + 'tsv' if tsv_out else 'txt'

def user_login():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        'X-Emby-Client': "Requests Python",
        'X-Emby-Device-Name': "Python",
        "X-Emby-Client-Version": "4.4.2.0",
        "X-Emby-Device-Id": "12345678-1234-1234-1234-123456789012"
    }

    # Authenticate info

    raw_data = {
        'username': emby_uname,
        'Pw': emby_passwd
    }

    try:
        res = requests.post(f'{emby_base_url}/Users/AuthenticateByName', params=raw_data, headers=headers, timeout=timeout)
    except requests.exceptions.ConnectionError:
        log.error(f'Cannot establish connection to emby_base_url! Stopping... emby_base_url={base_url}')
        sys.exit(1)

    try:
        data = json.loads(res.text)
        headers.update({
            'X-Emby-Token': data['AccessToken']
            })
        log.info('Successfully authenticated as username:%s'%emby_uname)
    except json.decoder.JSONDecodeError:
        if 'Invalid username' in res.text:
            log.error('Username or password is incorrect! Stopping...')
        else:
            log.error('Error occurred authenticating. Stopping...')
            log.error(f'{res.status_code} - {res.text}')
        sys.exit(1)


    
        

if __name__ == '__main__':
    
    user_login()
