import pandas as pd
import csv
from Configuration import Configuration

config = Configuration('configuration.json')

def create_cronos_fit_formatted_file():
    if config.isShowingIndividualFish:
        return #only for the average case
    file = pd.ExcelFile(config.outputFileName)
    sheet_names = file.sheet_names
    for sheet_name in sheet_names:
        df_for_group = file.parse(sheet_name)
        file_name = config.startDate + " " + sheet_name + ".csv"
        with open(file_name, 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            wr.writerow([config.startDate])
            wr.writerow(["exp"])
            for index, row in df_for_group.iterrows():
                wr.writerow([index + 1, row[config.xAxisColumn]])

def Main():
    pass

if __name__ == "__main__":
    Main()