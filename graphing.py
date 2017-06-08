"""
    File Name: graphing.py
    Author: Ari Madian
    Created: June 6, 2017 12:21 PM
    Python Version: 3.6

    graphing.py - Part of Machine-Learning Repo
    Repo: github.com/akmadian/Machine-Learning
"""

import csv
import arrow
import statistics
from GOLD import patterns
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import layout
from bokeh.models import HoverTool, PanTool, ResizeTool, WheelZoomTool, SaveTool, BoxSelectTool, CustomJS, ColumnDataSource
from bokeh.models.widgets import Toggle, Div

values = []
csv_headers = ('entryno.', 'accuracy/problist/guesslist/toline',
               'lines_ava', 'time')
entryno_counter = 0
run_count = 0
highest_accuracy = 0
lowest_accuracy = 100
avg_accuracy = 0
total_lines = 0
bokeh_x = []
bokeh_y = []
bokeh_uod = []


def time_():
    utc = arrow.utcnow()
    pst = utc.to('US/Pacific')
    return pst.format()


def csv_init():
    with open('Graphing_accuracy_data_0002.csv', 'w') as f:
        csv.writer(f).writerow(csv_headers)


def csv_write(returned):
    del values[:]
    global entryno_counter
    global run_count
    global highest_accuracy
    global lowest_accuracy
    global total_lines
    global avg_accuracy
    entryno_counter += 1
    run_count += 1
    with open('Graphing_accuracy_data_0002.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        values.append(entryno_counter)
        values.append(returned)
        values.append(str(returned[1][0] + returned[1][1]))
        values.append(str(time_()))

        bokeh_x.append(run_count)
        bokeh_y.append(returned[0])

        total_lines = returned[3]

        avg_accuracy = float(statistics.mean(bokeh_y))

        if returned[0] > highest_accuracy:
            highest_accuracy = returned[0]

        if returned[0] < lowest_accuracy:
            lowest_accuracy = returned[0]

        writer.writerow(values)


def bokeh():
    try:
        file_name = ''.join(['Accuracy_graph_5_' + str(run_count) + '.html'])

        source = ColumnDataSource(data=dict(x=bokeh_x, y=bokeh_y))

        hover = HoverTool(tooltips=[
            ('Index', '$index'),
            ('Accuracy', '@y' + '%'),
            ('Run Number', '@x'), ])

        TOOLS = [PanTool(), BoxSelectTool(), WheelZoomTool(), hover, SaveTool(), ResizeTool()]
        p = figure(plot_width=1200, plot_height=450, title='Accuracy By Algorithm Run', tools=TOOLS)

        # HTML For data description below graph
        div = Div(text=""" <b>Guess Accuracy Graph</b>. <br /><br />
        Highest Accuracy On Graph - <nobr><b><i>""" + str(highest_accuracy) + """</i></b> % </nobr><br />""" + """
        Lowest Accuracy On Graph  - <nobr><b><i>""" + str(lowest_accuracy) + """</i></b> % </nobr><br />""" + """
        Average Accuracy - <nobr><b><i>""" + str(avg_accuracy) + """</i></b> % </nobr><br />""" + """
        Total Lines Used - <nobr><b><i>""" + str(total_lines) + """</i></b></nobr><br />"""
                  , width=200, height=100)

        p.circle(x='x', y='y', fill_color='white', size=8, source=source)
        line = p.line(x='x', y='y', line_width=2, line_alpha=0.5, source=source)

        p.yaxis.axis_label = 'Accuracy %'
        p.xaxis.axis_label = '# Of guess algorithm runs'

        # JS for button callback handling
        code = '''object.visible = toggle.active'''
        callback = CustomJS.from_coffeescript(code=code, args={})
        toggle = Toggle(label='Toggle Line', button_type='success', callback=callback)
        callback.args = {'toggle': toggle, 'object': line}

        output_file(file_name)

        show(layout([p], [div, toggle]))
        save(layout([p], [div, toggle]))
    except RuntimeError:
        pass

while True:
    print('start')
    returned_list = patterns.csv_read()
    csv_write(returned_list)
    print('done')
    print(run_count)
    if run_count % 100 == 0:
        print('running bokeh')
        bokeh()
