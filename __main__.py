# -*- coding: utf-8 -*-
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
import sys
import traceback
import smtplib
import configparser
from string import Template
from twilio.rest import Client
import os
import socket

args = sys.argv[1:]
print(args)

config = configparser.ConfigParser().read('config.ini')

csv_headers = ['entryno.', 'value',
               'time', 'DOW', 'timeperiod',
               'OUDstreaktype', 'OUDstreakno.',
               'looptime']

RDF_Name = 'RDF_0003.csv'
RDF_Path = os.path.dirname(os.path.realpath(sys.argv[0])) + \
            '/Data-Files/Raw-Data-Files/' + \
            RDF_Name

values = [0, 0, 0, 0, 0, 0, 0, 0]
values_cache = [0, 0, 0, 0, 0, 0, 0, 0]
entryno_counter = 0

GREEN = '\033[0;32m'
RESET = '\033[0;0m'
RED = '\033[0;31m'

streak = 0
streak_type = 3
uod_state = 3


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
    if '-v' in args: print('Email Log Started')
    args_ = ('exctype', 'statuscode', 'traceback',
            'dir', 'values', 'programname',
            'time', 'addinfo')
    for i in args_:
        if i not in kwargs:
            if '-v' in args: print(str(i) + ' - Not in kwargs')
            kwargs[i] = None

    server = smtplib.SMTP('smtp.gmail.com', 587)
    if '-v' in args: print('Server Connection Established')
    server.ehlo()
    server.starttls()
    if '-v' in args: print('Ehlo and Starttls Successful')
    server.login(config['BUGREPORTING']['larloginemail'],
                 config['BUGREPORTING']['larloginpassword'])
    if '-v' in args: print('Login Successful')
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
    if '-v' in args: print('Message Defined')
    server.sendmail(config['BUGREPORTING']['larloginemail'],
                    config['BUGREPORTING']['lartoemail'], mes)
    if '-v' in args: print('Message Sent')
    server.quit()
    if '-v' in args: print('Server Connection Broken')
    if '-v' in args: print('Email Log Successful')


def text_log(**kwargs):
    """Uses SMS to text an error report

    Uses information passed in via kwargs to generate an excpetion/ error report

    :param kwargs:
    See kwargs: in email() for kwargs docs
    :return:
    """
    if '-v' in args: print('Text Log Started')
    account_sid = config['BUGREPORTING']['twilioaccssid']
    auth_token = config['BUGREPORTING']['twilioauthtoken']
    client = Client(account_sid, auth_token)
    if '-v' in args: print('Client Defined')

    t = Template('\n' + """

An exception occurred and was caught

Program name..: $programname

Time..: $time

Exception Type..: $extype
""")
    if '-v' in args: print('Message Defined')
    mess = t.substitute(kwargs)
    client.messages.create(
        to=config['BUGREPORTING']['twiliorecievenum'],
        from_=config['BUGREPORTING']['twiliosendnum'],
        body=mess)
    if '-v' in args: print('Text Log Successful')


def local_log(**kwargs):
    """ Logs an exception/ error report locally

    Longer description is essentially the same as email() and text_log()
    but it's a local text file.

    :param:
    fname       (str): What the log file should be named, do not include file extension
    See kwargs: in email() for the rest of them
    :return:
    """
    args_ = ('exctype', 'statuscode', 'traceback',
            'dir', 'values', 'programname',
            'time', 'addinfo')
    for i in args_:
        if i not in kwargs:
            kwargs[i] = None
    try:
        filename = kwargs['fname'] + '.txt'
        with open(filename, 'w') as f:
            for arg in args_:
                f.write(str(arg) + ' - ' + str(kwargs[arg]) + '\n')
    except Exception as e:
        print(e)
        print('-== Local Log Unsuccessful ==-')

    print('Local Log Successful')


