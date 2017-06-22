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
from time import sleep
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import layout
from bokeh import models
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
bokeh_totallines = []
bokeh_trendline = []
bokeh_trendline_smoothed = []
bokeh_trendline_smoothed_2 = []
btl_3 = []
btl_4 = []
btl_5 = []
btl_6 = []
btl_7 = []


def time_():
    utc = arrow.utcnow()
    pst = utc.to('US/Pacific')
    return pst.format()


def csv_init():
    with open('Graphing_accuracy_data_0003.csv', 'w') as f:
        csv.writer(f).writerow(csv_headers)


def trend_line(frlist=None, tolist=None):
    try:
        p1 = frlist[-2]
        p2 = frlist[-1]
        tolist.append((p1 + p2) / 2)
    except IndexError:
        pass


def csv_write(returned):
    """ Writes data to a csv file, essentially the output of the algorithm
    :param:
    returned (list) - The output of the guess algorithm. Returned from patterns.py
    """
    del values[:]
    global entryno_counter
    global run_count
    global highest_accuracy
    global lowest_accuracy
    global total_lines
    global avg_accuracy
    entryno_counter += 1
    run_count += 1
    with open('Graphing_accuracy_data_0003.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        values.append(entryno_counter)
        values.append(returned)
        values.append(str(returned[1][0] + returned[1][1]))
        values.append(str(time_()))

        bokeh_x.append(run_count)
        bokeh_y.append(returned[0])
        bokeh_totallines.append(returned[3])

        total_lines = returned[3]

        avg_accuracy = float(statistics.mean(bokeh_y))

        if len(bokeh_y) > 12:
            trend_line(bokeh_y, bokeh_trendline)
            trend_line(bokeh_trendline, bokeh_trendline_smoothed)
            trend_line(bokeh_trendline_smoothed, bokeh_trendline_smoothed_2)
            trend_line(bokeh_trendline_smoothed_2, btl_3)
            trend_line(btl_4, btl_5)
            trend_line(btl_5, btl_6)

        if returned[0] > highest_accuracy:
            highest_accuracy = returned[0]

        if returned[0] < lowest_accuracy:
            lowest_accuracy = returned[0]

        print(len(bokeh_y))
        print(len(bokeh_trendline))
        print(len(bokeh_trendline_smoothed))
        print(len(bokeh_trendline_smoothed_2))
        print(len(btl_3))

        writer.writerow(values)


def bokeh():
    """ Makes the bokeh graph for Accuracy - Guess alg runs
    :return:
    """
    try:
        file_name = ''.join(['Accuracy_graph_6_' + str(run_count) + '.html'])

        source = models.ColumnDataSource(data=dict(x=bokeh_x, y=bokeh_y,
                                  trend=bokeh_trendline_smoothed_2,
                                  smoothtrend=btl_4,
                                  smoothed2=btl_6))
        hover = models.HoverTool(tooltips=[
            ('Index', '$index'),
            ('Accuracy', '@y' + '%'),
            ('Run Number', '@x')])
        tools = [models.PanTool(), models.BoxSelectTool(), models.WheelZoomTool(),
                 hover, models.SaveTool(), models.ResizeTool()]
        # HTML For data description below graph
        div = Div(text=""" <b>Guess Accuracy Graph</b>. <br /><br />
        Highest Accuracy On Graph - <nobr><b><i>""" + str(highest_accuracy) + """</i></b> % </nobr><br />""" + """
        Lowest Accuracy On Graph  - <nobr><b><i>""" + str(lowest_accuracy) + """</i></b> % </nobr><br />""" + """
        Average Accuracy - <nobr><b><i>""" + str(avg_accuracy)[:5] + """</i></b> % </nobr><br />""" + """
        Total Lines Used - <nobr><b><i>""" + str(total_lines) + """</i></b></nobr><br />"""
                  , width=200, height=100)

        p = figure(plot_width=1000, plot_height=450, title='Accuracy By Algorithm Run',
                   tools=tools, toolbar_location='above')
        scatter = p.circle(x='x', y='y', fill_color='white', size=8, source=source)
        line = p.line(x='x', y='y', line_width=2, line_alpha=0.5, source=source,
                      line_color='blue')
        t_line = p.line(x='x', y='trend', line_width=2, line_alpha=0.5,
                        source=source, line_color='red', line_dash='dashed',
                        legend='Trend Line')
        st_line = p.line(x='x', y='smoothtrend', line_width=2, line_alpha=0.5,
                         source=source, line_color='red', line_dash='dashed')
        st_line_2 = p.line(x='x', y='smoothed2', line_width=2, line_alpha=0.5,
                           source=source, line_color='red', line_dash='dashed')
        p.yaxis.axis_label = 'Accuracy %'
        p.xaxis.axis_label = '# Of guess algorithm runs'

        # JS for button callback handling
        code = '''object.visible = toggle.active'''

        callback = models.CustomJS.from_coffeescript(code=code, args={})
        toggle_data_line = Toggle(label='Toggle Line', button_type='success',
                                  callback=callback)
        callback.args = {'toggle': toggle_data_line, 'object': line}
        print('Line Callback Set...')

        callback2 = models.CustomJS.from_coffeescript(code=code, args={})
        toggle_trend_line = Toggle(label='Toggle Trend Line',
                                   button_type='success', callback=callback2)
        callback2.args = {'toggle': toggle_trend_line, 'object': t_line}
        print('Trend Line Callback Set...')

        callback2 = models.CustomJS.from_coffeescript(code=code, args={})
        toggle_scatter = Toggle(label='Toggle Data Points',
                                button_type='success', callback=callback2)
        callback2.args = {'toggle': toggle_scatter, 'object': scatter}
        print('Scatter Callback Set...')

        callback2 = models.CustomJS.from_coffeescript(code=code, args={})
        toggle_st_line = Toggle(label='Toggle Smoothing 1',
                                button_type='success', callback=callback2)
        callback2.args = {'toggle': toggle_st_line, 'object': st_line}
        print('Scatter Callback Set...')

        callback2 = models.CustomJS.from_coffeescript(code=code, args={})
        toggle_st_line_2 = Toggle(label='Toggle Smoothing 2',
                                  button_type='success', callback=callback2)
        callback2.args = {'toggle': toggle_st_line_2, 'object': st_line_2}
        print('Scatter Callback Set...')

        output_file(file_name)
        show(layout([p],
                    [toggle_data_line, toggle_scatter],
                    [toggle_trend_line, toggle_st_line, toggle_st_line_2],
                    [div]))

        save(layout([p],
                    [toggle_data_line, toggle_scatter],
                    [toggle_trend_line, toggle_st_line, toggle_st_line_2],
                    [div]))

    except RuntimeError as e:
        print(e)
        pass

while True:
    print('start')
    returned_list = patterns.csv_read()
    csv_write(returned_list)
    print('done')
    print(run_count)
    if run_count % 15 == 0:
        print('running bokeh')
        bokeh()
