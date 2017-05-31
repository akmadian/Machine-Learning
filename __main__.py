"""
--------------------
    Initially created
    May 25, 2017 10:23 AM

    scrape.py

    Part of my machine learning project


    INT VALUES FOR Up Or Down (UOD)
    0 - Up
    1 - Down
    2 - Same


    INT VALUES FOR DAYS OF THE WEEK
    0 - Sunday
    1 - Monday
    2 - Tuesday
    3 - Wednesday
    4 - Thursday
    5 - Friday
    6 - Saturday
--------------------
"""
from lxml import html           # HTML Scraping
import requests                 # Gets page for lxml
import csv                      # CSV parser
import time
import sys, traceback           # Exception handling
import smtplib                  # Exception handling
import configparser             # Config file parser
from string import Template     # Exception handling
from twilio.rest import Client  # Exception handling

# TODO: Document all classes and functions

stock_xpath = '//*[@id="cross_rate_1"]/tbody/tr[1]/td[4]'   # Up here for easy reference
stock_site = 'https://www.investing.com/commodities/real-time-futures'
csv_headers = ['entryno.','value','UOD',
               'time','DOW','timeperiod',
               'OUDstreaktype','OUDstreakno.']
values = [0, 0, 0, 0, 0, 0, 0, 0]
values_cache = [0, 0, 0, 0, 0, 0, 0, 0]
entryno_counter = 1


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
    argslist = ('extype', 'statuscode', 'traceback',
                'dir', 'values', 'programname',
                'time', 'addinfo')
    for arg in argslist:
        if arg not in kwargs:
            kwargs[arg] = 'None'
        else:
            pass
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

    mes = 'Subject: Exception occurred and was caught\n\n' + t.substitute(**kwargs) + \
          'Local log status.....:' + '\n\n End exception log'
    server.sendmail(config['BUGREPORTING']['larloginemail'],
                    config['BUGREPORTING']['lartoemail'], mes)
    server.quit()


def text_log(**kwargs):
    """Uses SMS to text an error report

    Uses information passed in via kwargs to generate an excpetion/ error report

    :param kwargs:
    See kwargs: in email() for kwargs docs
    :return:
    """
    argslist = ('extype', 'statuscode', 'traceback',
                'dir', 'values', 'programname',
                'time', 'addinfo')
    for arg in argslist:
        if arg not in kwargs:
            kwargs[arg] = 'None'
        else:
            pass
    config = configparser.ConfigParser()
    config.read('config.ini')
    account_sid = config['BUGREPORTING']['twilioaccssid']
    auth_token = config['BUGREPORTING']['twilioauthtoken']
    client = Client(account_sid, auth_token)

    t = Template("""
An exception occurred and was caught
Check email report and/or local report for more information
Program name..: $programname
Time..: $time
Exception Type..: $extype
""")
    mess = t.substitute(kwargs)
    client.messages.create(
        to=config['BUGREPORTING']['twiliorecievenum'],
        from_=config['BUGREPORTING']['twiliosendnum'],
        body=mess)


def local_log(**kwargs):
    """ Logs an exception/ error report locally

    Longer description is essentially the same as email() and text_log()
    but it's a local text file.

    :param kwargs:
    fname       (str): What the log file should be named, do not include file extension
    See kwargs: in email() for the rest of them
    :return:
    """
    argslist = ('fname', 'extype', 'statuscode',
                'traceback', 'dir', 'values',
                'programname', 'time', 'addinfo')
    for arg in argslist:
        if arg not in kwargs:
            kwargs[arg] = 'None'
        else:
            pass
    filename = kwargs['fname'] + '.txt'
    with open(filename, 'w') as f:
        for arg in argslist:
            f.write(str(arg) + '.....:' + str(kwargs[arg]))