def scrape():
    """ Scrapes a stock value

    Uses requests and lxml to scrape a stock value
    :return:
    """
    stock_xpath = '//*[@id="cross_rate_1"]/tbody/tr[1]/td[4]'
    stock_site = 'https://www.investing.com/commodities/real-time-futures'

    del values_cache[:]
    if '-v' in args: print('Values Cache Cleared')
    for index in values:
        values_cache.append(index)
    if '-v' in args: print('Values Cache Updated')
    del values[:]
    if '-v' in args: print('Values Cleared')
    values.append(entryno_counter)
    value_ = []

    try:
        socket.create_connection((socket.gethostbyname('www.google.com'), 80), 2)
    except socket.timeout as e:
        print(e)
        print('-== Timeout Caught ==-')
        time.sleep(900)
        scrape()

    except Exception as e:
        print(e)
        print('-== Generic Exception Caught ==-')
        time.sleep(900)
        scrape()
    else:
        if '-v' in args: print('Good Connection')

    try:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter()
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        if '-v' in args: print('Session Mounted')
        page = session.get(stock_site, headers={'User-Agent': 'Mozilla/5.0'})
        if '-v' in args: print('Page Recieved')
        code = str(page.status_code)

        try:
            assert 200 <= int(code) < 300
        except AssertionError as e:
            print(e)
            print('-== Bad Status Code Returned ==-')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            email(extype='AssertionError', statuscode=code, traceback=exc_mes,
                  values=[values, values_cache], programname='Machine-Learning/__main__.py',
                  addinfo='Bad status code.', time=arrow_timestamp())
            local_log(fname='__main__errlog_run_0004', extype='AssertionError',
                      statuscode=code, traceback=e, programname='Machine-Learning/__main__.py',
                      addinfo='Bad status code')
            text_log(time=arrow_timestamp(), programname='Machine-Learning/__main__.py',
                     extype='AssertionError')

        else:
            if '-v' in args: print('Good Status Code Returned')
            tree = html.fromstring(page.content)
            value = tree.xpath(stock_xpath)[0].text
            for letter in value:
                if letter.isdigit():
                    value_.append(letter)
                elif letter == '\'' or letter == ',' or letter == '.':
                    pass
            values.append(int(''.join(value_)))
            if '-v' in args: print('Value Appended')
            csv_write(code)

    except requests.exceptions.Timeout as e:
        print(e)
        print('-== Timeout Exception Raised ==-')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        try:
            email(extype='requests.exceptions.ConnectionError', statuscode=code,
                  traceback=exc_mes, values=[values, values_cache],
                  programname='Machine-Learning/__main__.py')
        except NameError as e:
            print(e)
            print('-== NameError raised during Timeout exception catch ==-')
            email(extype='requests.exceptions.ConnectionError', traceback=exc_mes,
                  values=[values, values_cache], programname='Machine-Learning/__main__.py')
        local_log(fname='__main__errlog_run_0004', extype='requests.exceptions.ConnectionError',
                  statuscode=code, traceback=exc_mes, programname='Machine-Learning/__main__.py',
                  addinfo='Connection error, see traceback')
        text_log(time=arrow_timestamp(), programname='Machine-Learning/__main__.py',
                 extype='requests.exceptions.ConnectionError')
        time.sleep(900)
        scrape()
        print(exc_mes)

    except requests.exceptions.ConnectionError as e:
        print(e)
        print('-== ConnectionError Exception Raised ==-')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        try:
            email(extype='requests.exceptions.ConnectionError', statuscode=code,
                  traceback=exc_mes, values=[values, values_cache],
                  programname='__main__.py')
        except NameError as e:
            print(e)
            print('-== NameError Raised during ConnectionError Handling ==-')
            email(extype='requests.exceptions.ConnectionError',
                  traceback=exc_mes, values=[values, values_cache],
                  programname='__main__.py')

        local_log(fname='__main__errlog_run_0004', extype='requests.exceptions.ConnectionError',
                  statuscode=code, traceback=exc_mes, programname='__main__.py',
                  addinfo='Connection error, see traceback')
        text_log(time=arrow_timestamp(), programname='__main__.py',
                 extype='requests.exceptions.ConnectionError')
        time.sleep(900)
        scrape()

    except requests.exceptions.RequestException as e:
        print(e)
        print('-== Generic RequestException Raised ==-')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        try:
            email(extype='requests.exceptions.RequestException', statuscode=code,
                  traceback=exc_mes, values=[values, values_cache], programname='__main__.py')
        except NameError as e:
            print(e)
            print('NameError raised during RequestException Catch')
            email(extype='requests.exceptions.RequestException', traceback=exc_mes,
                  values=[values, values_cache], programname='__main__.py')
        local_log(fname='__main__errlog_run_0004', extype='requests.exceptions.RequestException',
                  statuscode=code, traceback=exc_mes, programname='__main__.py',
                  addinfo='Catchall requests error, see traceback')
        text_log(time=arrow_timestamp(), programname='__main__.py/ COMMODITIES_GOLD.py',
                 extype='requests.exceptions.RequestException')


