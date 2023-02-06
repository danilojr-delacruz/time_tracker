import pandas as pd
import numpy as np
import argparse

DATA_DIR = "/home/delacruz-danilojr/delacruz/Projects/time_tracker/data.csv"
TODAY = pd.Timestamp("today")


def add_entry(activity, duration, date=None):
    """
    duration (int): Minutes.
    date (str): Y-m-d format
    """
    if date is None:
        date = TODAY.strftime("%Y-%m-%d")
    
    with open(DATA_DIR, 'a') as f:
        f.write(f"\n{activity},{duration},{date}")

def summary(timeframe="week"):
    df = pd.read_csv(DATA_DIR).set_index("date")
    df.index = pd.to_datetime(df.index)
    
    if timeframe == "week":
        start=TODAY.to_period("W").start_time
        end=TODAY.to_period("W").end_time
        # Need to address this if you are considering other weeks.
        date_range = pd.date_range(start=start, end=end, freq="D")
        df = df.loc[start:end]

    # Ensure all days of the week are present
    summary = df.pivot_table(columns="activity", index="date", values="duration", aggfunc=np.sum)
    summary = summary.reindex(date_range).T
    summary.loc["Total"] = summary.sum(axis=0)
    summary.columns = summary.columns.day_name()
    summary["Total"] = summary.sum(axis=1)
    
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Time Tracker",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("mode", default="a", help="a (add), s (summary), l (log)")
    args = parser.parse_args()
    
    if args.mode == "a":
        activity = input("Activity: ")
        duration = int(input("Duration: "))
        
        add_entry(activity, duration)
    elif args.mode == "s":
        print(summary())
    elif args.mode == "l":
        print(pd.read_csv(DATA_DIR).set_index("date").head(50))
    else:
        print("Choose one of: a (add), s (summary), l (log) ")
        