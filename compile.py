#!/usr/bin/env python3
"""Creates a long file of yearly SCImago journal rankings."""

import time
from io import StringIO
from pathlib import Path

import pandas as pd
from curl_cffi import requests as cffi_requests
from playwright.sync_api import sync_playwright
from tqdm import tqdm
from yaml import safe_load

TARGET_FILE = Path("./all.csv")

START_YEAR = 1999
END_YEAR = time.localtime().tm_year  # Or override manually


def load_asjc_field_map(file="auxiliary.yaml"):
    """Load ASJC field map from a YAML file."""
    with open(file, 'r') as yaml_file:
        return safe_load(yaml_file)['ASJC_FIELD_MAP']


def get_cloudflare_cookies():
    """Use a real browser to pass Cloudflare and return cookies + user-agent."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False, channel="chrome",
            args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context()
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
        page = context.new_page()
        print("Opening browser to pass Cloudflare challenge...")
        print("If you see a Cloudflare checkbox, please click it.")
        page.goto("https://www.scimagojr.com/journalrank.php",
                  wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector("text=Journal Rankings", timeout=120000)
        cookies = context.cookies()
        user_agent = page.evaluate("() => navigator.userAgent")
        browser.close()
    return cookies, user_agent


def get_file(session, year, delay=1):
    """Fetch and process SCImago Journal Ranks for a given year."""
    time.sleep(delay)
    # Download file
    try:
        url = f"https://www.scimagojr.com/journalrank.php?year={year}&out=xls"
        response = session.get(url)
        response.raise_for_status()
    except Exception as e:
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
    # Pass Cloudflare with a real browser
    cookies, user_agent = get_cloudflare_cookies()
    print("Cloudflare passed, downloading data...")

    # Build curl_cffi session (impersonates Chrome TLS fingerprint)
    session = cffi_requests.Session(impersonate="chrome")
    session.headers["User-Agent"] = user_agent
    for c in cookies:
        session.cookies.set(c["name"], c["value"], domain=c["domain"])

    # Get files
    df = pd.concat([get_file(session, y) for y in tqdm(range(START_YEAR, END_YEAR))],
                   ignore_index=True)

    # Change field names
    field_map = load_asjc_field_map()
    df['field'] = df['field'].map(field_map)

    # Write out
    df = df.sort_values(["field", "Title", "year"])
    df.to_csv(TARGET_FILE, index=False)
