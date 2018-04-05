import argparse
import GraphData

def Main():

    parser = argparse.ArgumentParser(description='Graph some fish data')
    parser.add_argument('--skipaverage', type=bool, nargs='+',
                   help='skips the averaging and creates a graph for each fish')

    args = parser.parse_args()

    is_skipping_average = False if args.skipaverage is None else args.skipaverage

    GraphData.create_plots(is_skipping_average)

if __name__ == "__main__":
    Main()