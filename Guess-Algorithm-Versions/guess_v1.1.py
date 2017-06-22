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
import time
from datetime import datetime
import os
import sys
import statistics
from itertools import repeat
import random as random


outlist = []
run_count = 0


def average(streaks):
    streaks_without_zeros = [streak for streak in streaks if streak != 0]
    return statistics.mean(streaks_without_zeros)


def probability_list(l1, l2, l3):
    list_ = []
    list_.extend(repeat(0, int(round(l1))))
    list_.extend(repeat(1, int(round(l2))))
    list_.extend(repeat(2, int(round(l3))))
    return list_


def outfile_init():
    with open('patterns_outfile_0001.txt', 'w') as f:
        f.close()
    print('Outfile Initialized...')


def guess_v1_1(p_list):
    correct = 0
    incorrect = 0
    line_count = 0
    with open('combined.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            line_count += 1
            if line_count >= 4:
                guess_ = random.choice(p_list)
                if int(line[5]) == guess_:
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
    with open('combined.csv', 'r') as f:
        reader = csv.reader(f)
        print('CSV Opened...')
        print('Iterating...')
        for next_row in reader:
            row_count += 1
            #print(row_count)
            #print('Row     : %s' % row)
            #print('Next Row: %s' % next_row)
            if row_count >= 4:
                #print('Start')
                if int(row[5]) == 0:
                    num_0s += 1
                    if int(row[6]) > largest_0_streak:
                        largest_0_streak = int(next_row[6])
                    else:
                        pass
                    if (int(next_row[5]) == 0) and (row[6] != 0):
                        streak_0 += 1
                    else:
                        pass
                    if (int(row[5]) == 0) and (int(next_row[5]) != 0) and (int(row[6]) != 0):
                        streaks_0.append(streak_0)
                        streak_0 = 0
                    else:
                        pass
                elif int(row[5]) == 1:
                    num_1s += 1
                    if int(row[6]) > largest_1_streak:
                        largest_1_streak = int(next_row[6])
                    else:
                        pass
                    if (int(next_row[5]) == 1) and (row[6] != 0):
                        streak_1 += 1
                    else:
                        pass
                    if (int(row[5]) == 1) and (int(next_row[5]) != 1) and (int(row[6]) != 0):
                        streaks_1.append(streak_1)
                        streak_1 = 0
                    else:
                        pass
                elif int(row[5]) == 2:
                    num_2s += 1
                    if int(row[6]) > largest_2_streak:
                        largest_2_streak = int(next_row[6])
                    else:
                        pass
                    if (int(next_row[5]) == 2) and (row[6] != 0):
                        streak_2 += 1
                    else:
                        pass
                    if (int(row[5]) == 2) and (int(next_row[5]) != 2) and (int(row[6]) != 0):
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
        prob_list = probability_list(for_every_1_1, for_every_1_0, for_every_1_2)
        guess_list = guess(prob_list)
        percent_correct = round(((guess_list[0] / (guess_list[0] + guess_list[1])) * 100), 2)

        os.system('cls')
        print('Num 0s: %s' % num_0s)
        print('Num 1s: %s' % num_1s)
        print('Num 2s: %s' % num_2s)
        print('Largest 0 Streak: %s' % largest_0_streak)
        print('Largest 1 Streak: %s' % largest_1_streak)
        print('Largest 2 Streak: %s' % largest_2_streak)
        print('Num 0 Streaks: %s' % len(streaks_0))
        print('Num 1 Streaks: %s' % len(streaks_1))
        print('Num 2 Streaks: %s' % len(streaks_2))
        print('Streak 0 Avg: %s' % round(average(streaks_0), 3))
        print('Streak 1 Avg: %s' % round(average(streaks_1), 3))
        print('Streak 2 Avg: %s' % round(average(streaks_2), 3))
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

        with open('patterns_outfile_0001.txt', 'a') as f_:
            f_.write(str(guess_list) + '\n')

while True:
    starttime = datetime.now()
    outfile_init()
    csv_read()
    for i in range(0, 15):
        sys.stdout.write('\r' + str(15 - i) + ' Seconds Left Until Next Loop')
        time.sleep(1)
    print('\n\n')
