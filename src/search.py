# pylint: disable=unused-variable
"""search descriptors in database."""

import pandas as pd  # type: ignore

DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)


def _load_starting_words():
    with open("results/raw_starting_words.txt", "r", encoding="utf-8") as file:
        starting_words = file.read().splitlines()
    starting_words = [word.strip() for word in starting_words]
    return starting_words


def _load_ending_words():
    with open("results/raw_ending_words.txt", "r", encoding="utf-8") as file:
        ending_words = file.read().splitlines()
    ending_words = [word.strip() for word in ending_words]
    return ending_words


def _load_db():
    db = pd.read_csv(DIR_PATH + "db.csv.zip", compression="zip")
    db = db.dropna()
    return db


def _search_startwith(startswith, db, ending_words):

    db = db[db.term.str.startswith(startswith)]

    print()
    print("recovered records: ", db.shape[0])

    #
    startswith_len = len(startswith.split(" "))

    db = db[db.term.str.split(" ").str.len() > startswith_len]
    db["term"] = db["term"].str.split(" ").str[startswith_len + 1 :].str.join(" ")
    db = db.drop_duplicates(subset="term")
    db = db[db.term.str.strip().str.len() > 0]
    db = db[~db.term.isin(ending_words)]
    db = db[db.term.str.len() > 2]
    db = db.sort_values(by="term", ascending=True)
    #
    db = db[db.occ > 1]

    print(" filtered records: ", db.shape[0])
    print("_____________________ RESULTS _____________________")
    for term in db.term.values:
        print(
            startswith.replace(" ", "_")
            + "_"
            + term.replace(" ", "_").replace("-", "_")
        )
    print()


def _search_raw_string(raw_string, db):

    db = db[db.term.str.contains(raw_string)]

    print()
    print("recovered records: ", db.shape[0])

    db = db.dropna(subset=["term"])
    db = db[db.term.str.contains(raw_string)]
    db = db.drop_duplicates(subset="term")
    db = db.sort_values(by="term", ascending=True)
    #
    db = db[db.occ > 2]

    print(" filtered records: ", db.shape[0])
    print("_____________________ RESULTS _____________________")
    for term in db.term.values:
        print(term.replace(" ", "_").replace("-", "_"))
    print()


def _main():

    starting_words = _load_starting_words()
    ending_words = _load_ending_words()
    db = _load_db()

    text_string = "DRIVEN"

    # _search_startwith(text_string, db, ending_words)
    _search_raw_string(text_string, db)


if __name__ == "__main__":
    _main()
