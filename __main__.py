"""
    File Name: __main__.py
    Author: Ari Madian
    Created: May 25, 2017 10:23 AM
    Python Version: 3.6

    __main__.py - Part of Machine-Learning Repo
    Repo: github.com/akmadian/Machine-Learning
"""
from lxml import html
import requests
import csv
import time
import arrow
import sys, traceback
import smtplib
import configparser
from string import Template
from twilio.rest import Client
import os
import socket

csv_headers = ['entryno.', 'value', 'UOD',
               'time', 'DOW', 'timeperiod',
               'OUDstreaktype', 'OUDstreakno.']
values = [0, 0, 0, 0, 0, 0, 0, 0]
values_cache = [0, 0, 0, 0, 0, 0, 0, 0]
entryno_counter = 1
write_file_name = 'COMMODITIES_GOLD_DATA_0011.csv'

GREEN = '\033[0;32m'
RESET = '\033[0;0m'
RED = '\033[0;31m'


def is_connected():
    """Checks to see if an internet connection is active"""
    try:
        host = socket.gethostbyname('www.google.com')
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def output(run_status, statuscode):
    """ Outputs console-like information about the program runtime"""
    sys.stdout.write('__main__.py' + '\n')
    # Status
    print('\r' + 'Status        - [', end='')
    if run_status == 1:  # Good
        print('\r' + 'Status        - [', end='')
        sys.stdout.write(GREEN)
        print('OK', end='')
        sys.stdout.write(RESET)
        sys.stdout.write(']' + '\n')
    elif run_status == 2:  # Stopped
        sys.stdout.write('\033[F')
        sys.stdout.flush()
        print('\r' + 'Status        - [', end='')
        sys.stdout.write(RED)
        print('STOPPED', end='')
        sys.stdout.write(RESET)
        sys.stdout.write(']' + '\n')
    print('Time          - [' + str(arrow_timestamp()) + ']') # Time
    print('Response Code - [' + str(statuscode) + ']') # Response Code
    print('Num Of Values - [' + str(entryno_counter) + ']') # Num of values written
    print('PID           - [' + str(os.getpid()) + ']') # Process ID
    print('Internet Conn - [' + str(is_connected()) + ']') # Connected To Internet
    print('\n')


def email(**kwargs):
    """ Emails an exception report

    Uses information passed in with kwargs to fill out a template and send
    an email containing the information.

    :param kwargs:
    extype      (str): The type of exception or error
    statuscode  (str): The HTML response code
    traceback   (str): The traceback message
    dir         (str): The path to the .py file the exception occurred in
    values      (str): The values and values_cache list, or any other relevant values
    programname (str): The name of the script, can provide additional info
    time        (str): The time at which the exception occurred
    addinfo     (str): Any additional information about the exception/ error
    :return:
    """
    args = ('exctype', 'statuscode', 'traceback',
            'dir', 'values', 'programname',
            'time', 'addinfo')
    for i in args:
        if i not in kwargs:
            kwargs[i] = None

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(config['BUGREPORTING']['larloginemail'],
                 config['BUGREPORTING']['larloginpassword'])
    t = Template("""Program name.....: $programname
Time of exception.....: $time
Exception Type.....: $extype
Callback message.....:
$traceback




Status code.....: $statuscode
Directory.....: $dir
Program name.....: $programname
Values.....:
$values


Additional Information.....: $addinfo




""")

    mes = 'Subject: Exception occurred and was caught\n\n' + t.substitute(kwargs) + \
          'Local log status.....:' + '\n\n End exception log'
    server.sendmail(config['BUGREPORTING']['larloginemail'],
                    config['BUGREPORTING']['lartoemail'], mes)
    server.quit()
    print('Email Log Successful')


def text_log(**kwargs):
    """Uses SMS to text an error report

    Uses information passed in via kwargs to generate an excpetion/ error report

    :param kwargs:
    See kwargs: in email() for kwargs docs
    :return:
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    account_sid = config['BUGREPORTING']['twilioaccssid']
    auth_token = config['BUGREPORTING']['twilioauthtoken']
    client = Client(account_sid, auth_token)

    t = Template('\n' + """

An exception occurred and was caught

Program name..: $programname

Time..: $time

