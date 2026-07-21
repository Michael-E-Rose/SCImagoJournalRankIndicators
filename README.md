# SCImagoJournalRankIndicators
SCImago Journal Rank Indicators for all Journals in all fields since 1999

## What is this?
To ease the use of measures of Journal Quality in my research, I have compiled a panel dataset using the yearly Scimago Journal Impact Factors.  These data originate from https://www.scimagojr.com/journalrank.php and date back to 1999.  In June 2018 I made the data public so that everyone can use them freely and conveniently via http.

## How do I use this?

The dataset is available in two formats:
- **`all.parquet`** — Parquet file with optimised dtypes, small and fast to read.
- **`all.csv`** — CSV file, for broad compatibility. **The CSV file will be discontinued in 2028.** Please migrate to the Parquet format before then.

Usage in your scripts is easy:

* In *python* (using pandas):
```python
import pandas as pd
url = 'https://raw.githubusercontent.com/Michael-E-Rose/SCImagoJournalRankIndicators/master/all.parquet'
df = pd.read_parquet(url)
```

* In *R* (using arrow):
```R
library(arrow)
url <- 'https://raw.githubusercontent.com/Michael-E-Rose/SCImagoJournalRankIndicators/master/all.parquet'
df <- read_parquet(url)
```

* In *Stata* (using parquet package):
```Stata
parquet use "https://raw.githubusercontent.com/Michael-E-Rose/SCImagoJournalRankIndicators/master/all.parquet"
```

### Note
Journals will be listed multiple times when they belong to multiple ASJC fields. But their metrics are the same, so you can safely drop Sourceid-year duplicates.

## What's the benefit?
- Central and continuously updated online storage for seamless inclusion in local scripts.
- Longitudinal collection of the quality measures according to their three different methods.
