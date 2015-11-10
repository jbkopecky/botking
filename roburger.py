import random
import ssl
from collections import defaultdict

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
class HTTPSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


class BKBrowser(object):
    def __init__(self):
        # Browse url :
        self.browser = RoboBrowser(parser="html.parser")
        self.browser.session.headers = config.headers
        # Mount with custom SSL Adapter
        self.browser.session.mount('https://', HTTPSAdapter())

    def _connect(self):
        # Get to website
        print("- Connecting to url ...")
        self.browser.open(config.url)

    def _skip_first_page(self):
        button = self.browser.get_forms()[0]
        self.browser.submit_form(button)

    # Let's fill in the proper form !
    def _fill_form(self):
        while not self.browser.find('p', {'class': 'ValCode'}):
            inputs_map = max_radio_map(self.browser)
            f = self.browser.get_forms()[0]
            for i in f.keys():
                if f[i].value == '':
                    answers_list = inputs_map.get(i, ['1'])
                    f[i].value = random.choice(answers_list)
            f.serialize()
            self.browser.submit_form(f)

    def _fill_date_form(self):
        # Fill in Date/Time form and start the Questionnaire
        print("- Filling Forms Randomly ...")
        form = self.browser.get_forms()[0]
        form['JavaScriptEnabled'].value = '1'
        form['SurveyCode'].value = config.ID
        form['InputMonth'].value = config.date[0]
        form['InputDay'].value = config.date[1]
        form['InputHour'].value = config.time[0]
        form['InputMinute'].value = config.time[1]
        form.serialize()
        self.browser.submit_form(form)

    def get_validation_code(self):
        self._connect()
        self._skip_first_page()
        self._fill_date_form()
        self._fill_form()
        return self.browser.find('p', {'class': 'ValCode'}).text


def main():
    browser = BKBrowser()
    print("- " + browser.get_validation_code())
    print("- Bon appetit !")


if __name__ == '__main__':
    main()
