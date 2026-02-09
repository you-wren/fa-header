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
from typing import List, NamedTuple


class Args(NamedTuple):
    """Command-line args"""

    out_dir: str
    files: List[str]


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Add filename to headers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "file", metavar="str", nargs="+", help="Input file(s)"
    )

    parser.add_argument(
        "-o",
        "--out-dir",
        help="Output directory name",
        metavar="str",
        default="with_headers",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir)

    return Args(files=args.file, out_dir=args.out_dir)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    for i, file in enumerate(args.files, start=1):
        if not os.path.isfile(file):
            print(f'Invalid file "{args.file}"', file=sys.stderr)
            continue

        print(f"{i:3}: {file}")
        base, ext = os.path.splitext(os.path.basename(file))
        fname = re.sub(".cutforrev-t$", "", base)
        out_file = os.path.join(args.out_dir, fname + ext)
        out_fh = open(out_file, "wt")
        file_format = "fastq" if ext in [".fq", ".fastq"] else "fasta"

        for rec in SeqIO.parse(file, file_format):
            new_id = "_".join([fname, rec.id])
            out_fh.write(f">{new_id}\n{rec.seq}\n")

        out_fh.close()

    print(f'Done, see output in "{args.out_dir}"')


# --------------------------------------------------
if __name__ == "__main__":
    main()
