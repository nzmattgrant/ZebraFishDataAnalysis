import pandas as pd
from os import listdir
from os.path import isfile, join
from Configuration import Configuration
import math
from scipy import stats
import numpy

config = Configuration('configuration.json')

#todo rename functions to be more descriptive
#reorder the way they are doing things
def create_averaged_row(rows_to_combine, group_num):
    if len(rows_to_combine) < 1:
        return None

    sttime = rows_to_combine[0][config.timeColumn]
    lardurs = [r[config.durationColumn] for r in rows_to_combine]
    lardists = [r[config.distanceColumn] for r in rows_to_combine]

    return_row = {
        'group': group_num,
        'lardur': numpy.mean(lardurs),
        'lardur_standard_error': stats.sem(lardurs),
        'lardist': numpy.mean(lardists),
        'lardist_standard_error': stats.sem(lardists),
        'sttime': sttime.strftime('%H:%M:%S')
    }
    return return_row


#todo combine the shared code (get rid of copy paste code)
def create_single_fish_row(row, well_number):

    total_lardur = row[config.durationColumn]
    total_lardist = row[config.distanceColumn]
    sttime = row[config.timeColumn]

    return_row = {
        'group': well_number,
        'lardur': total_lardur,
        'lardist': total_lardist,
        'sttime': sttime.strftime('%H:%M:%S')
    }
    return return_row


def check_is_well_exluded(index, number_of_wells):
    wells_to_be_skipped = config.wellsToExclude
    for well_number in wells_to_be_skipped:
        #wells to exclude contains the curent cell number
        if (index + 1) % number_of_wells == well_number:
            return True
    return False

def get_transormed_data_from_input_file_for_fish_groups(fileName):

    group_timeslice_rows = []
    averaged_rows = []
    group_num = 1

    file = pd.ExcelFile(config.inputFileDirectory + "/" + fileName)
    df = file.parse(config.inputFileSheetName)

    if config.isDroppingEverySecondRow:
        df = df[df.index % 2 == 0].reset_index(drop=True)

    for index, row in df.iterrows():

        group_size = config.numberOfCells / len(config.groups)
        is_group_end = (index + 1) % group_size == 0
        if check_is_well_exluded(index, config.numberOfCells) is False:
            group_timeslice_rows.append(row)
        if is_group_end:
            averaged_rows.append(create_averaged_row(group_timeslice_rows, group_num))
            group_timeslice_rows = []
            if group_num == len(config.groups):
                group_num = 0
            group_num += 1
    return averaged_rows



def get_transormed_data_from_input_file_for_individual_fish(fileName):

    rows = []

    file = pd.ExcelFile(config.inputFileDirectory + "/" + fileName)
    df = file.parse(config.inputFileSheetName)

    if config.isDroppingEverySecondRow:
        df = df[df.index % 2 == 0].reset_index(drop=True)

    for index, row in df.iterrows():
        if check_is_well_exluded(index, config.numberOfCells) is False:
            rows.append(create_single_fish_row(row, (index % config.numberOfCells) + 1))
    return rows


def process_data_files_for_fish_groups(input_files):
    data_rows = []

    for file in input_files:
        data_rows.extend(get_transormed_data_from_input_file_for_fish_groups(file))

    df = pd.DataFrame(data_rows)
    writer = pd.ExcelWriter(config.outputFileName, engine='xlsxwriter', datetime_format='hh:mm:ss')

    for index, group in enumerate(config.groups):
        df.loc[df["group"] == index + 1].reset_index(drop=True).to_excel(writer, sheet_name=group["label"])

    writer.save()

def process_data_files_individual_fish(input_files):
    data_rows = []

    for file in input_files:
        data_rows.extend(get_transormed_data_from_input_file_for_individual_fish(file))

    df = pd.DataFrame(data_rows)
    writer = pd.ExcelWriter(config.outputFileName, engine='xlsxwriter', datetime_format='hh:mm:ss')

    group_size = config.numberOfCells / len(config.groups)
    for well_number in range(1, config.numberOfCells + 1):
        current_group_index = math.floor((well_number - 1) / group_size)
        sheet_name = config.groups[current_group_index]["label"] + " well number " + str(well_number)
        df.loc[df["group"] == well_number].reset_index(drop=True).to_excel(writer, sheet_name=sheet_name)

    writer.save()

def process_data_files():

    input_files = [f for f in listdir(config.inputFileDirectory) if isfile(join(config.inputFileDirectory, f))]
    input_xlsx_files = [f for f in input_files if f.lower().endswith(".xlsx")]
    input_xlsx_files.sort()

    if config.isShowingIndividualFish:
        process_data_files_individual_fish(input_xlsx_files)
    else:
        process_data_files_for_fish_groups(input_xlsx_files)

    print("data processing step complete")


def Main():
    pass

if __name__ == "__main__":
    Main()