"""Create descriptors database."""

import glob

import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)


def process_data():
    """Process the compressed CSV files."""

    db = pd.read_csv(DIR_PATH + "hypen.csv.zip", compression="zip")
    # db = db.sort_values(["term", "occ"], ascending=[True, False])
    # db = db.sort_values(["term", "occ"], ascending=[False, False])
    # db = db.sort_values("occ", ascending=False)
    # db = db.sort_values("occ", ascending=True)
    # db = db[db.term.astype(str).str.contains(";")]
    print(db.shape)
    print("_________________________________ DB __________________________________")
    print()
    print(db.head(60))
    print()
    print(db.tail(60))

    # for index in db.index[:1000]:
    #     print(db.at[index, "term"], "\t\t", db.at[index, "occ"])
    # print()


if __name__ == "__main__":
    process_data()
