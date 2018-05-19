import pandas as pd
import csv
from Configuration import Configuration

config = Configuration('configuration.json')

def generate_distance_sums_for_individual_fish():
    if config.isShowingIndividualFish is False:
        return #only for the single fish case
    file = pd.ExcelFile(config.outputFileName)
    sheet_names = file.sheet_names
    sums = []
    for index, sheet_name in enumerate(sheet_names):
        df_for_fish = file.parse(sheet_name)
        if (index + 1) not in config.wellsToExclude:
            sums.append({"name": sheet_name, "sum": df_for_fish[config.distanceColumn].sum()})
    file_name = config.startDate + " distance sums.csv"
    with open(file_name, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
        for sum in sums:
            wr.writerow([sum["name"], sum["sum"]])

def Main():
    pass

if __name__ == "__main__":
    Main()