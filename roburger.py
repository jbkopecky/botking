import re
from robobrowser import RoboBrowser
from requests_toolbelt import SSLAdapter
import config


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

for i in form.keys():
    if form[i] == '':
        form[i].value = ''
