import pandas as pd
import datetime
from datetime import timedelta
from dateutil import parser
from Configuration import Configuration

config = Configuration('configuration.json')

#todo move to util function
def get_datetime_from_date_and_timestamp(date_time, time_string, use_seconds=True):
    format_string = "%Y-%m-%d %H:%M" + (":%S" if use_seconds else "")
    return datetime.datetime.strptime(str(date_time) + " " + time_string, format_string)

def write_file_lines(file, df):
    current_date = parser.parse(config.startDate)
    previous_date_time = current_date
    for index, row in df.iterrows():
        date_time = get_datetime_from_date_and_timestamp(current_date.date(), row[config.timestampColumn])
        if date_time < previous_date_time:
            current_date = current_date + timedelta(days=1)
            date_time = get_datetime_from_date_and_timestamp(current_date.date(), row[config.timestampColumn])
        previous_date_time = date_time
        value = row[config.xAxisColumn]
        date_format = "%d-%m-%y %I:%M:%S%p"
        formatted_date = date_time.strftime(date_format).lower()
        file.write(formatted_date + "  " + str(value) + "\n")

def create_clock_lab_formatted_file():
    if config.isShowingIndividualFish:
        return

    for group in config.groups:
        file = pd.ExcelFile(config.outputFileName)
        label = group["label"]
        df_for_group = file.parse(label)
        file_name = config.startDate + " " + label + ".bbcl"
        #todo change the distance part to be dynamic
        with open(file_name, 'w') as file:
            file.write('# COLUMN      ID                      CHANNEL             DATATYPE                UNITS\n')
            file.write('# 1           ' + file_name + '   1                   Distance                mm\n')
            file.write("\n")
            file.write("START TIME:\n")
            write_file_lines(file, df_for_group)

def Main():
    pass

if __name__ == "__main__":
    Main()