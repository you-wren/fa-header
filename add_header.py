#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-08
Purpose: Add filename to headers
"""

import argparse
import os
import re
import sys
from Bio import SeqIO


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Add filename to headers',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='str',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help='Input file(s)')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory name',
                        metavar='str',
                        type=str,
                        default='with_headers')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    out_dir = args.outdir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    for i, file in enumerate(args.file, start=1):
        print(f'{i:3}: {file.name}')
        base, ext = os.path.splitext(os.path.basename(file.name))
        fname = re.sub('.cutforrev-t$', '', base)
        out_file = os.path.join(out_dir, fname + ext)
        out_fh = open(out_file, 'wt')

        for rec in SeqIO.parse(file, 'fasta'):
            new_id = '_'.join([fname, rec.id])
            out_fh.write(f'>{new_id}\n{rec.seq}\n')

        out_fh.close()

    print(f'Done, see output in "{out_dir}"')

# --------------------------------------------------
if __name__ == '__main__':
    main()
