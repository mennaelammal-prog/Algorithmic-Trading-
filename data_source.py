"""
Drop-in replacement for `vbt.YFData.download(...).get(''Close'')` that works
without live internet access to Yahoo Finance.

Why this exists
----------------
The original template pulls prices straight from Yahoo Finance at research
time (`vbt.YFData.download`) and at backtest time (`YahooDataBacktesting`).
That''s fine on a normal machine, but it fails anywhere Yahoo''s endpoints are
network-blocked (locked-down sandboxes, restrictive corporate proxies, CI
runners, etc.) with connection errors rather than a clean message.

`load_prices()` below is a straight substitute for the Yahoo download step
in notebooks/examples.ipynb:

    # before
    data = vbt.YFData.download(symbols, start=start_date, end=end_date)
    price = data.get(''Close'')

    # after
    from data_source import load_prices
    price = load_prices(symbols, start=start_date, end=end_date)

Resolution order per symbol
----------------------------
1. data/<SYMBOL>.csv   -- a local CSV you provide (see data/README.md for
   the expected columns and where to export one from).
2. Yahoo Finance, via vectorbt -- only attempted if the CSV isn''t present,
   and only works where Yahoo''s endpoints are actually reachable.

Mixing is fine: keep SPY.csv locally and let the rest come from Yahoo, etc.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

# Accept the column header spellings used by the common export sources
# (Yahoo''s own "Download" button, Stooq, most broker exports).
_CLOSE_COLUMN_CANDIDATES = ["Close", "close", "Adj Close", "adj_close", "CLOSE"]
_DATE_COLUMN_CANDIDATES = ["Date", "date", "DATE", "Datetime", "timestamp"]


def _read_local_csv(symbol: str) -> pd.Series | None:
    path = DATA_DIR / f"{symbol}.csv"
    if not path.exists():
        return None

    df = pd.read_csv(path)

    date_col = next((c for c in _DATE_COLUMN_CANDIDATES if c in df.columns), None)
    close_col = next((c for c in _CLOSE_COLUMN_CANDIDATES if c in df.columns), None)
    if date_col is None or close_col is None:
        raise ValueError(
            f"data/{symbol}.csv doesn''t look like a price export "
            f"(found columns: {list(df.columns)}). "
            f"Expected a ''{_DATE_COLUMN_CANDIDATES[0]}'' and a "
            f"''{_CLOSE_COLUMN_CANDIDATES[0]}'' column -- see data/README.md."
        )

    df[date_col] = pd.to_datetime(df[date_col])
    series = df.set_index(date_col)[close_col].sort_index()
    series.name = symbol
    return _to_naive(series)


def _to_naive(series: pd.Series) -> pd.Series:
    """
    Strip timezone info from a series'' DatetimeIndex, if any.

    Local CSVs are naive already, but Yahoo Finance (via vectorbt) returns a
    UTC-aware index. Mixing the two -- or comparing either against the plain
    `pd.Timestamp(start)`/`pd.Timestamp(end)` used for date-range filtering
    below -- raises "Invalid comparison between dtype=datetime64[ns, UTC]
    and Timestamp". Normalizing everything to naive here keeps both sources
    comparable regardless of which symbols come from which source.
    """
    if isinstance(series.index, pd.DatetimeIndex) and series.index.tz is not None:
        series = series.copy()
        series.index = series.index.tz_localize(None)
    return series


def load_prices(symbols: list[str], start: str, end: str) -> pd.DataFrame:
    """
    Return a DataFrame of daily close prices for `symbols`, columns in the
    same order as `symbols`, indexed by date and clipped to [start, end).

    Raises a clear RuntimeError (naming exactly which symbols failed and
    why) rather than letting a network error or a malformed CSV surface as
    a confusing stack trace deep inside vectorbt/pandas.
    """
    local_hits: dict[str, pd.Series] = {}
    missing: list[str] = []

    for symbol in symbols:
        series = _read_local_csv(symbol)
        if series is not None:
            local_hits[symbol] = series
        else:
            missing.append(symbol)

    remote_hits: dict[str, pd.Series] = {}
    if missing:
        try:
            import vectorbt as vbt  # imported lazily so a CSV-only run never needs it importable issues

            remote = vbt.YFData.download(missing, start=start, end=end).get("Close")
            if isinstance(remote, pd.Series):
                remote = remote.to_frame(name=missing[0])
            for symbol in missing:
                remote_hits[symbol] = _to_naive(remote[symbol])
        except Exception as exc:
            found = ", ".join(sorted(local_hits)) or "none"
            raise RuntimeError(
                f"No local CSV for {missing}, and the fallback Yahoo Finance "
                f"download failed ({exc!r}). Symbols loaded from data/*.csv: "
                f"{found}. Drop a CSV per missing symbol into data/ (see "
                f"data/README.md) or run this somewhere with Yahoo Finance "
                f"reachable."
            ) from exc

    all_series = {**local_hits, **remote_hits}
    price = pd.DataFrame({s: all_series[s] for s in symbols})
    price = price.loc[(price.index >= pd.Timestamp(start)) & (price.index < pd.Timestamp(end))]
    price = price.sort_index()

    if price.isna().any().any():
        bad_cols = price.columns[price.isna().any()].tolist()
        raise RuntimeError(
            f"Loaded price data has gaps (NaNs) in columns: {bad_cols}. "
            f"Check the date range in those CSVs covers [{start}, {end})."
        )

    return price