Exception Type..: $extype
""")
    mess = t.substitute(kwargs)
    client.messages.create(
        to=config['BUGREPORTING']['twiliorecievenum'],
        from_=config['BUGREPORTING']['twiliosendnum'],
        body=mess)
    print('Text Log Successful')


def local_log(extype= None, statuscode= None, traceback= None,
              dir= None, values= None, programname= None, time=None,
              addinfo= None, fname=None):
    """ Logs an exception/ error report locally

    Longer description is essentially the same as email() and text_log()
    but it's a local text file.

    :param:
    fname       (str): What the log file should be named, do not include file extension
    See kwargs: in email() for the rest of them
    :return:
    """
    filename = fname + '.txt'
    '''
    with open(filename, 'w') as f:
        for arg in argslist:
            f.write(str(arg) + '.....:' + str(kwargs[arg]))
            '''
    print('Local Log Successful')


def scrape():
    """ Scrapes a stock value

    Uses requests and lxml to scrape a stock value
    :return:
    """
    stock_xpath = '//*[@id="cross_rate_1"]/tbody/tr[1]/td[4]'
    stock_site = 'https://www.investing.com/commodities/real-time-futures'

    del values_cache[:]
    for index in values:
        values_cache.append(index)
    del values[:]
    values.append(entryno_counter)
    value_ = []

    try:
        socket.create_connection((socket.gethostbyname('www.google.com'), 80), 2)
    except:
        time.sleep(900)
        scrape()
    else:
        pass

    try:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter()
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        page = session.get(stock_site, headers={'User-Agent': 'Mozilla/5.0'})
        code = str(page.status_code)
        try:
            assert 200 == 200
        except AssertionError as e:
            output(2, code)
            print(e)
            email(extype='AssertionError', statuscode=code, traceback=e,
                  values=[values, values_cache], programname='__main__.py/ COMMODITIES_GOLD.py',
                  addinfo='Bad status code.', time=arrow_timestamp())
            local_log(fname='__main__errlog_run_0004', extype='AssertionError',
                      statuscode=code, traceback=e, programname='__main__.py/ COMMODITIES_GOLD.py',
                      addinfo='Bad status code')
            text_log(time=arrow_timestamp(), programname='__main__.py/ COMMODITIES_GOLD.py', extype='AssertionError')
            raise AssertionError
        else:
            os.system('cls')
            output(1, code)
            print(values)
            print(values_cache)
            tree = html.fromstring(page.content)
            n_converted = tree.xpath(stock_xpath)
            s_converted = n_converted[0].text
            for letter in s_converted:
                if letter.isdigit():
                    value_.append(letter)
                elif letter == '\'' or letter == ',' or letter == '.':
                    pass
                nvalue = ''.join(value_)
            values.append(nvalue)
            CSVOps.csv_write(code)

    except requests.exceptions.Timeout as e:
        output(2, code)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        email(extype='requests.exceptions.ConnectionError', statuscode=code,
              traceback=exc_mes, values=[values, values_cache], programname='__main__.py/ COMMODITIES_GOLD.py')
        local_log(fname='__main__errlog_run_0004', extype='requests.exceptions.ConnectionError',
                  statuscode=code, traceback=exc_mes, programname='__main__.py/ COMMODITIES_GOLD.py',
                  addinfo='Connection error, see traceback')
        text_log(time=arrow_timestamp(), programname='__main__.py/ COMMODITIES_GOLD.py', extype='requests.exceptions.ConnectionError')
        time.sleep(900)
        scrape()
        print(exc_mes)

    except requests.exceptions.ConnectionError:
        output(2, code)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        email(extype='requests.exceptions.ConnectionError', statuscode=code,
              traceback=exc_mes, values=[values, values_cache], programname='__main__.py/ COMMODITIES_GOLD.py')
        local_log(fname='__main__errlog_run_0004', extype='requests.exceptions.ConnectionError',
                  statuscode=code, traceback=exc_mes, programname='__main__.py/ COMMODITIES_GOLD.py',
                  addinfo='Connection error, see traceback')
        text_log(time=arrow_timestamp(), programname='__main__.py/ COMMODITIES_GOLD.py', extype='requests.exceptions.ConnectionError')
        time.sleep(900)
        scrape()
        print(exc_mes)

    except requests.exceptions.RequestException as e:
        output(2, code)
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        email(extype='requests.exceptions.RequestException', statuscode=code,
              traceback=exc_mes, values=[values, values_cache], programname='__main__.py')
        local_log(fname='__main__errlog_run_0004', extype='requests.exceptions.RequestException',
                  statuscode=code, traceback=exc_mes, programname='__main__.py/ COMMODITIES_GOLD.py',
                  addinfo='Catchall requests error, see traceback')
        text_log(time=arrow_timestamp(), programname='__main__.py/ COMMODITIES_GOLD.py', extype='requests.exceptions.RequestException')


class OtherDataGet:
    """ Gets and assembles other types of data for the log file"""
    streak = 0
    streak_type = 3
    uod_state = 3

    @staticmethod
    def uod():
        """ Determines whether the last value was higher, lower, or the same
            as the one before it.

        :return int:    See main file docstring for int key
        """
        global values_cache
        try:
            if int(values[1]) > int(values_cache[1]):  # If value went up
                if OtherDataGet.streak_type != 0:  # If it was previously down or same
                    OtherDataGet.uod_state = 0  # Set state to up
                    OtherDataGet.streak = 0  # Reset streak
                    OtherDataGet.streak_type = 0  # Set streak type to up
                if int(values_cache[4]) == 0:  # If last state was up
                    OtherDataGet.streak += 1  # Add one to streak counter
                return 0
            elif int(values[1]) < int(values_cache[1]):  # If value went down
                if OtherDataGet.streak_type != 1:
                    OtherDataGet.uod_state = 1
                    OtherDataGet.streak = 0
                    OtherDataGet.streak_type = 1
                if int(values_cache[4]) == 1:
                    OtherDataGet.streak += 1
                return 1
            elif int(values[1]) == int(values_cache[1]):  # If value is the same
                if OtherDataGet.streak_type != 2:
                    OtherDataGet.uod_state = 2
                    OtherDataGet.streak = 0
                    OtherDataGet.streak_type = 2
                if int(values_cache[4]) == 2:
                    OtherDataGet.streak += 1
                return 2
        except IndexError:
            try:
                values_cache = [0, 0, 0, 0, 0, 0, 0]
                OtherDataGet.uod()
            except RecursionError:
                pass

    @staticmethod
    def day_of_week():
        """ Gets the day of the week

        :return int:    See docstring at top of file for int key
        """
        list_ = list(time.localtime())
        day = list_[6] + 1
        L = ['0', str(day)]
        return ''.join(L)

    @staticmethod
    def time_period():
        """ Gets the time period

        :return int:    year/mo/dow/12hr/6hr/3hr/1hr
        """
        tmp_list = []
        time_list_ = list(time.localtime())
        year = time_list_[0]
        month = time_list_[1]
        hour = int(time.strftime(format('%H')))
        tmp_list.append(str(year))
        tmp_list.append(''.join(['0', str(month)]))
        tmp_list.append(str(OtherDataGet.day_of_week()))
        if hour <= 12:
            tmp_list.append('01')
            if hour <= 6:
                tmp_list.append('01')
                if hour <= 3:
                    tmp_list.append('01')
                elif 3 < hour <= 6:
                    tmp_list.append('02')
                elif 6 < hour <= 9:
                    tmp_list.append('03')
                elif 9 < hour <= 12:
                    tmp_list.append('04')
            elif 6 < hour <= 12:
                tmp_list.append('02')
        elif hour > 12:
            tmp_list.append('02')
            if 12 < hour <= 18:
                tmp_list.append('03')
                if 12 < hour <= 15:
                    tmp_list.append('05')
                elif 15 < hour <= 18:
                    tmp_list.append('06')
                elif 18 < hour <= 21:
                    tmp_list.append('07')
                elif 21 < hour <= 24:
                    tmp_list.append('08')
            elif 18 < hour <= 24:
                tmp_list.append('04')
        tmp_list.append(str(hour))
        nlist = ''.join(tmp_list)
        return nlist


def arrow_timestamp():
    stamp = arrow.utcnow().to('US/Pacific').format('YYYY-MM-DD HH:mm:ss')
    return stamp


class CSVOps:
    """ Operations involving CSV files"""
    @staticmethod
    def csv_write(code):
        """ Writes to a csv file

        Gets additional information and writes it to a CSV file
        :return:
        """
        values.append(arrow_timestamp())
        values.append(int(OtherDataGet.time_period()))
        values.append(OtherDataGet.uod())
        values.append(OtherDataGet.streak)
        os.system('cls')
        output(1, code)
        print(values_cache)
        print(values)
        with open(write_file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(values)
        print(' - Written')

    @staticmethod
    def csv_init():
        """ Initializes a csv file with headers

        :return:
        """
        with open(write_file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)


if __name__ == '__main__':
    output(1, None)
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(' - Config File Parsed')
    time.sleep(1)
    print(' - CSV File Initiated')
    time.sleep(1)
    while True:
        scrape()
        entryno_counter += 1
