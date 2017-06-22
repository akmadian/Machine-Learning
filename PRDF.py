# -*- coding: utf-8 -*-
"""
    File Name: guessby_row.py
    Author: Ari Madian
    Created: June 21, 2017 3:32 PM
    Python Version: 3.6
    Probability List Version: v1.2

    guessby_row.py - Part of Machine-Learning Repo
    Repo: github.com/akmadian/Machine-Learning
"""

import csv
from datetime import datetime
import statistics
from itertools import repeat
import random as random

RDF_Name = 'RDF_0001.csv'
PRDF_Name = 'PRDF_0001.csv'


def probability_list(l1, l2, l3, sno, streak, avstlen=None):
    """Generates a list that simulates the probability of
    the next value being a 0, 1, or 2.

    :param:
    l1       (int): Proportional ratio of number of 1s to 0s
    l2       (int): Proportional ratio of number of 1s to 1s
    l3       (int): Proportional ratio of number of 1s to 2s
    sno      (int): Current streak length
    streak   (int): Streak type a 0, 1, or 2
    avstlen  (int): Longest 2 streak length

    :return:
    list_    (list): Simulated probability list"""
    list_ = []
    list_.extend(repeat(0, int(round(l1))))
    list_.extend(repeat(1, int(round(l2))))
    list_.extend(repeat(2, int(round(l3))))
    if avstlen is not None:
        if streak == 2 and avstlen / 2 < sno < avstlen / 1.5:
            list_.append(2)
        elif streak == 2 and avstlen / 4 < sno < avstlen / 2:
            for _ in range(2): list_.append(2)
        elif streak == 2 and 0 < sno <= avstlen / 4:
            for _ in range(3): list_.append(2)
    return list_


def guess(p_list, stopnum):
    """Goes through the file and guesses the next value state

    :param:
    p_list   (list): The list returned by probability_list()
    stopnum  (int): The line number to stop guessing at

    :return:
    (list): How many guesses were correct and incorrect"""
    correct = 0
    incorrect = 0
    line_count = 0
    # print('Stop at: ' + str(stopnum))
    with open(RDF_Name) as f:
        reader = csv.reader(f)
        for line in reader:
            # print('Guess line count: ' + str(line_count))
            line_count += 1
            if len(line) == 6 and line[0].isdigit():
                # print('start')
                if int(line[0]) <= int(stopnum):
                    # print(line)
                    # print('Used')
                    guess_ = random.choice(p_list)
                    if int(line[4]) == guess_:
                        correct += 1
                    else:
                        incorrect += 1
                else:
                    # print('stopped')
                    break
        return [correct, incorrect]


def csv_write(rowsused, accuracy, timeofentcode, num_xslist, lx_streaklist,
              cstreak_list, forevery_list, value, timeofentstamp, looptime,
              problist, guesslist):
    """Writes processed data to a csv file

    :param:
    rowsused       (int): The number of rows processed in csv_read()
    accuracy       (int): The percentage of correct guesses
    timeofentcode  (int): The custom timestamp from the time the raw data
                          was written to the file
    num_xslist     (list): List with the vaiables [num_0s, num_1s, num_2s]
                           from csv_read()
    lx_streaklist  (list): List containing the largest streaks with the variables
                           [largest_0_streak, largest_1_streak, largest_2_streak]
                           from csv_read()
    cstreak_list   (list): List containing the current streak lengths with variables
                           [streak_0, streak_1, streak_2] from csv_read()
    forevery_list  (list): List containing the proportional ratios of the amount
                           of oud states with vaiables
                           [for_every_1_1, for_every_1_0, for_every_1_2] from csv_read()
    value          (int): The value of the stock from raw data file
    timeofentstamp (str): Timestamp from the raw data file at the time of the entry
    looptime       (str): Time delta of how long it took csv_read() to get to its current line
    problist       (list): The probability list returned by probability_list()
    guesslist      (list): The list returned by guess()"""
    values = [rowsused, accuracy, timeofentcode, num_xslist, lx_streaklist,
              cstreak_list, forevery_list, value, timeofentstamp, looptime,
              problist, guesslist]
    with open(PRDF_Name, 'a', newline='') as file:
        csv.writer(file).writerow(values)


