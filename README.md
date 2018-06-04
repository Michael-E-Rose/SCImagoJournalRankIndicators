# ScimagoEconJournalImpactFactors
Scimago Impact Factors for Economis and Econometrics Journal since 1999

## What is this?
To ease the use of measures of Journal Quality of Economics journals in my research, I have compiled a panel dataset using the yearly Scimago Journal Impact Factors.  These data originate from https://www.scimagojr.com/journalrank.php and date back to 1999.  In June 2018 I made the data public so that everyone can use them freely and conveniently via internet.

## How do I use this?

In folder [compiled/](./compiled/) you find the file you are looking for: A long list of Journals with their yearly SJR (Scimago Journal Rank), the h-index and avgerage citations.  All of them are measured using articles from the previous three years.

Usage in your scripts is easy:

* In python (with pandas):
```python
import pandas as pd
url = 'https://raw.githubusercontent.com/Michael-E-Rose/ScimagoEconJournalImpactFactors/master/compiled/Scimago_JIFs.csv'
df = pd.read_csv(url)
```

* In R:
```R
url = 'https://raw.githubusercontent.com/Michael-E-Rose/ScimagoEconJournalImpactFactors/master/compiled/Scimago_JIFs.csv'
df <- read.csv(url)
```

* In Stata:
```Stata
insheet using "https://raw.githubusercontent.com/Michael-E-Rose/ScimagoEconJournalImpactFactors/master/compiled/Scimago_JIFs.csv"
```

## What's the benefit?
- Central and continuously updated online storage for seamless inclusion in local scripts.
- Longitudinal collection of the quality measures according to their three different methods.
