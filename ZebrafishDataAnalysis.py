import ProcessData
import GraphData
import FormatDataForClockLab
from Configuration import Configuration

def Main():

    config = Configuration('configuration.json')

    if config.isProcessingDataFirst:
        ProcessData.process_data_files()

    if config.isGeneratingGraph:
        GraphData.create_plots()

    if config.isGeneratingClocklabFiles:
        FormatDataForClockLab.create_clock_lab_formatted_file()

if __name__ == "__main__":
    Main()