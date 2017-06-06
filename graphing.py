"""
    File Name: graphing.py
    Author: Ari Madian
    Created: June 6, 2017 12:21 PM
    Python Version: 3.6

    graphing.py - Part of Machine-Learning Repo
    Repo: github.com/akmadian/Machine-Learning
"""

import matplotlib.pyplot as plt
import csv
import arrow
import time
from GOLD import patterns

values = []
csv_headers = ('entryno.', 'accuracy/problist/guesslist/toline',
               'lines_ava', 'time')
entryno_counter = 0
run_count = 0
mpl_x = []
mpl_y = []


def time_():
    utc = arrow.utcnow()
    pst = utc.to('US/Pacific')
    return pst.format()


def csv_init():
    with open('Graphing_accuracy_data_0001.csv', 'w') as f:
        csv.writer(f).writerow(csv_headers)


def csv_write(returned):
    del values[:]
    global entryno_counter
    global run_count
    entryno_counter += 1
    run_count += 1
    with open('Graphing_accuracy_data_0001.csv', 'a') as f:
        writer = csv.writer(f)
        values.append(entryno_counter)
        values.append(returned)
        values.append(str(returned[1][0] + returned[1][1]))
        values.append(str(time_()))

        mpl_x.append(run_count)
        mpl_y.append(returned[0])

        writer.writerow(values)


def mpl():
    file_name = ''.join(['Accuracy_graph_2_' + str(run_count) + '.png'])
    plt.plot(mpl_x, mpl_y)
    plt.scatter(mpl_x, mpl_y)
    plt.xlabel('Evaluation Num')
    plt.ylabel('Accuracy')
    plt.savefig(file_name, dpi=200)


csv_init()
while True:
    print('start')
    returned_list = patterns.csv_read()
    csv_write(returned_list)
    mpl()
    print('done')
    time.sleep(5)




