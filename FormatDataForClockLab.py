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
        date_format = "%m-%d-%y %I:%M:%S%p"
        formatted_date = date_time.strftime(date_format).lower()
        file.write(formatted_date + "  " + '{0:0.3f}'.format(value).zfill(9) + "\n")

def write_to_file(file_name, df_for_group):
    with open(file_name, 'w') as file:
        file.write('# COLUMN      ID                      CHANNEL             DATATYPE                UNITS\n')
        file.write('# 1           ' + file_name + '   1                   Distance                mm\n')
        file.write("\n")
        file.write("START TIME:\n")
        write_file_lines(file, df_for_group)

def create_clock_lab_formatted_file():
    file = pd.ExcelFile(config.outputFileName)
    sheet_names = file.sheet_names
    for sheet_name in sheet_names:
        df_for_group = file.parse(sheet_name)
        file_name = config.startDate + " " + sheet_name + ".bbcl"
        write_to_file(file_name, df_for_group)

def Main():
    pass

if __name__ == "__main__":
    Main()