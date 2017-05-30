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
import console

stock_xpath = '//*[@id="last_last"]'
stock_site = 'https://www.investing.com/equities/amazon-com-inc'
request_header = {'User-Agent': 'Mozilla/5.0'}
# CSV HEADERS - [INT, INT, INT, INT, INT, INT, INT, INT]
csv_headers = ('entryno.','value','UOD','time','DOW','timeperiod','OUDstreaktype','OUDstreakno.')
values = []
values_cache = []
entryno_counter = 1


def scrape():
    del values_cache[:]
    for index in values:
        values_cache.append(index)
    del values[:]
    values.append(entryno_counter)
    value_ = []
    page = requests.get(stock_site, headers=request_header)
    code = str(page.status_code)
    print('Status Code %s' % code)
    try:
        assert (199 < code > 300)
    except AssertionError:
        pass
    else:
        tree = html.fromstring(page.content)
        n_converted = tree.xpath(stock_xpath)
        s_converted = n_converted[0].text
        converted = str(s_converted.encode('utf-8'))
        for letter in converted:
            conditional = bool(letter.isdigit() or letter == '.' or
                               letter == ',' or letter == '+' or
                               letter == '-' or letter == '%')
            if conditional:
                value_.append(letter)
                joinedvalue = ''.join(value_)
            elif (conditional is False) or (letter == 'b'):
                pass
            values.append(joinedvalue)
    CSVOps.csv_write()


class OtherDataGet:
    streak = 0
    streak_type = 3
    uod_state = 3

    @staticmethod
    def uod():
        if entryno_counter == 1:
            pass
        else:
            if values[1] > values_cache[1]:  # If value went up
                if OtherDataGet.uod_state == 1 or 2:  # If it was previously down or same
                    OtherDataGet.uod_state = 0  # Set state to up
                    OtherDataGet.streak = 0  # Reset streak
                    OtherDataGet.streak_type = 0  # Set streak type to up
                elif OtherDataGet.uod_state == 0:  # If last state was up
                    OtherDataGet.streak += 1  # Add one to streak counter
                return 0
            elif values[1] < values_cache[1]:
                if OtherDataGet.uod_state == 0 or 2:
                    OtherDataGet.uod_state = 1
                    OtherDataGet.streak = 0
                    OtherDataGet.streak_type = 1
                elif OtherDataGet.uod_state == 1:
                    OtherDataGet.streak += 1
                return 1
            elif values[1] == values_cache[1]:
                if OtherDataGet.uod_state == 0 or 1:
                    OtherDataGet.uod_state = 2
                    OtherDataGet.streak = 0
                    OtherDataGet.streak_type = 2
                elif OtherDataGet.uod_state == 2:
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
        return day

    @staticmethod
    def time_period():
        return 404

    @staticmethod
    def uod_streak_no():
        return OtherDataGet.streak


class CSVOps:
    @staticmethod
    def csv_write():
        values.append(str(OtherDataGet.uod()))
        values.append(str(OtherDataGet.time()))
        values.append(str(OtherDataGet.time_period()))
        values.append(str(OtherDataGet.streak_type))
        values.append(str(OtherDataGet.streak))
        with open('NASDAQ_AMZN_DATA.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(values)

    @staticmethod
    def csv_init():
        with open('NASDAQ_AMZN_DATA.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)


def main():
    conditional = (130000 > OtherDataGet.time()) and (OtherDataGet.time() > int(0o063000))
    if conditional:
        scrape()
        global entryno_counter
        entryno_counter += 1
        print(entryno_counter)
    elif not conditional:
        pass


CSVOps.csv_init()


while True:
    main()



