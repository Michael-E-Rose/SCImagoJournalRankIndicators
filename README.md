# SCImagoJournalRankIndicators
SCImago Journal Rank Indicators for all Journals in all fields since 1999

## What is this?
To ease the use of measures of Journal Quality in my research, I have compiled a panel dataset using the yearly Scimago Journal Impact Factors.  These data originate from https://www.scimagojr.com/journalrank.php and date back to 1999.  In June 2018 I made the data public so that everyone can use them freely and conveniently via http.

## How do I use this?

In this folder you find the file you are looking for: A long list of journals with their yearly SJR (SCImago Journal Rank), the h-index and avgerage citations.  All of them are measured using articles from the previous three years.  The file is a simple csv file.

Usage in your scripts is easy:

* In *python* (using pandas):
```python
import pandas as pd
url = 'https://raw.githubusercontent.com/Michael-E-Rose/SCImagoJournalRankIndicators/master/all.csv'
df = pd.read_csv(url)
```

* In *R*:
```R
url = 'https://raw.githubusercontent.com/Michael-E-Rose/SCImagoJournalRankIndicators/master/all.csv'
df <- read.csv(url)
```

* In *Stata*:
```Stata
insheet using "https://raw.githubusercontent.com/Michael-E-Rose/SCImagoJournalRankIndicators/master/all.csv"
```

### Note
Journals will be listed multiple times when they belong to multiple ASJC fields. But their metrics are the same, so you can safely drop Sourceid-year duplicates.

## What's the benefit?
- Central and continuously updated online storage for seamless inclusion in local scripts.
- Longitudinal collection of the quality measures according to their three different methods.
