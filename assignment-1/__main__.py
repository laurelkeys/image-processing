import os.path
import argparse

class Technique:
    FLOYD_STEINBERG = "floyd_steinberg"
    STEVENSON_ARCE = "stevenson_arce"
    BURKES = "burkes"
    SIERRA = "sierra"
    STUCKI = "stucki"
    JARVIS_JUDICE_NINKE = "jarvis_judice_ninke"
    
    list_all = [FLOYD_STEINBERG, STEVENSON_ARCE, BURKES, SIERRA, STUCKI, JARVIS_JUDICE_NINKE]

def get_parser():
    parser = argparse.ArgumentParser(description='Implementations of dithering techniques for creating halftone images.')
    parser.add_argument('image', type=str, 
                        help='The name of the input (original) image')
    parser.add_argument('--input_folder', '-i', type=str, default="i", 
                        help='The folder path for the input (original) image')
    parser.add_argument('--output_folder', '-o', type=str, default="o", 
                        help='The output folder path for the dithered image')
    parser.add_argument('--technique_index', '-t', type=int, choices=range(0, 7), 
                        help='The index of the dithering technique to be used, where: 0=floyd_steinberg, '
                             '1=stevenson_arce, 2=burkes, 3=sierra, 4=stucki, 5=jarvis_judice_ninke')
    parser.add_argument('--verbose', '-v', action="store_true", 
                        help='Increase verbosity')
    return parser

v_print = None
def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    if args.verbose:
        print(f"Technique: {Technique.list_all[args.technique_index] if args.technique_index else 'all'}")
        def __v_print(*args):
            print(args)
    else:
        __v_print = lambda *a: None
    
    global v_print
    v_print = __v_print

if __name__ == '__main__':
    main()