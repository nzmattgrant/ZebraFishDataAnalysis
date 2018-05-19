import ProcessData
import GraphData
import FormatDataForClockLab
import FormatDataForChronosFit
import DataFormatter
from Configuration import Configuration

def Main():

    config = Configuration('configuration.json')

    if config.isProcessingDataFirst:
        ProcessData.process_data_files()

    if config.isGeneratingGraph:
        GraphData.create_plots()

    if config.isGeneratingClocklabFiles:
        FormatDataForClockLab.create_clock_lab_formatted_bulked_out_with_zeros_text_file()

    if config.isGeneratingChronosFitFile:
        FormatDataForChronosFit.create_cronos_fit_formatted_file()

    if config.isShowingIndividualFish and config.isGeneratingDistanceSums:
        DataFormatter.generate_distance_sums_for_individual_fish()

if __name__ == "__main__":
    Main()