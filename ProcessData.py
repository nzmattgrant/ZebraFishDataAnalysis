import pandas as pd
import Configuration
#Todo put the different groups in different excel sheets
config = {}

def create_averaged_row(rows_to_combine, group_num):
    if len(rows_to_combine) < 1:
        return None

    total_lardur = 0
    total_lardist = 0
    sttime = rows_to_combine[0]['sttime']
    for row in rows_to_combine:
        total_lardur += row['lardur']
        total_lardist += row['lardist']

    return_row = {
        'group': group_num,
        'lardur': total_lardur / len(rows_to_combine),
        'lardist': total_lardist / len(rows_to_combine),
        'sttime': sttime.strftime('%H:%M:%S')
    }
    return return_row


def process_data_files(is_skipping_average):

    config = Configuration('configuration.json')

    file = pd.ExcelFile("96 well dist tracking day 5 LD 22-03-18.xlsx")
    df = file.parse("96 well dist tracking day 5 LD")
    df = df[df.index % 2 == 0].reset_index(drop=True)
    group_timeslice_rows = []
    averaged_rows = []
    group_num = 1
    for index, row in df.iterrows():
        group_timeslice_rows.append(row)
        group_size = config.numberOfCells / config.numberOfGroups
        if (index + 1) % (group_size) == 0:
            averaged_rows.append(create_averaged_row(group_timeslice_rows, group_num))
            group_timeslice_rows = []
            if group_num == config.numberOfGroups:
                group_num = 0
            group_num += 1

    output_df = pd.DataFrame(averaged_rows)

    writer = pd.ExcelWriter('Day 8.xlsx', engine='xlsxwriter', datetime_format='hh:mm:ss')
    output_df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

def Main():
    pass

if __name__ == "__main__":
    Main()