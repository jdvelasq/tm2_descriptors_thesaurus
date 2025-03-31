"""Create descriptors database."""

import glob

import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)
COMPRESSED_PATH = DIR_PATH + "_compressed/"


def process_data():
    """Process the compressed CSV files."""

    filenames = glob.glob(COMPRESSED_PATH + "*.zip")

    for filename in tqdm(filenames):

        df = pd.read_csv(filename, compression="zip")

        df = df.assign(descritors=[[] for _ in range(len(df))])

        for _, row in df.iterrows():
            descriptors = set()
            for col in [
                "Title Noun Phrases",
                "Abstract Noun Phrases",
                "Author Keywords",
                "Index Keywords",
            ]:
                if isinstance(row[col], str):
                    for word in row[col].split("; "):
                        if word != "NAN":
                            descriptors.add(word.upper())

            df.at[_, "descriptors"] = "; ".join(sorted(descriptors))

        df.to_csv(filename, index=False, compression="zip")


if __name__ == "__main__":
    process_data()
