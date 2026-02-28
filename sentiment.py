from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def add_sentiment(df):

    sentiments = []

    for msg in df["message"]:
        score = sia.polarity_scores(msg)["compound"]
        sentiments.append(score)

    df["sentiment"] = sentiments

    return df