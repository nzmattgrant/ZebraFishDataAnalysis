import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

night_start_time_string = '21:00'
day_start_time_string = '05:00'
night_label = 'night'
day_label = 'day'
group_label = 'group'
timestamp_column_label = 'sttime'
duration_column_label = 'lardur'
day_color = '#919191'
night_color = '#000000'

file = pd.ExcelFile("pandas_simple.xlsx")
df = file.parse("Sheet1")

def get_datetime_from_date_and_timestamp(date_time, time_string, use_seconds=True):
    format_string = "%Y-%m-%d %H:%M" + (":%S" if use_seconds else "")
    return datetime.datetime.strptime(str(date_time) + " " + time_string, format_string)

def get_labels_for_timestamps(timestamp_list):
    x_labels = []
    current_date = datetime.date.today()
    previous_datetime = datetime.datetime.min
    last_label = None

    for index, val in enumerate(timestamp_list):
        current_datetime = get_datetime_from_date_and_timestamp(current_date, val[0])
        if current_datetime < previous_datetime and last_label is not None:
            current_date = current_date + timedelta(days=1)
            current_datetime = get_datetime_from_date_and_timestamp(current_date, val[0])
        night_start_today = get_datetime_from_date_and_timestamp(current_date, night_start_time_string, False)
        morning_start_today = get_datetime_from_date_and_timestamp(current_date, day_start_time_string, False)
        is_night = current_datetime > night_start_today or current_datetime < morning_start_today
        is_day = is_night is False
        is_night_to_day_change = (last_label == night_label or last_label is None) and is_day
        is_day_to_night_change = (last_label == day_label or last_label is None) and is_night
        is_day_night_cycle_change = last_label is None or is_day_to_night_change or is_night_to_day_change
        current_label = day_label if is_day else night_label
        if is_day_night_cycle_change:
            previous_datetime = current_datetime
            last_label = current_label
        x_labels.append(current_label if is_day_night_cycle_change else "")

    return x_labels

def create_sub_plot_for_group(group_number):
    df_for_group = df.loc[df[group_label] == group_number].reset_index(drop=True)
    timestamp_list = df_for_group[[timestamp_column_label]].values.tolist()
    x_labels = get_labels_for_timestamps(timestamp_list)
    timestamp_list_len = len(timestamp_list)
    timestamp_range = range(timestamp_list_len)
    plt.plot(df_for_group[duration_column_label])
    plt.xticks(timestamp_range, x_labels)

def get_non_blank_labels_with_indexes(x_ticks):
    label_index_dict = {}
    for index, x_tick in enumerate(x_ticks):
        x_tick_string = x_tick.get_text()
        if x_tick_string == day_label:
            label_index_dict[index/2] = x_tick_string
    return label_index_dict

def create_plots():
    create_sub_plot_for_group(1)
    create_sub_plot_for_group(2)
    create_sub_plot_for_group(3)

    plt.tick_params(axis="x", direction="out", width=6, length=10)
    x_tick_lines = plt.gca().get_xticklines()
    x_ticks = plt.gca().get_xaxis().get_majorticklabels()
    index_dict = get_non_blank_labels_with_indexes(x_ticks)
    # get the first label in the list that is not ""
    is_day = len(index_dict) > 0 and index_dict[list(index_dict.keys())[0]] == day_label
    for index, row in enumerate(x_tick_lines):
        useful_line_index = index / 2
        # for some reason there is a dummy line every second line that adds nothing
        if index != 0 and index_dict.keys().__contains__(useful_line_index):
            is_day = not is_day
        if is_day:
            row.set_color(day_color)
        else:
            row.set_color(night_color)

    plt.show()

create_plots()
