"""Create descriptors database."""

import glob

import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)


def process_data():
    """Process the compressed CSV files."""

    filenames = glob.glob(DIR_PATH + "_compressed/*.zip")

    dataframes = []

    for filename in tqdm(filenames):

        df = pd.read_csv(filename, compression="zip")

        author_keywords = df["Author Keywords"].dropna()

        if not author_keywords.empty:

            author_keywords = author_keywords.str.split("; ")
            author_keywords = author_keywords.explode()
            author_keywords = author_keywords.str.strip()

            dataframes.append(
                pd.DataFrame(
                    {
                        "term": author_keywords.to_list(),
                        "occ": 1,
                    }
                )
            )

        index_keywords = df["Index Keywords"].dropna()

        if not index_keywords.empty:

            index_keywords = index_keywords.str.split("; ")
            index_keywords = index_keywords.explode()
            index_keywords = index_keywords.str.strip()

            dataframes.append(
                pd.DataFrame(
                    {
                        "term": index_keywords.to_list(),
                        "occ": 1,
                    }
                )
            )

    #
    dataframe = pd.concat(dataframes, ignore_index=True)
    dataframe = dataframe.groupby("term", as_index=False).sum().reset_index(drop=True)

    dataframe = dataframe[dataframe["term"].str.startswith("-") == False]
    dataframe = dataframe[dataframe["term"].str.endswith("-") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("!") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("$") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("%") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("&") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("+") == False]
    dataframe = dataframe[dataframe["term"].str.startswith(",") == False]
    dataframe = dataframe[dataframe["term"].str.startswith(".") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("#") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("&") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("*") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("(") == False]
    dataframe = dataframe[dataframe["term"].str.startswith(")") == False]
    dataframe = dataframe[dataframe["term"].str.startswith(":") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("<") == False]
    dataframe = dataframe[dataframe["term"].str.startswith(">") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("=") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("?") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("/") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("[") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("]") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("_") == False]
    dataframe = dataframe[dataframe["term"].str.startswith("\\") == False]
    dataframe = dataframe[dataframe["term"].str.match(r"^\d") == False]
    dataframe = dataframe[dataframe["term"].str.contains("<") == False]
    dataframe = dataframe[dataframe["term"].str.contains(">") == False]

    dataframe["term"] = dataframe["term"].str.replace("^a ", "", regex=True)
    dataframe["term"] = dataframe["term"].str.replace("^an ", "", regex=True)
    dataframe["term"] = dataframe["term"].str.replace("^and ", "", regex=True)
    dataframe["term"] = dataframe["term"].str.replace("^the ", "", regex=True)

    dataframe.to_csv(DIR_PATH + "keywords.csv.zip", index=False, compression="zip")


if __name__ == "__main__":
    process_data()
