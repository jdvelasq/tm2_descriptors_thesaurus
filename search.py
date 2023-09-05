import os

import pandas as pd

files = os.listdir("journals")


found_keywords = set()
keywords = set()
for file in files:
    #
    df = pd.read_csv("journals/" + file, encoding="utf-8")

    for column in ["Author Keywords", "Index Keywords"]:
        if column in df.columns:
            words = set(
                df["Author Keywords"]
                .dropna()
                .astype(str)
                .str.upper()
                .str.split("; ")
                .explode()
                .str.strip()
                .str.replace("--", "-")
                .str.replace(".", "")
                .str.replace(",", "")
                .str.split(" ")
                .explode()
                .str.strip()
                .to_list()
            )

            keywords = keywords.union(words)


hypened_words = set(
    word for word in keywords if "-" in word if word.replace("-", "") in keywords
)


n_new = len(hypened_words - found_keywords)


found_keywords = found_keywords.union(hypened_words)

found_keywords = [word for word in found_keywords if word[0] != "-"]
found_keywords = [word for word in found_keywords if word[-1] != "-"]
found_keywords = [word for word in found_keywords if "(" not in word[0]]
found_keywords = [word for word in found_keywords if len(word) > 3]
found_keywords = [word for word in found_keywords if "<" not in word]
found_keywords = [word for word in found_keywords if word[0] not in "0123456789"]

for word in sorted(found_keywords)[-20:]:
    print(word)

with open("hypened_words.txt", "w") as f:
    for word in sorted(found_keywords):
        f.write(word + "\n")
