"""Create descriptors database."""

import glob

import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)
COMPRESSED_PATH = DIR_PATH + "_compressed/"


def _concatenate_dataframes(filenames):
    dataframes = []
    for filename in tqdm(filenames):
        dataframes.append(pd.read_csv(filename, compression="zip"))

    return pd.concat(dataframes, ignore_index=True)


def process_data():
    """Process the compressed CSV files."""

    filenames = glob.glob(COMPRESSED_PATH + "*.zip")
    dataframe = _concatenate_dataframes(filenames)
    descriptors = dataframe.descriptors.str.split("; ").explode().str.strip()
    #
    descriptors = descriptors.str.replace('"', "")
    descriptors = descriptors[descriptors.str.startswith("#") == False]
    descriptors = descriptors[descriptors.str.startswith("$") == False]
    descriptors = descriptors[descriptors.str.startswith("!") == False]
    descriptors = descriptors[descriptors.str.startswith("%") == False]
    descriptors = descriptors[descriptors.str.contains("<SUB>") == False]
    descriptors = descriptors[descriptors.str.contains("@") == False]
    # descriptors = descriptors[descriptors.str.contains("|") == False]

    #
    value_counts = descriptors.value_counts()

    db = pd.DataFrame(
        {
            "term": value_counts.index,
            "occ": value_counts.values,
        }
    )

    db.to_csv(DIR_PATH + "db.csv.zip", index=False, compression="zip")


if __name__ == "__main__":
    process_data()
