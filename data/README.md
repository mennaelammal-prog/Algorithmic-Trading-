# Price data for offline / network-restricted use

`data_source.py` reads one CSV per ticker from this folder before ever
touching Yahoo Finance, so the notebook and backtest keep working in places
where Yahoo's API is blocked.

## Expected filenames

One file per symbol, named exactly `<SYMBOL>.csv`, e.g.:

```
data/
  AAPL.csv
  MSFT.csv
  GOOGL.csv
  AMZN.csv
  NVDA.csv
  META.csv
  TSLA.csv
  SPY.csv
```

## Expected columns

A `Date` column plus a `Close` column (case-insensitive; `Adj Close` is
also accepted). Anything else in the file is ignored, so you can export
straight from most sources without cleanup:

```csv
Date,Open,High,Low,Close,Volume
2021-01-04,133.52,133.61,126.76,129.41,143301900
2021-01-05,128.89,131.74,128.43,131.01,97664900
...
```

## Where to get one

- **Yahoo Finance (browser):** open `finance.yahoo.com/quote/AAPL/history`,
  set the date range, and use the "Download" link -- no API call, no
  network block, just a file.
- **Stooq:** `stooq.com/q/d/l/?s=aapl.us&i=d` downloads a CSV directly.
- **Your broker / data vendor:** any OHLC(V) export works as long as it has
  `Date` and `Close`.
- **This repo's own tooling, run somewhere with internet:** on a machine
  that *can* reach Yahoo, run

  ```python
  import vectorbt as vbt
  vbt.YFData.download(["AAPL"], start="2021-01-01", end="2026-01-01") \
      .get().reset_index().rename(columns={"index": "Date"}) \
      .to_csv("data/AAPL.csv", index=False)
  ```

  then copy the resulting `data/*.csv` files to wherever you need them
  (including back into this sandbox).

Files in this folder are git-ignored (see `.gitignore`) so your price data
never ends up committed to the repo by accident.
