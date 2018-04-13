import ProcessData
import GraphData
from Configuration import Configuration

def Main():

    config = Configuration('configuration.json')

    if config.isProcessingDataFirst:
        ProcessData.process_data_files()

    if config.isGeneratingGraph:
        GraphData.create_plots()

if __name__ == "__main__":
    Main()