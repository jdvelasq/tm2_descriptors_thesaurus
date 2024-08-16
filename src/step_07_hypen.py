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

    # loads all terms in the database
    db = pd.read_csv(DIR_PATH + "db.csv.zip", compression="zip")

    # generates a list of single words
    db["term"] = db["term"].str.split(" ")
    db = db.explode("term")
    db["term"] = db["term"].str.strip()

    # select words without hypens
    words_without_hypens = db.term[db.term.str.contains(r"\-") == False].to_list()
    # print(words_without_hypens[:5])
    # print()

    # select words with hypens
    db = db[db["term"].str.contains("-") == True]
    db = db.groupby("term", as_index=False).sum().reset_index()
    db = db.sort_values(["occ", "term"], ascending=[False, True]).reset_index(drop=True)

    print("--1--")
    print(db.head())
    print()

    #
    # cleaning:
    #
    db = db[db["term"].str.startswith("-") == False]
    db = db[db["term"].str.endswith("-") == False]

    db = db[db["term"].str.contains(",") == False]
    db = db[db["term"].str.contains(":") == False]
    db = db[db["term"].str.contains("!") == False]
    db = db[db["term"].str.contains("{") == False]
    db = db[db["term"].str.contains("}") == False]
    db = db[db["term"].str.contains("&") == False]
    db = db[db["term"].str.contains("#") == False]
    db = db[db["term"].str.contains("%") == False]
    db = db[db["term"].str.contains("<") == False]
    db = db[db["term"].str.contains("=") == False]
    db = db[db["term"].str.contains(">") == False]
    db = db[db["term"].str.contains("~") == False]

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

    # remove terms with numbers
    db = db[db["term"].str.contains(r"\d") == False]

    print("--2--")
    print(db.head())
    print()

    # the word without hypens must exits in the list of words
    db = db[db["term"].str.replace("-", "").isin(words_without_hypens)]

    print("--3--")
    print(db.head())
    print()

    # the secod part of the hypened term must exist in the list of words
    db = db[db["term"].str.split("-").str[-1].isin(words_without_hypens)]

    print("--4--")
    print(db.head())
    print()

    # the second part of the hypened term must be a valid word in english
    db = db[db["term"].str.split("-").str[-1].apply(is_correct_word)]

    # the parts of the hypened term must be at least 2 and 3 characters long
    db = db[db["term"].str.split("-").str[0].str.len() > 1]
    db = db[db["term"].str.split("-").str[-1].str.len() > 2]

    # each part contains at least 1 vocal
    db = db[db["term"].str.split("-").str[0].str.contains(r"[AEIOU]") == True]
    db = db[db["term"].str.split("-").str[-1].str.contains(r"[AEIOU]") == True]

    print("--5--")
    print(db.head())
    print()

    # compute the number of occurences of the hypened term
    # compute apparences of terms with hypens
    db = db.groupby("term", as_index=False).sum().reset_index()
    db = db.sort_values(["occ", "term"], ascending=[False, True])

    # selects the most frequent word as correction error strategy
    db["word"] = db["term"].str.replace("-", "")
    db = db.groupby("word", as_index=False).agg({"term": list, "occ": "sum"})
    db["term"] = db["term"].str[0]

    # select hypened words with more than 4 characters
    # db = db[db.term.str.len() > 4]

    db = db.sort_values(["occ", "word"], ascending=[False, True])

    for i in range(1, 20):
        db_copy = db[db.occ > i]
        print(i, "\t rows: ", db_copy.shape[0])

    db = db[db.occ > 5]

    #
    db.to_csv(DIR_PATH + "hypen.csv.zip", index=False, compression="zip")
    #
    with open("results/raw_hypened_words.txt", "wt", encoding="utf-8") as file:
        for term in db.term:
            file.write(term + "\n")


if __name__ == "__main__":
    process_data()
