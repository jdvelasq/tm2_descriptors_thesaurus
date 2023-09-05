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


error_terms = set(word for word in keywords if word.endswith("ERROR"))
n_new = len(error_terms)


found_keywords = found_keywords.union(error_terms)

found_keywords = [word for word in found_keywords if word[0] != "-"]
found_keywords = [word for word in found_keywords if word[-1] != "-"]
found_keywords = [word for word in found_keywords if "(" not in word[0]]
found_keywords = [word for word in found_keywords if len(word) > 3]
found_keywords = [word for word in found_keywords if "<" not in word]
found_keywords = [word for word in found_keywords if word[0] not in "0123456789"]

for word in sorted(found_keywords)[-5:]:
    print(word)

print("---> " + str(n_new))

with open("error_terms.txt", "w") as f:
    for word in sorted(found_keywords):
        f.write(word + "\n")
