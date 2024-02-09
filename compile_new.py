#!/usr/bin/env python3
# Author:   Michael E. Rose <michael.ernst.rose@gmail.com>
#           Carolin Formella
"""Creates a long file of yearly Journal Impact Factors."""

from pathlib import Path

import pandas as pd
import requests
from io import StringIO

TARGET_FILE = Path("./all.csv")

ASJC_FIELD_MAP = {"Multidisciplinary": 1000,
    "Agricultural and Biological Sciences": 1100,
    "Arts and Humanities": 1200,
    "Biochemistry, Genetics and Molecular Biology": 1300,
    "Business, Management and Accounting": 1400,
    "Chemical Engineering": 1500,
    "Chemistry": 1600,
    "Computer Science": 1700,
    "Decision Sciences": 1800,
    "Dentistry": 3500,
    "Earth and Planetary Sciences": 1900,
    "Economics, Econometrics and Finance": 2000,
    "Energy": 2100,
    "Engineering": 2200,
    "Environmental Science": 2300,
    "Health Professions": 3600,
    "Immunology and Microbiology": 2400,
    "Materials Science": 2500,
    "Medicine": 2700,
    "Mathematics": 2600,
    "Neuroscience": 2800,
    "Nursing": 2900,
    "Pharmacology, Toxicology and Pharmaceutics": 3000,
    "Physics and Astronomy": 3100,
    "Psychology": 3200,
    "Social Sciences": 3300,
    "Veterinary": 3400}

def get_file(response, t):
    """Get individual file with Journal Impact Factors."""
    df = pd.read_csv(StringIO(response.text), delimiter=';', dtype={5: str, 'Issn':str})
    print()
    df = df[df['Type'] == 'journal']
    df["SJR"] = df["SJR"].str.replace(',', '.').astype(float).round(3)
    df["Cites / Doc. (2years)"] = df["Cites / Doc. (2years)"].str.replace(',', '.').astype(float)
    df['year'] = t
    df['Areas'] = df['Areas'].str.split('; ')
    df = df.explode('Areas')
    df = df.rename(columns={'H index': 'h-index',
                            'Areas' : 'field',
                            'Cites / Doc. (2years)': 'avg_citations'})
    df['field'] = df['field'].map(ASJC_FIELD_MAP)
    order = ['Title','field', 'year', 'SJR', 'h-index', 'avg_citations',
             'Issn', 'Sourceid']
    return df[order]

def main():
  df_out = pd.DataFrame()

  for t in range(1999, 2023):

      response = requests.get(f"https://www.scimagojr.com/journalrank.php?year={t}&out=xls")

      if response.status_code == 200:
          df_out = pd.concat([df_out, get_file(response, t)], axis=0, ignore_index=True)
      else:
          print(f"Failed to download data for year {t}")

  df_out.to_csv(TARGET_FILE)

  if __name__ == '__main__':
    main()