"""Extract keywords and noun phrases from the text."""

import glob

import pandas as pd  # type: ignore
import textblob  # type: ignore
from tqdm import tqdm  # type: ignore

DIRPATH = "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/_compressed/"


def process_data():
    """Process the compressed CSV files."""

    filenames = glob.glob(DIRPATH + "*.zip")

    for filename in tqdm(filenames):

        df = pd.read_csv(filename, compression="zip")

        for col in ["Title", "Abstract"]:

            df[col + " Noun Phrases"] = df[col].astype(str)
            df[col + " Noun Phrases"] = df[col + " Noun Phrases"].str.replace(
                " 's ", " "
            )
            df[col + " Noun Phrases"] = df[col + " Noun Phrases"].apply(
                lambda x: "; ".join(list(textblob.TextBlob(x).noun_phrases))
            )

        df.to_csv(filename, index=False, compression="zip")


if __name__ == "__main__":
    process_data()
