# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from glob import glob

import pandas as pd
import os

SOURCE_FOLDER = "./raw_data/"
TARGET_FILE = "./compiled/Scimago_JIFs.csv"
dict1 = {"Agricultural and Biological Sciences" : 1100, 
              "Arts and Humanities" : 1200, 
              "Biochemistry, Genetics and Molecular Biology" : 1300,
              "Business, Management and Accounting" : 1400, 
              "Chemical Engineering" : 1500, 
              "Chemistry" : 1600, 
              "Computer Science" : 1700, 
              "Decision Sciences" : 1800, 
              "Dentistry" : 3500, 
              "Earth and Planetary Sciences" : 1900,
              "Economics, Econometrics and Finance" : 2000,
              "Energy" : 2100, 
              "Engineering" : 2200,
              "Environmental Science" : 2300,
              "Health Professions" : 3600, 
              "Immunology and Microbiology" : 2400, 
              "Materials Science" : 2500,
              "Mathematics" : 2600, 
              "Medicine" : 2700,
              "Neuroscience" : 2800, 
              "Nursing" : 2900, 
              "Pharmacology, Toxicology and Pharmaceutics" : 3000, 
              "Physics and Astronomy" : 3100, 
              "Psychology" : 3200,
              "Social Sciences" : 3300,
              "Veterinary" : 3400}


def read_file(fname):
    """Read individual file with Journal Impact Factors."""
    df = pd.read_excel(fname, index_col=2)
    df = df[df['Type'] == 'journal']
    df['year'] = fname.split()[1]
    df['field'] = os.path.basename(fname)
    df['field'] = df['field'].str.replace('scimagojr|.csv|.xlsx|Subject Area -|\d+', ' ')
    df['field'] = df['field'].replace(dict1, regex=True)
    return df[['field', 'year', 'SJR', 'H index', 'Cites / Doc. (2years)', 'Issn', 'Sourceid']]


def main():
    files = sorted(glob(SOURCE_FOLDER + "*.xlsx"))
    out = pd.concat([read_file(f) for f in files], axis=0)
    out = out.rename(columns={'H index': 'h-index',
                              'Cites / Doc. (2years)': 'avg_citations'})
    out.to_csv(TARGET_FILE)


if __name__ == '__main__':
    main()

