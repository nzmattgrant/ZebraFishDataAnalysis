import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#load up the data from the cleaned up excel sheet
#create a data frame for each group
#converting the times to objects as you go
#put each stream of data into a matplotlib graph

file = pd.ExcelFile("pandas_simple.xlsx")
df = file.parse("Sheet1")
#df['sttime'] = pd.to_timedelta(df['sttime'])
group_1_df = df.loc[df['group'] == 1]
# group_2_df = df.loc[df['group'] == '2']
# group_3_df = df.loc[df['group'] == '3']

for index, row in group_1_df[['lardur', 'sttime']].iterrows():
    print(row['lardur'])
    print(row['sttime'])
    print(type(row['sttime']))
xlabels = []
for index, val in group_1_df[['sttime']].iterrows():
    xlabels.append(str(val['sttime']) if index % 18 == 0 else "")
plt.plot(range(len(group_1_df['sttime'])), group_1_df['lardur'])
plt.xticks(range(len(xlabels)), xlabels, rotation=70)
plt.show()
# group_1_x_axis = pd.DataFrame(group_1_df, columns=['sttime'])
# group_1_y_axis = pd.DataFrame(group_1_df, columns=['lardur'])
# group_1_df.plot(kind ='line', xticks=group_1_x_axis, yticks=group_1_y_axis)
