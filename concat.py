#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-08
Purpose: Concat sequence files
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
        description='Concat sequence files, fix headers',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='str',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help='Input file(s)')

    parser.add_argument('-o',
                        '--outfile',
                        help='Output file name',
                        metavar='str',
                        type=str,
                        default='out.fa')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    out_fh = open(args.outfile, 'wt')

    for i, file in enumerate(args.file, start=1):
        print(f'{i:3}: {file.name}')
        fname = re.sub('.cutforrev-t.fasta$', '', file.name)

        for rec in SeqIO.parse(file, 'fasta'):
            new_id = '_'.join([fname, rec.id])
            out_fh.write(f'>{new_id}\n{rec.seq}\n')

    out_fh.close()
    print('Done')

# --------------------------------------------------
if __name__ == '__main__':
    main()
