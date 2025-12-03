#!/usr/bin/env python3
"""Creates a long file of yearly SCImago journal rankings."""

import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm
from yaml import safe_load

TARGET_FILE = Path("./all.csv")

START_YEAR = 1999
END_YEAR = time.localtime().tm_year  # Or override manually


def load_asjc_field_map(file="auxiliary.yaml"):
    """Load ASJC field map from a YAML file."""
    with open(file, 'r') as yaml_file:
        return safe_load(yaml_file)['ASJC_FIELD_MAP']


def get_file(year, delay=1):
    """Fetch and process SCImago Journal Ranks for a given year."""
    time.sleep(delay)
    # Download file
    try:
        url = f"https://www.scimagojr.com/journalrank.php?year={year}&out=xls"
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Failed to download data for year {year}: {e}")
        return None
    df = pd.read_csv(StringIO(response.text), delimiter=';', dtype={5: str, 'Issn': str})
    # Parse file
    df = df[df['Type'] == 'journal']
    df["SJR"] = df["SJR"].str.replace(',', '.').astype(float).round(3)
    df["Citations / Doc. (2years)"] = df["Citations / Doc. (2years)"].str.replace(',', '.').astype(float)
    df['Areas'] = df['Areas'].str.split('; ')
    df = df.explode('Areas')
    rename = {'H index': 'h-index', 'Areas': 'field',
              'Citations / Doc. (2years)': 'avg_citations'}
    df = df.rename(columns=rename)
    df['year'] = year
    order = ['Title', 'field', 'year', 'SJR', 'h-index', 'avg_citations',
             'Issn', 'Sourceid']
    return df[order]


if __name__ == '__main__':
    # Get file
    df = pd.concat([get_file(y) for y in tqdm(range(START_YEAR, END_YEAR))],
                   ignore_index=True)

    # Change field names
    field_map = load_asjc_field_map()
    df['field'] = df['field'].map(field_map)

    # Write out
    df = df.sort_values(["field", "Title", "year"])
    df.to_csv(TARGET_FILE, index=False)
