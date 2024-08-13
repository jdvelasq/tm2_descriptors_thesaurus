"""Create descriptors database."""

import glob

import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)


def process_data():
    """Process the compressed CSV files."""

    db = pd.read_csv(DIR_PATH + "db.csv.zip", compression="zip")
    #
    db["term"] = db["term"].str.split(" ")
    db = db.explode("term")
    db["term"] = db["term"].str.strip()
    #
    db = db[db["term"].str.startswith("-") == False]
    db = db[db["term"].str.endswith("-") == False]
    db = db[db["term"].str.startswith("!") == False]
    db = db[db["term"].str.startswith("$") == False]
    db = db[db["term"].str.startswith("%") == False]
    db = db[db["term"].str.startswith("&") == False]
    db = db[db["term"].str.startswith("+") == False]
    db = db[db["term"].str.startswith(",") == False]
    db = db[db["term"].str.startswith(".") == False]
    db = db[db["term"].str.startswith("#") == False]
    db = db[db["term"].str.startswith("&") == False]
    db = db[db["term"].str.startswith("*") == False]
    db = db[db["term"].str.startswith("(") == False]
    db = db[db["term"].str.startswith(")") == False]
    db = db[db["term"].str.startswith(":") == False]
    db = db[db["term"].str.startswith("<") == False]
    db = db[db["term"].str.startswith(">") == False]
    db = db[db["term"].str.startswith("=") == False]
    db = db[db["term"].str.startswith("?") == False]
    db = db[db["term"].str.match(r"^\d") == False]
    #
    db = db.groupby("term").sum().reset_index()
    #
    words = db.term[db.term.str.contains("-") == False].to_list()

    db = db[db["term"].str.contains("-") == True]
    db = db[db["term"].str.replace("-", "").isin(words)]
    #
    db = db.sort_values(["occ", "term"], ascending=[False, True])
    #
    db["word"] = db["term"].str.replace("-", "")
    db = db.groupby("word", as_index=False).agg({"term": list, "occ": "sum"})
    db["term"] = db["term"].str[0]
    db = db.sort_values(["occ", "word"], ascending=[False, True])
    #
    db = db[db.occ > 1]
    #
    db.to_csv(DIR_PATH + "hypen.csv.zip", index=False, compression="zip")
    #
    with open("results/hypened_words.txt", "wt", encoding="utf-8") as file:
        for term in db.term:
            file.write(term + "\n")


if __name__ == "__main__":
    process_data()
