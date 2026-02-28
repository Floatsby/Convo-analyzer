import re
import pandas as pd
from datetime import datetime

def parse_chat(file_path):

    pattern = r"(\d+/\d+/\d+), (\d+:\d+) - (.*?): (.*)"

    messages = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:

            match = re.match(pattern, line)

            if match:
                date, time, sender, message = match.groups()

                timestamp = datetime.strptime(
                    date + " " + time,
                    "%d/%m/%y %H:%M"
                )

                messages.append({
                    "timestamp": timestamp,
                    "sender": sender,
                    "message": message
                })

    df = pd.DataFrame(messages)

    return df