def csv_read():
    """Reads a csv file, and does some stuff with the data."""
    num_0s = 0
    num_1s = 0
    num_2s = 0
    largest_0_streak = 0
    largest_1_streak = 0
    largest_2_streak = 0
    streaks_0 = []
    streaks_1 = []
    streaks_2 = []
    streak_0 = 0
    streak_1 = 0
    streak_2 = 0
    row_count = 0

    starttime = datetime.now()
    row = []
    with open(RDF_Name) as f:
        reader = csv.reader(f)
        for next_row in reader:
            print('-----------------------------------------')
            row_count += 1
            if row_count >= 4:

                if int(row[4]) == 0:
                    num_0s += 1
                    if int(row[5]) > largest_0_streak: largest_0_streak = int(next_row[5])
                    # Check if current streak is higher than last highest streak
                    if (int(next_row[4]) == 0) and (row[5] != 0): streak_0 += 1
                    # Add one to current streak counter if streak continues
                    if (int(row[4]) == 0) and (int(next_row[4]) != 0) and (int(row[5]) != 0):
                        # Check to see if streak ends on next row
                        streaks_0.append(streak_0)  # Add the last streak to the streaks list
                        streak_0 = 0  # Reset streak counter

                elif int(row[4]) == 1:
                    num_1s += 1
                    if int(row[5]) > largest_1_streak: largest_1_streak = int(next_row[5])
                    if (int(next_row[4]) == 1) and (row[5] != 0): streak_1 += 1
                    if (int(row[4]) == 1) and (int(next_row[4]) != 1) and (int(row[5]) != 0):
                        streaks_1.append(streak_1)
                        streak_1 = 0

                elif int(row[4]) == 2:
                    num_2s += 1
                    if int(row[5]) > largest_2_streak: largest_2_streak = int(next_row[5])
                    if (int(next_row[4]) == 2) and (row[5] != 0): streak_2 += 1
                    if (int(row[4]) == 2) and (int(next_row[4]) != 2) and (int(row[5]) != 0):
                        streaks_2.append(streak_2)
                        streak_2 = 0

                try:
                    for_every_1_0 = num_0s / num_1s  # Number of 1s for every 0
                    for_every_1_1 = num_1s / num_1s  # Number of 1s for every 1
                    for_every_1_2 = num_2s / num_1s  # Number of 2s for every 2
                except ZeroDivisionError as e:
                    print(e)
                    print('ZeroDivisionError at for_every_section')
                    for_every_1_0 = 1  # Set default values
                    for_every_1_1 = 1
                    for_every_1_2 = 5

                    prob_list = probability_list(for_every_1_1, for_every_1_0, for_every_1_2,
                                                 row[5], row[4], largest_2_streak)
                    # print('Row Count: ' + str(row_count))
                    print('SStop At: ' + str(row_count - 3))
                    guess_list = guess(prob_list, row_count - 3)
                    print('Sum: ' + str(sum(guess_list)))
                    # print(guess_list)
                    try:
                        percent_correct = round(((guess_list[0] / sum(guess_list)) * 100), 2)
                    except ZeroDivisionError as e:
                        print(e)
                        print('ZeroDivisionError at percent_correct def')
                        percent_correct = None

                    looptime = str(datetime.now() - starttime)[5:]

                    if sum(guess_list) == row_count - 3:
                        csv_write(row_count - 3,
                                  percent_correct,
                                  next_row[3],
                                  [num_0s, num_1s, num_2s],
                                  [largest_0_streak, largest_1_streak, largest_2_streak],
                                  [streak_0, streak_1, streak_2],
                                  [1, 1, 5],
                                  row[1],
                                  row[2],
                                  looptime,
                                  prob_list,
                                  guess_list)
                    else:
                        print('didnt add up - 0')
                else:
                    prob_list = probability_list(for_every_1_1, for_every_1_0, for_every_1_2,
                                                 row[5], row[4], largest_2_streak)
                    # print('Row Count: ' + str(row_count))
                    print('SStop At: ' + str(row_count - 3))
                    guess_list = guess(prob_list, row_count - 3)
                    print('Sum: ' + str(sum(guess_list)))
                    # print(guess_list)
                    try:
                        percent_correct = round(((guess_list[0] / sum(guess_list)) * 100), 2)
                    except ZeroDivisionError as e:
                        print(e)
                        print('ZeroDivisionError at percent_correct def')
                        percent_correct = None
                    looptime = str(datetime.now() - starttime)[5:]

                    if sum(guess_list) == row_count - 3:
                        csv_write(row_count - 3,
                                  percent_correct,
                                  next_row[3],
                                  [num_0s, num_1s, num_2s],
                                  [largest_0_streak, largest_1_streak, largest_2_streak],
                                  [streak_0, streak_1, streak_2],
                                  [round(for_every_1_1, 2), round(for_every_1_0, 2), round(for_every_1_2, 2)],
                                  row[1],
                                  row[2],
                                  looptime,
                                  prob_list,
                                  guess_list)
                    else:
                        print('didnt add up - 1')

                del row[:]
                row = [thing for thing in next_row]
            else:
                del row[:]
                row = [thing for thing in next_row]


csv_read()
