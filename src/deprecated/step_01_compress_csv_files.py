"""Compress CSV files in a directory using gzip."""

import glob
import os

import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

DIRPATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)


def compress_csv_files():
    """Select columns from CSV files and compress them using zip."""

    filenames = glob.glob(DIRPATH + "/_raw/*.csv")

    ## filenames = filenames[:10] # to debug

    for filename in tqdm(filenames):
        df = pd.read_csv(filename)
        df = df[
            [
                "Title",
                "Year",
                "Source title",
                "Abstract",
                "Author Keywords",
                "Index Keywords",
            ]
        ]
        filename = os.path.basename(filename)
        new_filename = os.path.join(DIRPATH + "/_compressed/", filename) + ".zip"
        df.to_csv(new_filename, index=False, compression="zip")


if __name__ == "__main__":
    compress_csv_files()
