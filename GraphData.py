import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.ticker as ticker
import datetime
from datetime import timedelta
import math
import os

from Configuration import Configuration

config = Configuration('configuration.json')

night_label = 'night'
day_label = 'day'
group_label = 'group'
day_color = '#ffcc00'
night_color = '#000000'


def get_datetime_from_date_and_timestamp(date_time, time_string, use_seconds=True):
    format_string = "%Y-%m-%d %H:%M" + (":%S" if use_seconds else "")
    return datetime.datetime.strptime(str(date_time) + " " + time_string, format_string)

def get_bulked_out_labels_for_timestamps(timestamp_list):
    x_labels = []
    current_date = datetime.date.today()
    previous_datetime = datetime.datetime.min
    last_label = None

    for index, val in enumerate(timestamp_list):
        current_datetime = get_datetime_from_date_and_timestamp(current_date, val[0])
        if current_datetime < previous_datetime and last_label is not None:
            current_date = current_date + timedelta(days=1)
            current_datetime = get_datetime_from_date_and_timestamp(current_date, val[0])
        night_start_today = get_datetime_from_date_and_timestamp(current_date, config.nightStartTime, False)
        morning_start_today = get_datetime_from_date_and_timestamp(current_date, config.dayStartTime, False)
        if night_start_today < morning_start_today:
            night_start_today = get_datetime_from_date_and_timestamp(current_date + timedelta(days=1), config.nightStartTime, False)
        is_night = current_datetime > night_start_today or current_datetime < morning_start_today
        is_day = is_night is False
        is_night_to_day_change = (last_label == night_label or last_label is None) and is_day
        is_day_to_night_change = (last_label == day_label or last_label is None) and is_night
        is_day_night_cycle_change = last_label is None or is_day_to_night_change or is_night_to_day_change
        current_label = day_label if is_day else night_label
        if is_day_night_cycle_change:
            previous_datetime = current_datetime
            last_label = current_label
        x_labels.append(current_label)

    return x_labels

import numpy, scipy.optimize

def fit_sin(tt, yy):
    #from stack overflow
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = numpy.array(tt)
    yy = numpy.array(yy)
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*numpy.pi)
    fitfunc = lambda t: A * numpy.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}

def create_sub_plot_data_set(color, label, isErrorPlot=False):

    file = pd.ExcelFile(config.outputFileName)
    df_for_group = file.parse(label)
    timestamp_list = df_for_group[[config.timestampColumn]].values.tolist()
    x_labels = get_bulked_out_labels_for_timestamps(timestamp_list)
    timestamp_list_len = len(timestamp_list)
    timestamp_range = range(timestamp_list_len)
    std_error_column = config.xAxisColumn + "_standard_error"
    plt.ylim(config.yAxisStart, config.yAxisLimit)
    if isErrorPlot:
        markers, caps, bars = plt.errorbar(y=df_for_group[config.xAxisColumn],
                     x=timestamp_range,
                     yerr=df_for_group[std_error_column],
                     label=label,
                     color=color,
                     errorevery=1,
                     elinewidth=1,
                     capsize=2)
        [bar.set_alpha(config.errorBarTransparency) for bar in bars]
        [cap.set_alpha(config.errorBarTransparency) for cap in caps]
    else:
        plt.plot(df_for_group[config.xAxisColumn], label=label, color=color)

    if config.isFittingCosineCurve:
        result = fit_sin(timestamp_range, df_for_group[config.xAxisColumn].values)
        plt.plot(timestamp_range, result["fitfunc"](timestamp_range), "r-", label="y fit curve", linewidth=2)
    plt.xticks(timestamp_range, x_labels)

def get_non_blank_labels_with_indexes(x_ticks):
    label_index_dict = {}
    for index, x_tick in enumerate(x_ticks):
        x_tick_string = x_tick.get_text()
        if x_tick_string == day_label or x_tick_string == night_label:
            label_index_dict[index/2] = x_tick_string
    return label_index_dict

