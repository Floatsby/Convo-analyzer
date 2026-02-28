def calculate_response_times(df):

    df = df.sort_values("timestamp")

    response_times = []

    previous_time = None

    for time in df["timestamp"]:

        if previous_time is None:
            response_times.append(None)

        else:
            diff = (time - previous_time).total_seconds() / 60
            response_times.append(diff)

        previous_time = time

    df["response_minutes"] = response_times

    return df