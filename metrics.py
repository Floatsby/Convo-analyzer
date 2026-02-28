def relationship_metrics(df):

    avg_sentiment = df["sentiment"].mean()

    avg_response = df["response_minutes"].mean()

    messages_per_person = df["sender"].value_counts()

    return {
        "average_sentiment": avg_sentiment,
        "average_response_time": avg_response,
        "messages_per_person": messages_per_person
    }