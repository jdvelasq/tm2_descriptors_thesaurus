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

        df["descriptors"] = df["descriptors"].astype(str).str.replace("/", " ")

        df.to_csv(filename, index=False, compression="zip")


if __name__ == "__main__":
    process_data()
