"""Create descriptors database."""

import pandas as pd  # type: ignore
from nltk.corpus import words as nltk_words

DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)


nltk_word_list = set(nltk_words.words())


def _extract_keywords():

    db = pd.read_csv(DIR_PATH + "keywords.csv.zip", compression="zip")
    db["term"] = db.term.str.split(" ")
    db = db.explode("term")
    db["term"] = db.term.str.strip()
    db = db.drop_duplicates(subset=["term"])
    terms = db.term.str.upper().to_list()

    return terms


def _extract_starting_words():

    db = pd.read_csv(DIR_PATH + "db.csv.zip", compression="zip")

    db["term"] = db.term.str.split(" ")
    db = db[db.term.str.len() > 1]
    db["term"] = db.term.str[0]
    db = db[db["term"].str.match(r"^\d") == False]

    return _db_clean(db)


def _extract_ending_words():

    db = pd.read_csv(DIR_PATH + "db.csv.zip", compression="zip")

    db["term"] = db.term.str.split(" ")
    db = db[db.term.str.len() > 1]
    db["term"] = db.term.str[-1]
    db = db[db["term"].str.match(r"^\d") == False]

    return _db_clean(db)


def is_correct_word(word):
    return word.lower() in nltk_word_list


def _db_clean(db):

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
    db = db[db["term"].str.contains("_") == False]
    db = db[db["term"].str.contains("-") == False]

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

    # the strings in the column "term" has no numbers
    db = db[db["term"].apply(lambda x: not any(char.isdigit() for char in x))]

    db = db[db.term.str.len() > 4]

    db = db.groupby("term", as_index=False).sum().reset_index(drop=True)

    db = db.sort_values(["occ", "term"], ascending=[False, True]).reset_index(drop=True)

    return db


def process_data():
    """Process the compressed CSV files."""

    keywords = _extract_keywords()

    db = _extract_starting_words()
    db = db[~db.term.isin(keywords)]
    db = db[db.term.str.len() > 2]
    db = db[db.term.str.contains(r"[AEIOU]")]
    db = db[~db.term.str.contains(r"\d")]
    db = db[db.term.apply(is_correct_word)]

    # db = db[db.occ > 0]

    starting_words = db.term.to_list()

    with open("results/raw_starting_words.txt", "wt", encoding="utf-8") as file:
        for term in starting_words:
            file.write(term + "\n")

    # for _, row in db.head(200).iterrows():
    #     print(row["term"], "\t", row["occ"])

    db = _extract_ending_words()
    db = db[~db.term.isin(keywords)]
    db = db[db.term.str.len() > 2]
    db = db[db.term.str.contains(r"[AEIOU]")]
    db = db[~db.term.str.contains(r"\d")]
    db = db[db.term.apply(is_correct_word)]

    # db = db[db.occ > 0 | db.term.isin(starting_words)]

    ending_words = db.term.to_list()

    with open("results/raw_ending_words.txt", "wt", encoding="utf-8") as file:
        for term in ending_words:
            file.write(term + "\n")


if __name__ == "__main__":
    process_data()
