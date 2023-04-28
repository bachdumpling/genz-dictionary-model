import pandas as pd
from langdetect import detect, LangDetectException

# Read the comment_data.csv file
comment_data = pd.read_csv("comment_data.csv", on_bad_lines='skip')

# Filter out non-English comments
english_comments = []
for comment in comment_data["comments"]:
    try:
        if detect(comment) == "en":
            english_comments.append(comment)
    except LangDetectException:
        pass

# Write the filtered comments to a new file called english_comments.csv
pd.DataFrame({"comments": english_comments}).to_csv("english_comments.csv", index=False)
