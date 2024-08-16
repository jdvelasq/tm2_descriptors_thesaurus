"""Extracts abbreviations from author and index keywords."""

import glob

import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

DIRPATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)


def main():
    """Select columns from CSV files and compress them using zip."""

    filenames = glob.glob(DIRPATH + "/_raw/*.csv")

    # filenames = filenames[:10]  # to debug

    keywords = []

    for filename in tqdm(filenames):
        df = pd.read_csv(filename)
        for col in ["Author Keywords", "Index Keywords"]:
            frame = df[col].dropna()
            if frame.shape[0] == 0:
                continue
            frame = frame.str.split("; ")
            frame = frame.explode()
            frame = frame.str.strip()
            frame = frame.str.upper()
            keywords.extend(frame.to_list())

    dataframe = pd.DataFrame(
        {
            "term": sorted(set(keywords)),
        }
    )

    dataframe = dataframe[dataframe.term.str.endswith(")")]
    dataframe = dataframe[~dataframe.term.str.startswith("(")]

    dataframe["key"] = dataframe.term.str.extract(r"\((.*?)\)")
    dataframe["key"] = dataframe.key.str.strip()
    dataframe = dataframe.dropna()

    dataframe["term"] = (
        dataframe.term.str.replace(r"\(.*?\)", "", regex=True)
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("__+", "_", regex=True)
    )

    dataframe = dataframe.drop_duplicates()

    dataframe = dataframe[~dataframe.key.str.match(r"^\d")]
    dataframe = dataframe[~dataframe.key.str.contains(" ")]
    dataframe = dataframe[~dataframe.key.str.contains("&")]
    dataframe = dataframe[~dataframe.key.str.contains(":")]
    dataframe = dataframe[~dataframe.key.str.contains("%")]
    dataframe = dataframe[~dataframe.key.str.contains(r"\(")]
    dataframe = dataframe[~dataframe.key.str.contains("\)")]
    dataframe = dataframe[~dataframe.key.str.contains("\+")]
    dataframe = dataframe[~dataframe.key.str.contains(",")]
    dataframe = dataframe[~dataframe.key.str.contains("'")]
    dataframe = dataframe[~dataframe.key.str.contains("<")]
    dataframe = dataframe[~dataframe.key.str.contains(">")]
    dataframe = dataframe[~dataframe.key.str.contains("~")]
    dataframe = dataframe[~dataframe.key.str.startswith("-")]

    dataframe = dataframe[~dataframe.key.str.contains(r"[^\w\d_-]")]
    dataframe = dataframe[~dataframe.term.str.contains(r"[^\w\d_\- ]")]

    dataframe = dataframe[~dataframe.term.str.contains("<")]
    dataframe = dataframe[~dataframe.term.str.contains(">")]

    dataframe = dataframe.groupby("key").agg({"term": list}).reset_index()

    with open("results/abbreviations.txt", "w", encoding="utf-8") as file:
        for _, row in dataframe.iterrows():
            print(row["key"], file=file)
            for term in row["term"]:
                print(f"    {term}", file=file)


if __name__ == "__main__":
    main()