def get_night_and_day_label_count(x_ticks):
    label_index_dict = {}
    previous_label = x_ticks[0]
    label_index = 0
    for index, x_tick in enumerate(x_ticks):
        current_label = x_tick
        is_label_change = previous_label != current_label
        if is_label_change:
            label_index = label_index + 1
        if len(label_index_dict) <= label_index:
            label_index_dict[label_index] = 0
        label_index_dict[label_index] = label_index_dict[label_index] + 1
        previous_label = current_label
    return label_index_dict

def create_xticks():

    plt.tick_params(axis="x", direction="out", width=6, length=10)
    x_tick_lines = plt.gca().get_xticklines()
    for x_tick_line in x_tick_lines:
        x_tick_line.set_visible(False)
    x_ticks = plt.gca().get_xaxis().get_majorticklabels()
    x_tick_labels = []
    for x_tick_text_object in x_ticks:
        x_tick_text_object.set_visible(False)
        x_tick_labels.append(x_tick_text_object.get_text())

    label_counts = get_night_and_day_label_count(x_tick_labels)

    x = [0]
    x_minor_values = []
    x_minor_labels = []
    current_day = config.startDay

    color_collection = []
    current_color = day_color if x_tick_labels[0] == day_label else night_color
    previous_color = None

    for index, label_count in enumerate(label_counts.values()):
        color_collection.append(current_color)

        next_x_tick_value = label_count + x[index]
        x.append(next_x_tick_value)

        next_x_minor_tick_value = x[index]

        #day transition
        if current_color == day_color and (previous_color is None or previous_color == night_color):
            x_minor_labels.append(current_day)
            x_minor_values.append(next_x_minor_tick_value)
            current_day = current_day + 1

        previous_color = current_color
        current_color = night_color if current_color == day_color else day_color

    y = np.zeros(len(label_counts) + 1)

    ax = plt.gca()
    ax.xaxis.set_minor_locator(ticker.FixedLocator(x_minor_values))
    ax.xaxis.set_minor_formatter(ticker.FixedFormatter(x_minor_labels))

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, colors=color_collection, linewidth=5,
                        transform=ax.get_xaxis_transform(), clip_on=False)
    ax.add_collection(lc)
    ax.spines["bottom"].set_visible(False)
    ax.set_xticks(x)
    ax.set_ylabel(config.yAxisLabel)
    ax.set_xlabel(config.xAxisLabel)
    ax.legend(loc="upper right")
    #print(label_counts)


def create_plots_for_single_fish():

    group_size = config.numberOfCells / len(config.groups)
    well_numbers = [i for i in range(1, config.numberOfCells + 1) if i not in config.wellsToExclude]
    for well_number in well_numbers:
        plt.cla()
        current_group_index = math.floor((well_number - 1) / group_size)
        group = config.groups[current_group_index]
        label = group["label"] + " well number " + str(well_number)
        create_sub_plot_data_set(group["color"], label)
        create_xticks()
        plt.title(group["label"] + " well number " + str(well_number))
        plt.margins(0)

        output_directory = "OutputGraphs"

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)


        plt.savefig(output_directory + "/" + label)

def create_combined_plots_for_groups():
    for group_number in range(1, len(config.groups) + 1):
        group = config.groups[group_number - 1]
        create_sub_plot_data_set(group["color"], group["label"], config.isShowingStandardError)

    create_xticks()
    plt.margins(0)
    plt.show()

def create_seperate_plots_for_groups():
    for group_number in range(1, len(config.groups) + 1):
        plt.cla()
        group = config.groups[group_number - 1]
        create_sub_plot_data_set(group["color"], group["label"], config.isShowingStandardError)
        create_xticks()
        plt.margins(0)
        plt.show()

def create_plots_for_fish_groups():
    if config.isShowingSingleGraphPerGroup:
        create_seperate_plots_for_groups()
    else:
        create_combined_plots_for_groups()

def create_plots():
    if config.isShowingIndividualFish:
        create_plots_for_single_fish()
    else:
        create_plots_for_fish_groups()

def Main():
   pass

if __name__ == "__main__":
    Main()