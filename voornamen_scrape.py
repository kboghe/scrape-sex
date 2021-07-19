#import packages
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

#retrieve set of user agents
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

#headertje maken
def set_headers(user_agent_rotator):
    useragent_pick = user_agent_rotator.get_random_user_agent()
    headers = {'User-Agent': useragent_pick,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
    return headers

#scrape functie
def get_sex(x):
    for i in range(10):
        try:
            url_bank = 'https://www.meertens.knaw.nl/nvb/naam/is/'+x.Voornaam
            openpage = requests.get(url=url_bank, headers=headers)
        except:
            headers = set_headers(user_agent_rotator)
            time.sleep(3)
            continue
        else:
            break
    else:
        raise Exception('Sorry, something went wrong while connecting...')

    try:
        name_table = pd.read_html(openpage.text)[0].replace('--',0)
        if int(name_table[2][1]) > int(name_table[2][5]):
            sex = 'M'
        else:
            sex = 'V'
    except:
        sex = 'onbekend'
    time.sleep(random.uniform(3,6))
    return pd.Series([sex])

#maak df aan met enkele voornamen
gender_names = pd.DataFrame({'Voornaam':['Jozef','Maria']})

#zoek geslacht op adhv voornaam
gender_names['sex'] = gender_names.apply(get_sex,axis=1)   

gender_names.head()
