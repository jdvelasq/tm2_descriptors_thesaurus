"""Search terms in the database."""

import pandas as pd  # type: ignore

DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)


db = pd.read_csv(DIR_PATH + "db.csv.zip", compression="zip")
#
# db = db[db.term.str.contains("COVID") == True]
db = db[db.term.str.startswith("M-") == True]
db["term"] = db.term.str.split(" ").str[0]
db = db.drop_duplicates(subset=["term"])
db = db.sort_values(by="term")
#
print()
for _, row in db.iterrows():
    print(row.term)
print()
