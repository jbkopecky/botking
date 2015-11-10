from collections import defaultdict
import random
import time
import ssl

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from robobrowser import RoboBrowser

import config

def max_radio_map(brow):
    radio_map = defaultdict(list)
    for k in brow.find_all('input'):

        in_name = k.get('name', None)
        in_type = k.get('type', None)

        if in_type == 'radio' and in_name:
            radio_map[k['name']].append(k['value'])

    return radio_map

# Custom SSL Adapter, see:
# https://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/   
class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager( num_pools=connections,
                                        maxsize=maxsize,
                                        block=block,
                                        ssl_version=ssl.PROTOCOL_TLSv1)

# Browse url :
browser = RoboBrowser(parser="lxml")
browser.session.headers = config.headers

# Mount with custom SSL Adapter
browser.session.mount('https://', MyAdapter())

# Get to website
print "- Connecting to url ..."
browser.open(config.url)

# Click on first button to go to second page:
button = browser.get_forms()[0]
browser.submit_form(button)

# Fill in Date/Time form and start the Questionnaire
form = browser.get_forms()[0]
form['JavaScriptEnabled'].value = '1'
form['SurveyCode'].value = config.ID
form['InputMonth'].value = config.date[0]
form['InputDay'].value = config.date[1]
form['InputHour'].value = config.time[0]
form['InputMinute'].value = config.time[1]

form.serialize()
browser.submit_form(form)

print "- Filling Forms Randomly ..."
# Let's fill in the proper questionnaire !
while not browser.find('p', {'class': 'ValCode'}):
    inputs_map = max_radio_map(browser)
    f = browser.get_forms()[0]
    for i in f.keys():
        if f[i].value == '':
            answers_list = inputs_map.get(i, ['1'])
            f[i].value = random.choice(answers_list)
    f.serialize()
    browser.submit_form(f)

print "- " + browser.find('p', {'class': 'ValCode'}).text
print "- Bon appetit !"