def uod():
    """ Determines whether the last value was higher, lower, or the same
        as the one before it.

    :return int:    See main file docstring for int key
    """
    global values_cache
    global streak_type
    global uod_state
    global streak
    try:
        if '-v' in args: print('uod() Now Running')
        if int(values[1]) > int(values_cache[1]):  # If value went up
            if streak_type != 0:  # If it was previously down or same
                uod_state = 0  # Set state to up
                streak = 0  # Reset streak
                streak_type = 0  # Set streak type to up
            if int(values_cache[4]) == 0:  # If last state was up
                streak += 1  # Add one to streak counter
            return 0
        elif int(values[1]) < int(values_cache[1]):  # If value went down
            if streak_type != 1:
                uod_state = 1
                streak = 0
                streak_type = 1
            if int(values_cache[4]) == 1:
                streak += 1
            return 1
        elif int(values[1]) == int(values_cache[1]):  # If value is the same
            if streak_type != 2:
                uod_state = 2
                streak = 0
                streak_type = 2
            if int(values_cache[4]) == 2:
                streak += 1
            return 2
    except IndexError as e:
        print(e)
        print('-== IndexError Caught During uod() Run ==-')
        try:
            values_cache = [0, 0, 0, 0, 0, 0, 0]
            if '-v' in args: print('Retrying uod()')
            uod()
        except RecursionError as e:
            print(e)
            print('-== RecursionError Caught During uod() Retry ==-')
            pass


def istrading():
    """ Determines if the script is running within the stock's trading hours"""
    dow = arrow.utcnow().to('US/Pacific').format('dddd')
    if '-v' in args: print('DOW Defined')
    time_ = arrow.utcnow().to('US/Pacific').format('HHmm')
    if '-v' in args: print('Time Defined')
    if dow != 'Saturday' and 1500 < int(time_) > 1415:
        if '-v' in args: print('Istrading - True')
        return True
    else:
        if '-v' in args: print('Istrading - False')
        return False


def time_period():
    """Gets a custom timestamp"""
    stamp = arrow.utcnow().to('US/Pacific').format('YYYYMMDDdHHmmss')
    if '-v' in args: print('Custom Stamp Defined')
    return stamp


def arrow_timestamp():
    """Gets a generic timestamp"""
    stamp = arrow.utcnow().to('US/Pacific').format('YYYY-MM-DD HH:mm:ss')
    if '-v' in args: print('Generic Stamp Defined')
    return stamp


def csv_write(code):
    """ Writes to a csv file

    Gets additional information and writes it to a CSV file
    """
    values.append(arrow_timestamp())
    if '-v' in args: print('Timestamp Appended')
    values.append(int(time_period()))
    if '-v' in args: print('Custom Timestamp Appended')
    values.append(uod())
    if '-v' in args: print('uod Appended')
    values.append(streak)
    if '-v' in args: print('Streak Appended')
    print(values_cache)
    print(values)

    with open(RDF_Path, 'a', newline='') as file:
        looptime = str(time.time() - starttime)[:7]
        print('Looptime - ' + looptime)
        values.append(looptime)
        csv.writer(file).writerow(values)
    if '-v' in args: print('Values Written')


def csv_init():
    """ Initializes a csv file with headers and necessary data for PRDF"""
    cases = [[None, None, None, None, 0, 2],
             [None, None, None, None, 1, 2],
             [None, None, None, None, 2, 2]]
    with open(RDF_Path, 'w') as file:
        csv.writer(file).writerow(csv_headers)
        for list_ in cases:
            csv.writer(file).writerow(list_)
        if '-v' in args: print('CSV Initialized')


def argsinterpret(listchoice):
    """Interprets sys.argv data

    :param:
    listchoice  (str): The users choice of which arg list to return"""
    rawargs = sys.argv
    addargs = sys.argv[1:]
    groupedargs = [''.join([thing, next(iter(rawargs))])
    if 'test' in thing else None for thing in iter(rawargs)]
    return rawargs if listchoice == 'rawargs' \
        else addargs if listchoice == 'addargs' \
        else groupedargs if listchoice == 'groupedargs' \
        else 'Not a valid option'


while True:
    if True:
        if '-v' in args: print('Is Trading')
        starttime = time.time()
        scrape()
        if '-v' in args: print('Loop Successful')
        entryno_counter += 1
    else:
        if '-v' in args: print('Not Trading')
        time.sleep(300)
        continue
