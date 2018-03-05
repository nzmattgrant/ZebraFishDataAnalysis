import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

def get_datetime_from_date_and_timestamp(date_time, time_string, use_seconds=True):
    format_string = "%Y-%m-%d %H:%M" + (":%S" if use_seconds else "")
    return datetime.datetime.strptime(str(date_time) + " " + time_string, format_string)

night_start_time_string = '21:00'
day_start_time_string = '05:00'
night_label = 'night'
day_label = 'day'
timestamp_column_label = 'sttime'
duration_column_label = 'lardur'
day_color = '#919191'
night_color = '#000000'

file = pd.ExcelFile("pandas_simple.xlsx")
df = file.parse("Sheet1")
#df['sttime'] = pd.to_timedelta(df['sttime'])
group_1_df = df.loc[df['group'] == 1].reset_index(drop=True)
# group_2_df = df.loc[df['group'] == '2']
# group_3_df = df.loc[df['group'] == '3']

for index, row in group_1_df[[duration_column_label, timestamp_column_label]].iterrows():
    print(row[duration_column_label])
    print(row[timestamp_column_label])
    print(type(row[timestamp_column_label]))

x_labels = []
current_date = datetime.date.today()
previous_datetime = datetime.datetime.min
first_label = None
last_label = None
timestamp_list = group_1_df[[timestamp_column_label]].values.tolist()
change_label_indexes = []

#def find_current_x_lable

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
    if last_label is None:
        first_label = current_label
    if is_day_night_cycle_change:
        change_label_indexes.append(index)
        previous_datetime = current_datetime
        last_label = current_label
    x_labels.append(current_label if is_day_night_cycle_change else "")
sttime_len = len(timestamp_list)
sttime_range = range(sttime_len)
plt.plot(group_1_df[duration_column_label])
plt.xticks(sttime_range, x_labels, rotation=70)
plt.tick_params(axis="x", direction="out", width=6, length=10)
x_tick_lines = plt.gca().get_xticklines()
isDay = first_label == day_label
for index, row in enumerate(x_tick_lines):
    useful_line_index = index/2
    #for some reason there is a dummy line every second line that adds nothing
    if index != 0 and change_label_indexes.__contains__(useful_line_index):
        isDay = not isDay
    if isDay:
        row.set_color(day_color)
    else:
        row.set_color(night_color)

plt.show()

# group_1_x_axis = pd.DataFrame(group_1_df, columns=['sttime'])
# group_1_y_axis = pd.DataFrame(group_1_df, columns=['lardur'])
# group_1_df.plot(kind ='line', xticks=group_1_x_axis, yticks=group_1_y_axis)
