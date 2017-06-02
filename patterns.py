"""
    File Name: patterns.py
    Author: Ari Madian
    Created: May 31, 2017  9:16AM
    Python Version: 3.6

    patterns.py - part of Machine-Learning Repo
    Repo: github.com/akmadian/Machine-Learning
"""

import csv
import time
from datetime import datetime
import os
import sys
import statistics

def average(streaks):
    streaks_without_zeros = [streak for streak in streaks if streak != 0]
    return statistics.mean(streaks_without_zeros)

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
    with open('COMMODITIES_GOLD_DATA_0006.csv', 'r') as f:
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
        if os.name == 'nt':
            os.system('cls')
        else:
            pass
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
        print('')
        time_delta = str(datetime.now() - starttime)[5:]
        print('Loop took: %s Seconds' % round(float(time_delta), 4))
        print('Done')

while True:
    starttime = datetime.now()
    csv_read()
    for i in range(0, 15):
        sys.stdout.write('\r' + str(15 - i) + ' Seconds Left Until Next Loop')
        time.sleep(1)
    print('\n\n')