#!/usr/bin/env python3
# Author:   Michael E. Rose <michael.ernst.rose@gmail.com>
"""Creates a long file of yearly Journal Impact Factors."""

from glob import glob

import pandas as pd

SOURCE_FOLDER = "./raw_data/"
TARGET_FILE = "./compiled/Scimago_JIFs.csv"


def read_file(fname):
    """Read individual file with Journal Impact Factors."""
    df = pd.read_excel(fname, index_col=2)
    df = df[df['Type'] == 'journal']
    df['year'] = fname.split()[1]
    return df[['year', 'SJR', 'H index', 'Cites / Doc. (2years)']]


def main():
    files = sorted(glob(SOURCE_FOLDER + "*.xlsx"))
    out = pd.concat([read_file(f) for f in files], axis=0)
    out = out.rename(columns={'H index': 'h-index',
                              'Cites / Doc. (2years)': 'avg_citations'})
    out.to_csv(TARGET_FILE)


if __name__ == '__main__':
    main()
