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

        df["Abstract"] = df["Abstract"].map(
            lambda x: pd.NA if x.upper() == "[NO ABSTRACT AVAILABLE]" else x
        )
        #
        for col in ["Title", "Abstract", "Author Keywords", "Index Keywords"]:

            df[col] = df[col].astype(str).str.lower()
            df[col] = df[col].str.replace("’", "'", regex=False)
            #
            if col not in ["Author Keywords", "Index Keywords"]:
                df[col] = df[col].str.replace(";", ".", regex=False)
            #
            df[col] = df[col].str.replace(r"(", r" ( ", regex=False)  # (
            df[col] = df[col].str.replace(r")", r" ) ", regex=False)  # )
            df[col] = df[col].str.replace(r"$", r" $ ", regex=False)  # $
            df[col] = df[col].str.replace(r"/", r" / ", regex=False)  # /
            df[col] = df[col].str.replace(r"?", r" ? ", regex=False)  # ?
            df[col] = df[col].str.replace(r"¿", r" ¿ ", regex=False)  # ?
            df[col] = df[col].str.replace(r"!", r" ! ", regex=False)  # !
            df[col] = df[col].str.replace(r"¡", r" ¡ ", regex=False)  # ¡
            df[col] = df[col].str.replace(r"=", r" = ", regex=False)  # =
            df[col] = df[col].str.replace(r'"', r' " ', regex=False)  # "
            df[col] = df[col].str.replace(r":", r" : ", regex=False)  # :
            df[col] = df[col].str.replace(r"%", r" % ", regex=False)  # %
            #
            df[col] = df[col].str.replace(r"(\w+)(,\s)", r"\1 \2", regex=True)  # ,
            df[col] = df[col].str.replace(r"(\')(,\s)", r"\1 \2", regex=True)  # ,
            df[col] = df[col].str.replace(r"(\w+)(\.\s)", r"\1 \2", regex=True)  # .
            df[col] = df[col].str.replace(r"(\w+)\.$", r"\1 .", regex=True)  # .
            #
            df[col] = df[col].str.replace(r"(\w+)'s(\b)", r"\1\2", regex=True)  # 's
            df[col] = df[col].str.replace(r"(\w+)'(\s)", r"\1\2", regex=True)  # s
            #
            df[col] = df[col].str.replace("'", "", regex=False)

            df[col] = (
                df[col]
                .str.normalize("NFKD")
                .str.encode("ascii", errors="ignore")
                .str.decode("utf-8")
            )

            df[col] = (
                df[col].str.replace(r"\s+", r" ", regex=True).str.strip()
            )  # multiple spaces

        #
        df.to_csv(filename, index=False, compression="zip")


if __name__ == "__main__":
    process_data()
