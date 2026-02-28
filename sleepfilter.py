def filter_sleep_hours(df):

    df["hour"] = df["timestamp"].dt.hour

    df = df[(df["hour"] >= 7) & (df["hour"] <= 23)]

    return df