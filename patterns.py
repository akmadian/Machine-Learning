"""
    Parent File Name: patterns.py
    File Name: guess_v1.1.py
    Author: Ari Madian
    Created: May 31, 2017  9:16AM
    Python Version: 3.6
    Guess Algorithm Version: v1.1

    patterns.py - part of Machine-Learning Repo
    Repo: github.com/akmadian/Machine-Learning
"""

import csv
from datetime import datetime
import os
import statistics
from itertools import repeat
import random as random


outlist = []
run_count = 0


def average(streaks):
    try:
        streaks_without_zeros = [streak for streak in streaks if streak != 0]
        return statistics.mean(streaks_without_zeros)
    except statistics.StatisticsError:
        return 'Not enough data'


def probability_list_v1_1(l1, l2, l3, streak, sno, avstlen):
    list_ = []
    list_.extend(repeat(0, int(round(l1))))
    list_.extend(repeat(1, int(round(l2))))
    list_.extend(repeat(2, int(round(l3))))
    list_.append(2)
    if streak == 2 and avstlen / 2 < sno < avstlen / 1.5:
        list_.append(2)
    elif streak == 2 and avstlen / 4 < sno < avstlen / 2:
        list_.append(2)
        list_.append(2)
    elif streak == 2 and 0 < sno <= avstlen / 4:
        list_.append(2)
        list_.append(2)
        list_.append(2)
    return list_


def outfile_init():
    with open('patterns_outfile_0001.txt', 'w') as f:
        f.close()
    print('Outfile Initialized...')


def guess_v1_1(p_list):
    correct = 0
    incorrect = 0
    line_count = 0
    with open('COMMODITIES_GOLD_DATA_0011.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            line_count += 1
            if line_count >= 4:
                guess_ = random.choice(p_list)
                if int(line[4]) == guess_:
                    correct += 1
                else:
                    incorrect += 1
            else:
                pass
        return [correct, incorrect]


def csv_read():
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
    row = []
    starttime = datetime.now()
    with open('COMMODITIES_GOLD_DATA_0011.csv', 'r') as f:
        reader = csv.reader(f)
        print('CSV Opened...')
        print('Iterating...')
        for next_row in reader:
            row_count += 1
            if row_count >= 4:
                if int(row[4]) == 0:
                    num_0s += 1
                    if int(row[5]) > largest_0_streak:
                        largest_0_streak = int(next_row[5])
                    else:
                        pass
                    if (int(next_row[4]) == 0) and (row[5] != 0):
                        streak_0 += 1
                    else:
                        pass
                    if (int(row[4]) == 0) and (int(next_row[4]) != 0) and (int(row[5]) != 0):
                        streaks_0.append(streak_0)
                        streak_0 = 0
                    else:
                        pass
                elif int(row[4]) == 1:
                    num_1s += 1
                    if int(row[5]) > largest_1_streak:
                        largest_1_streak = int(next_row[5])
                    else:
                        pass
                    if (int(next_row[4]) == 1) and (row[5] != 0):
                        streak_1 += 1
                    else:
                        pass
                    if (int(row[4]) == 1) and (int(next_row[4]) != 1) and (int(row[5]) != 0):
                        streaks_1.append(streak_1)
                        streak_1 = 0
                    else:
                        pass
                elif int(row[4]) == 2:
                    num_2s += 1
                    if int(row[5]) > largest_2_streak:
                        largest_2_streak = int(next_row[5])
                    else:
                        pass
                    if (int(next_row[4]) == 2) and (row[5] != 0):
                        streak_2 += 1
                    else:
                        pass
                    if (int(row[4]) == 2) and (int(next_row[4]) != 2) and (int(row[5]) != 0):
                        streaks_2.append(streak_2)
                        streak_2 = 0
                    else:
                        pass
                del row[:]
                for thing in next_row:
                    row.append(thing)
            else:
                pass
                del row[:]
                for thing in next_row:
                    row.append(thing)

        for_every_1_0 = num_0s / num_1s
        for_every_1_1 = num_1s / num_1s
        for_every_1_2 = num_2s / num_1s
        prob_list = probability_list(for_every_1_1, for_every_1_0, for_every_1_2, next_row[4], next_row[5])
        guess_list = guess_v1_1(prob_list)
        percent_correct = round(((guess_list[0] / (guess_list[0] + guess_list[1])) * 100), 2)

        print('Num 0s, 1s, 2s:         ' + num_0s + ' - ' + num_1s + ' - ' + num_2s)
        print('Largest 0, 1, 2 Streak: ' + str(largest_0_streak) + ' - ' + str(largest_1_streak) + ' - ' + str(largest_2_streak))
        print('Num 0, 1, 2 Streaks:    ' + str(len(streaks_0)) + ' - ' + str(len(streaks_1)) + ' - ' + str(len(streak_2)))
        try:
            print('Streak 0 Avg: %s' % round(average(streaks_0), 3))
            print('Streak 1 Avg: %s' % round(average(streaks_1), 3))
            print('Streak 2 Avg: %s' % round(average(streaks_2), 3))
        except TypeError:
            print('Streak 0 Avg: %s' % average(streaks_0))
            print('Streak 1 Avg: %s' % average(streaks_1))
            print('Streak 2 Avg: %s' % average(streaks_2))
        print('Factor 1 for 1: %s' % round(for_every_1_1, 3))
        print('Factor 0 for 1: %s' % round(for_every_1_0, 3))
        print('Factor 2 for 1: %s' % round(for_every_1_2, 3))
        print('Probability list: %s' % prob_list)
        print('Num correct, incorrect guesses: %s' % guess_list)
        print('Percent Correct: %s' % percent_correct + '%')
        print('Total Lines: %s' % str(guess_list[0] + guess_list[1]))
        print('')
        time_delta = str(datetime.now() - starttime)[5:]
        print('Loop took: %s Seconds' % round(float(time_delta), 4))
        print('Done')

    return [percent_correct, prob_list, guess_list, row_count]


def main():
    outfile_init()
    csv_read()
