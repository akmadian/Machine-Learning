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
from lxml import html
import requests
import csv
import time
import sys
import random
import os
import sys, traceback
import smtplib

stock_xpath = '//*[@id="cross_rate_1"]/tbody/tr[1]/td[4]'
stock_site = 'https://www.investing.com/commodities/real-time-futures'
request_header = {'User-Agent': 'Mozilla/5.0'}
# CSV HEADERS - [INT, INT, INT, INT, INT, INT, INT, INT]
csv_headers = ['entryno.','value','UOD','time','DOW','timeperiod','OUDstreaktype','OUDstreakno.']
values = [0, 0, 0, 0, 0, 0, 0, 0]
values_cache = [0, 0, 0, 0, 0, 0, 0, 0]
entryno_counter = 1


def email(exc_traceback_thing):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('importantaristuff@gmail.com', 'Rycbar1234')
    mes = """A runtime exception occurred during the running of the Commodities_Gold.py
For more information see console.""" + str(exc_traceback_thing)
    server.sendmail('importantaristuff@gmail.com',
                    'importantaristuff@gmail.com', mes)
    server.quit()


def scrape():
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
        page = session.get(stock_site, headers=request_header)
        code = str(page.status_code)
        try:
            assert (code == '200')
        except AssertionError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc_mes = repr(
                traceback.format_exception(exc_type, exc_value, exc_traceback))
            email(exc_mes)
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
    except requests.exceptions.ConnectionError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(
            traceback.format_exception(exc_type, exc_value, exc_traceback))
        email(exc_mes)
        time.sleep(900)
        scrape()
    except requests.exceptions.RequestException as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_mes = repr(
            traceback.format_exception(exc_type, exc_value, exc_traceback))
        email(exc_mes)
        raise e


class OtherDataGet:
    streak = 0
    streak_type = 3
    uod_state = 3

    @staticmethod
    def uod():
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
        # timelist format = [year, month, day, hour, minute, second, weekday, yearday]
        timelist = list(time.localtime())
        hour = time.strftime(format('%H'))
        time_ = [str(hour), str((timelist[4])), str((timelist[5]))]
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
        return int(time__)

    @staticmethod
    def day_of_week():
        list_ = list(time.localtime())
        day = list_[6] + 1
        L = ['0', str(day)]
        return ''.join(L)

    @staticmethod
    def time_period():
        '''
        Day of week
        Time of day 12hr
        Time of day 6hr
        Time of day 3hr
        time of day 1hr
        :return:
        '''
        tmp_list = []
        time_list_ = list(time.localtime())
        time_ = str(OtherDataGet.time())
        time_list = [time_[i:i+2] for i in range(0, len(time_), 2)]
        print(time_list)
        year = time_list_[0]
        month = time_list_[1]
        hour = int(time_list[0])
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
    @staticmethod
    def csv_write():
        values.append(OtherDataGet.uod())
        values.append(OtherDataGet.time())
        values.append(int(OtherDataGet.time_period()))
        values.append(OtherDataGet.streak_type)
        values.append(OtherDataGet.streak)
        print(values)
        with open('COMMODITIES_GOLD_DATA_0002.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(values)

    @staticmethod
    def csv_init():
        with open('COMMODITIES_GOLD_DATA_0002.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)


def main():
    print(OtherDataGet.time())
    conditional = (150000 <= OtherDataGet.time() > 141500)
    if conditional:
        scrape()
        global entryno_counter
        entryno_counter += 1
    elif not conditional:
        print('Not in time range')
        pass


CSVOps.csv_init()
while True:
    main()
