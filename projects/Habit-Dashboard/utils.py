import pandas as pd
from datetime import timedelta, date

def df_from_db(session):
    df = pd.read_sql("select * from daily_entry order by day", session.bind, parse_dates=["day"])
    return df.set_index("day")

def rolling_metrics(df, window=7):
    roll = df.rolling(f"{window}D").mean()
    return roll[["sleep_hours","weight_kg","workouts_min","code_min"]]

def current_streak(series: pd.Series, break_after: int = 7) -> int:
    """
    Streak continues until you accumulate `break_after` consecutive zero/NaN days.
    Default: break after 7 missed days.

    Parameters
    ----------
    series : pd.Series
        Indexed by datetime (one value per day if logged).
    break_after : int
        Length of consecutive misses that resets the streak.
    """
    if series.empty:
        return 0

    # 1. expand to full calendar span, fill missing with 0
    start = series.index.min().normalize()
    end   = max(series.index.max().normalize(), pd.Timestamp(date.today()))
    full  = series.reindex(pd.date_range(start, end, freq="D"), fill_value=0)

    # 2. walk backward from the end
    streak = 0          # total “good” days
    gap    = 0          # consecutive misses encountered so far

    for value in reversed(full.values):
        if value > 0:
            streak += 1
            gap = 0                   # reset gap on success day
        else:
            gap += 1
            if gap >= break_after:    # 7 missed days → stop
                break

    return streak
