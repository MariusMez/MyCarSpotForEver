import argparse
import logging
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

"""
@author:     Marius Mézerette
@copyright:  2018 Marius Mézerette
@license:    BSD
@contact:    marius.mez@gmail.com
@deffield    updated: 24-09-2018
"""

__all__ = []
__version__ = 0.1
__date__ = '24-09-2018'
__updated__ = '24-09-2018'

program_name = os.path.basename(sys.argv[0])
program_version = "v%s" % __version__
program_build_date = str(__updated__)
program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
program_shortdesc = 'RPA for MyCarSpot: votre place de parking a vous pour toujours !'
program_license = '''{}

Created by Marius Mezerette on {}.
Copyright 2018 Marius Mezerette . All rights reserved.

Licensed under the BSD.

Distributed on an "AS IS" basis without warranties
or conditions of any kind, either express or implied.

USAGE
'''.format(program_shortdesc, str(__date__))


URL_MYCARSPOT_LOGIN = 'https://mycarspot.fr/docapostsophia/Login'
CHROMEDRIVER_DEFAULT_PATH = './chromedriver'
GECKODRIVER_DEFAULT_PATH = './geckodriver'
WINDOW_SIZE = (1280, 1024)
WAITING_MAX_TIME = 20
SLEEP_TIME = 3


class SeleniumProcessor(object):

    def __init__(self, driver='chrome', driver_executable_path=CHROMEDRIVER_DEFAULT_PATH, headless=True):
        if driver == 'firefox':
            self.driver = webdriver.Firefox(executable_path=driver_executable_path)
        elif driver == 'chrome':
            chrome_options = Options()
            if headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(
                executable_path=driver_executable_path,
                options=chrome_options
            )

        width, height = WINDOW_SIZE
        self.driver.set_window_size(width, height)
        self.driver.implicitly_wait(WAITING_MAX_TIME)

    def click(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()

    def sign_in(self, login, mdp):
        self.driver.get(URL_MYCARSPOT_LOGIN)
        try:
            lgn = self.driver.find_element_by_xpath('//*[@id="inputEmail"]')
            lgn.send_keys(login)
            psw = self.driver.find_element_by_xpath('//*[@id="password"]')
            psw.send_keys(mdp)
            self.click('//*[@id="ButtonSignIn"]')
        except NoSuchElementException as ex:
            logging.error('sign_in error: ' + ex.msg)
            raise


class MyCarSpotForEver(object):

    def __init__(self, selenium_processor, login_name, password):
        self.selenium = selenium_processor
        self.login(login_name, password)

    def login(self, login_name, password):
        try:
            self.selenium.sign_in(login_name, password)
        except NoSuchElementException as ex:
            logging.error('login error: ' + ex.msg)
            raise

    def confirm(self):
        try:
            self.selenium.click('//*[@id="ButtonConfirm"]')
        except NoSuchElementException as ex:
            logging.error('confirm error (invalid credentials or website has changed): ' + ex.msg)
            raise


def configure_selenium(driver_name, driver_executable_path, debug=False):
    return SeleniumProcessor(driver=driver_name,
                             driver_executable_path=driver_executable_path,
                             headless=not debug)


def process_args(args, defaults):
    parser = argparse.ArgumentParser(description=program_license, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.prog = 'mycarspotforever'
    parser.add_argument('--driver',
                        choices=['firefox', 'chrome'],
                        default="chrome",
                        help="Which driver should be used (default: %(default)s)")
    parser.add_argument('--driver_path',
                        metavar='driver_path',
                        default=CHROMEDRIVER_DEFAULT_PATH,
                        help='Path to web driver wich should be used (default: {})'.format(CHROMEDRIVER_DEFAULT_PATH))
    parser.add_argument('--version',
                        action='version',
                        version=program_version_message)
    parser.add_argument('--debug',
                        action='store_true',
                        default=True,
                        help="Launch webdriver with GUI (no headless mode).")
    parser.add_argument('--logins',
                        metavar='logins',
                        required=True,
                        help="Login names and passwords in 'user1:passwd1,user2:passwd2'")

    parameters = parser.parse_args(args)
    return parameters


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parameters = process_args(args, None)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    selenium_processor = configure_selenium(driver_name=parameters.driver,
                                            driver_executable_path=parameters.driver_path,
                                            debug=parameters.debug)

    users = parameters.logins.split(",")
    for user in users:
        login_name, password = user.split(":")
        mcs = MyCarSpotForEver(selenium_processor, login_name, password)
        time.sleep(SLEEP_TIME)
        mcs.confirm()
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
