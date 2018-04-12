import pandas as pd
from os import listdir
from os.path import isfile, join
from Configuration import Configuration

config = Configuration('configuration.json')

def create_averaged_row(rows_to_combine, group_num):
    if len(rows_to_combine) < 1:
        return None

    total_lardur = 0
    total_lardist = 0
    sttime = rows_to_combine[0][config.timeColumn]
    for row in rows_to_combine:
        total_lardur += row[config.durationColumn]
        total_lardist += row[config.distanceColumn]

    return_row = {
        'group': group_num,
        'lardur': total_lardur / len(rows_to_combine),
        'lardist': total_lardist / len(rows_to_combine),
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

def process_data_for_fish_groups(fileName):

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

def process_data_for_individual_fish(fileName):
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

def process_data_files():

    input_files = [f for f in listdir(config.inputFileDirectory) if isfile(join(config.inputFileDirectory, f))]
    input_xlsx_files = [f for f in input_files if f.lower().endswith(".xlsx")]
    input_xlsx_files.sort()

    data_rows = []

    for file in input_xlsx_files:
        if config.isShowingIndividualFish:
            data_rows.extend(process_data_for_individual_fish(file))
        else:
            data_rows.extend(process_data_for_fish_groups(file))

    output_df = pd.DataFrame(data_rows)
    writer = pd.ExcelWriter(config.outputFileName, engine='xlsxwriter', datetime_format='hh:mm:ss')
    output_df.to_excel(writer, sheet_name=config.outputFileSheetName)
    writer.save()

def Main():
    pass

if __name__ == "__main__":
    Main()