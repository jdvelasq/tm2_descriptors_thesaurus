"""Create descriptors database."""

import glob

import pandas as pd  # type: ignore
from nltk.corpus import words as nltk_words
from tqdm import tqdm  # type: ignore

DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)

nltk_word_list = set(nltk_words.words())


def is_correct_word(word):
    return word.lower() in nltk_word_list


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

    db = db[db["term"].str.contains("!") == False]
    db = db[db["term"].str.contains("%") == False]
    db = db[db["term"].str.contains("&") == False]
    db = db[db["term"].str.contains(",") == False]
    db = db[db["term"].str.contains("#") == False]
    db = db[db["term"].str.contains("&") == False]
    db = db[db["term"].str.contains("~") == False]
    db = db[db["term"].str.contains("{") == False]
    db = db[db["term"].str.contains("}") == False]
    db = db[db["term"].str.contains("=") == False]
    db = db[db["term"].str.contains("<") == False]
    db = db[db["term"].str.contains(">") == False]
    db = db[db["term"].str.contains(":") == False]

    db = db[db["term"].str.contains(r"\$") == False]
    db = db[db["term"].str.contains(r"\+") == False]
    db = db[db["term"].str.contains(r"\.") == False]
    db = db[db["term"].str.contains(r"\|") == False]
    db = db[db["term"].str.contains(r"\*") == False]
    db = db[db["term"].str.contains(r"\(") == False]
    db = db[db["term"].str.contains(r"\)") == False]
    db = db[db["term"].str.contains(r"\[") == False]
    db = db[db["term"].str.contains(r"\]") == False]
    db = db[db["term"].str.contains(r"\^") == False]
    db = db[db["term"].str.contains(r"\?") == False]
    db = db[db["term"].str.contains(r"\\") == False]

    db = db[db["term"].str.contains(r"\d") == False]

    #
    db = db.groupby("term").sum().reset_index()
    #
    words = db.term[db.term.str.contains("-") == False].to_list()

    db = db[db["term"].str.contains("-") == True]
    db = db[db["term"].str.replace("-", "").isin(words)]
    db = db[db["term"].str.split("-").str[-1].isin(words)]
    #
    db = db.sort_values(["occ", "term"], ascending=[False, True])
    #
    db["word"] = db["term"].str.replace("-", "")
    db = db.groupby("word", as_index=False).agg({"term": list, "occ": "sum"})
    db["term"] = db["term"].str[0]
    db = db[db.term.str.len() > 4]
    db = db.sort_values(["occ", "word"], ascending=[False, True])
    #
    # db = db[db.term.apply(is_correct_word)]
    # db = db[db.occ > 1]
    #
    db.to_csv(DIR_PATH + "hypen.csv.zip", index=False, compression="zip")
    #
    with open("results/raw_hypened_words.txt", "wt", encoding="utf-8") as file:
        for term in db.term:
            file.write(term + "\n")


if __name__ == "__main__":
    process_data()
