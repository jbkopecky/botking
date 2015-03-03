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

browser.open(config.url)

# Click on first button to go to second page:
button = browser.get_forms()[0]
browser.submit_form(button)