def scrape():
    """ Scrapes a stock value

    Uses requests and lxml to scrape a stock value
    :return:
    """
    del values_cache[:]
    for index in values:
        values_cache.append(index)
    del values[:]
    values.append(entryno_counter)
    value_ = []
    try:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter()
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        page = session.get(stock_site, headers={'User-Agent': 'Mozilla/5.0'})
        code = str(page.status_code)
        try:
            assert 200 <= code < 300
        except AssertionError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            email(extype='AssertionError', statuscode=code, traceback=exc_mes,
                  values=[values, values_cache], programname='__main__.py/ COMMODITIES_GOLD.py',
                  addinfo='Bad status code.')
            local_log(fname='__main__errlog_run_0004', extype='AssertionError',
                      statuscode=code, traceback=exc_mes, programname='__main__.py/ COMMODITIES_GOLD.py',
                      addinfo='Bad status code')
            text_log(time=OtherDataGet.time(), programname='__main__.py/ COMMODITIES_GOLD.py', extype='AssertionError')
            raise AssertionError
        else:
            print('Status Code %s' % code)
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
            print(values)
            CSVOps.csv_write()
        finally:
            print('Status Code %s' % code)
    except requests.exceptions.ConnectionError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        email(extype='requests.exceptions.ConnectionError', statuscode=code,
             traceback=exc_mes, values=[values, values_cache], programname='__main__.py/ COMMODITIES_GOLD.py')
        local_log(fname='__main__errlog_run_0004', extype='requests.exceptions.ConnectionError',
                  statuscode=code, traceback=exc_mes, programname='__main__.py/ COMMODITIES_GOLD.py',
                  addinfo='Connection error, see traceback')
        text_log(time=OtherDataGet.time(), programname='__main__.py/ COMMODITIES_GOLD.py', extype='requests.exceptions.ConnectionError')
        time.sleep(900)
        scrape()
    except requests.exceptions.RequestException as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        email(extype='requests.exceptions.RequestException', statuscode=code,
             traceback=exc_mes, values=[values, values_cache], programname='__main__.py/ COMMODITIES_GOLD.py')
        local_log(fname='__main__errlog_run_0004', extype='requests.exceptions.RequestException',
                  statuscode=code, traceback=exc_mes, programname='__main__.py/ COMMODITIES_GOLD.py',
                  addinfo='Catchall requests error, see traceback')
        text_log(time=OtherDataGet.time(), programname='__main__.py/ COMMODITIES_GOLD.py', extype='requests.exceptions.RequestException')


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
        if int(values[1]) > int(values_cache[1]):  # If value went up
            if OtherDataGet.streak_type != 0:  # If it was previously down or same
                OtherDataGet.uod_state = 0  # Set state to up
                OtherDataGet.streak = 0  # Reset streak
                OtherDataGet.streak_type = 0  # Set streak type to up
            if int(values_cache[5]) == 0:  # If last state was up
                OtherDataGet.streak += 1  # Add one to streak counter
            return 0
        elif int(values[1]) < int(values_cache[1]):
            if OtherDataGet.streak_type != 1:
                OtherDataGet.uod_state = 1
                OtherDataGet.streak = 0
                OtherDataGet.streak_type = 1
            if int(values_cache[5]) == 1:
                OtherDataGet.streak += 1
            return 1
        elif int(values[1]) == int(values_cache[1]):
            if OtherDataGet.streak_type != 2:
                OtherDataGet.uod_state = 2
                OtherDataGet.streak = 0
                OtherDataGet.streak_type = 2
            if int(values_cache[5]) == 2:
                OtherDataGet.streak += 1
            return 2

    @staticmethod
    def time():
        """ Gets the time in 24hr format

        Combines hour, minute, second into a single integer
                hr/min/sec
        :return int:
        """
        # timelist format = [year, month, day, hour, minute, second, weekday, yearday]
        timelist = list(time.localtime())
        hour = time.strftime(format('%H'))
        time_ = [hour, str((timelist[4])), str((timelist[5]))]
        if len(time_[0]) == 1:
            L = ['0', time_[0]]
            nhour = ''.join(L)
            time_[0] = nhour
        elif len(time_[0]) == 0:
            time_[0] = '00'
        if len(time_[1]) == 1:
            L = ['0', time_[1]]
            nmin = ''.join(L)
            time_[1] = nmin
        if len(time_[2]) == 1:
            L = ['0', time_[2]]
            nsec = ''.join(L)
            time_[2] = nsec
        time__ = str(''.join(time_))
        return time__

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
        time_ = str(OtherDataGet.time())
        time_list = [time_[i:i+2] for i in range(0, len(time_), 2)]
        print(time_list)
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


class CSVOps:
    """ Operations involving CSV files"""
    @staticmethod
    def csv_write():
        """ Writes to a csv file

        Gets additional information and writes it to a CSV file
        :return:
        """
        values.append(OtherDataGet.uod())
        values.append(OtherDataGet.time())
        values.append(int(OtherDataGet.time_period()))
        values.append(OtherDataGet.streak_type)
        values.append(OtherDataGet.streak)
        print(values)
        with open('COMMODITIES_GOLD_DATA_0004.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(values)

    @staticmethod
    def csv_init():
        """ Initializes a csv file with headers

        :return:
        """
        with open('COMMODITIES_GOLD_DATA_0004.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)


def main(): # TODO: Document
    print(OtherDataGet.time())
    #conditional = (150000 <= OtherDataGet.time() > 141500)
    #if conditional:
    scrape()
    global entryno_counter
    entryno_counter += 1
    #elif not conditional:
    #   print('Not in time range')
    #    pass


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    CSVOps.csv_init()
    while True:
        main()
