"""Extract keywords and noun phrases from the text."""

import glob

import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

DIRPATH = "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/_compressed/"


def process_data():
    """Process the compressed CSV files."""

    filenames = glob.glob(DIRPATH + "*.zip")

    for filename in tqdm(filenames):

        df = pd.read_csv(filename, compression="zip")
        # print()
        # print(df[].head())
        # print()

        for _, row in df.head().iterrows():
            # print(row["Title Noun Phrases"])
            # print(row["Abstract Noun Phrases"])
            # print(row["Title"])
            # print(row["Abstract"])
            # print(row["Author Keywords"])
            # print(row["Index Keywords"])
            print(row["descriptors"])
            print()


if __name__ == "__main__":
    process_data()
