''' This is the main file for relative placement scoring. It will 
read the input files and make the necessary scoring.
'''

from Relative_Placement import Relative_Placements ## Does the heavy lifting
from scoring            import parse_input_file    ## for parsing shit

def main():
    import pprint, argparse
    pp = pprint.PrettyPrinter(indent=4)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',   nargs='?', type=argparse.FileType('r'),
                        help='use the given file as input')
    parser.add_argument('--files',  nargs='*', type=argparse.FileType('r'),
                        help='use multiple files as input')
    parser.add_argument('--scores', nargs='*', type=argparse.FileType('r'),
                        help='use multiple score files as input')
    parser.add_argument('--output', nargs='?', type=argparse.FileType('r'),
                        help='the output file for the program')
    parser.add_argument('--pprint', action='store_true',
                        help='pretty prints the output to stdout')

    args   = parser.parse_args()
    scores = parse_input_file(args.file)
    rp     = Relative_Placements(scores, 5, 3, False)

    print rp

if __name__ == '__main__': main()