import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from parser import parse_chat
from sentiment import add_sentiment
from response import calculate_response_times
from sleepfilter import filter_sleep_hours
from metrics import relationship_metrics

# ------------------------
# Helper functions
# ------------------------

# Argument detection
conflict_words = ["never", "always", "fine", "whatever", "stop", "leave", "done", "why"]

def detect_arguments(df):
    df["argument_flag"] = False
    for i, row in df.iterrows():
        message = row["message"].lower()
        if row["sentiment"] < -0.5 or any(word in message for word in conflict_words):
            df.loc[i, "argument_flag"] = True
    return df

# Interest trend (simple engagement score)
def engagement_score(df):
    sentiment = df["sentiment"].mean()
    response = df["response_minutes"].mean()
    if pd.isna(response):
        response = 0
    score = sentiment - (response * 0.01)
    return score

# ------------------------
# Streamlit Dashboard
# ------------------------

st.title("Convo Analyzer")

uploaded_file = st.file_uploader("Upload your chat.txt file", type="txt")

if uploaded_file:
    with open("temp_chat.txt", "wb") as f:
        f.write(uploaded_file.getbuffer())

    df = parse_chat("temp_chat.txt")
    df = add_sentiment(df)
    df = calculate_response_times(df)
    df = filter_sleep_hours(df)
    df = detect_arguments(df)

    results = relationship_metrics(df)
    engagement = engagement_score(df)
    argument_count = df["argument_flag"].sum()

    # ------------------------
    # Metrics
    # ------------------------
    st.header("Relationship Metrics")
    st.write("Average Sentiment:", round(results["average_sentiment"], 3))
    st.write("Average Response Time:", round(results["average_response_time"], 2), "minutes")
    st.write("Messages per person:")
    st.write(results["messages_per_person"])
    st.write("Argument Messages Detected:", argument_count)
    st.write("Engagement Score (higher = more active & positive):", round(engagement, 3))

    # ------------------------
    # Sentiment Over Time
    # ------------------------
    st.header("Sentiment Over Time")
    sentiment_plot = df.set_index("timestamp")["sentiment"]

    fig, ax = plt.subplots()
    sentiment_plot.plot(ax=ax, marker='o')
    ax.set_ylabel("Sentiment")
    ax.set_xlabel("Time")
    st.pyplot(fig)

    # ------------------------
    # Response Time Distribution
    # ------------------------
    st.header("Response Time Distribution")
    fig2, ax2 = plt.subplots()
    df["response_minutes"].hist(ax=ax2)
    ax2.set_xlabel("Minutes")
    ax2.set_ylabel("Frequency")
    st.pyplot(fig2)

    # ------------------------
    # Arguments Highlight
    # ------------------------
    st.header("Argument Messages")
    arg_df = df[df["argument_flag"]]
    if len(arg_df) == 0:
        st.write("No argument messages detected.")
    else:
        st.dataframe(arg_df[["timestamp", "sender", "message", "sentiment"]])

    # ------------------------
    # Raw Messages
    # ------------------------
    st.header("All Messages")
    st.dataframe(df)