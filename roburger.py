import re
from robobrowser import RoboBrowser
from requests_toolbelt import SSLAdapter
from collections import defaultdict
import config


def max_radio_map(brow):
    radio_map = defaultdict(list)
    for k in brow.find_all('input'):

        in_name = k.get('name', None)
        in_type = k.get('type', None)

        if in_type == 'radio' and in_name:
            radio_map[k['name']].append(k['value'])

    return radio_map


# Browse url :
browser = RoboBrowser()
browser.session.headers = config.headers

# Hacky: Force SSLv3 -- Must get adequates libs
adapter = SSLAdapter('SSLv3')
browser.session.mount('https://', adapter)

# Get to website
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

# Let's fill in the proper questionnaire !
import ipdb; ipdb.set_trace() # BREAKPOINT
inputs_map = max_radio_map(browser)

import ipdb; ipdb.set_trace() # BREAKPOINT

for i in form.keys():
    if form[i] == '':
        form[i].value = ''
