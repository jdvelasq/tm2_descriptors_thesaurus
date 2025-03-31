"""Create a list of common hypened words."""

import pandas as pd  # type: ignore
import glob



DIR_PATH = (
    "/Users/jdvelasq/Library/Mobile Documents/com~apple~CloudDocs/_tm2_descriptors/"
)

def load_raw_csv_files_as_df():
    """Load raw CSV files as dataframes."""
    files = glob.glob(DIR_PATH + "raw/*.csv")
    data_frames = [pd.read_csv(file) for file in files]
    data_frame = pd.concat(data_frames)
    data_frame = data_frame.drop_duplicates()
    data_frame = data_frame.reset_index(drop=True)
    return data_frame



def process_keywords(keywords):
    
    # process the keywords:
    keywords = keywords.str.split("; ")
    keywords = keywords.explode()
    keywords = keywords.str.strip()
    keywords = keywords.str.lower()

    # process the words:
    words = keywords.str.split(" ")
    words = words.explode()
    words = words.str.strip()
    words = words.str.replace('"', "")
    words = words.str.replace("'", "")

    words = words[words.str.len() > 0]

    # compute occ:
    words = words.rename("word")
    words = pd.DataFrame(words)
    words["occ"] = 1
    words = words.groupby("word", as_index=False).agg({"occ": "sum"})   

    # separate hypened and non-hypened words:
    hypened_words = words[words.word.str.contains("-")].sort_values("occ", ascending=False)
    non_hypened_words = words[~words.word.str.contains("-")].sort_values("occ", ascending=False)
    
    # to remove misspelled words:
    hypened_words = hypened_words[hypened_words.occ > 2]
    hypened_words = hypened_words[hypened_words.word.str.len() > 3]

    # select hypened words:
    hypened_words = hypened_words[hypened_words.occ > 3]
    hypened_words = hypened_words[hypened_words.word.apply(lambda x: x.replace("-", "").isalpha())]
    hypened_words = hypened_words[hypened_words.word.apply(lambda x: x.replace("-", "") in non_hypened_words.word.to_list())]
    hypened_words = hypened_words[hypened_words.word.apply(lambda x: x[0] != "-" and x[-1] != "-")]

    return hypened_words

    

def run():
    data_frame = load_raw_csv_files_as_df()
    data_frame  = data_frame[["Author Keywords", "Index Keywords"]]
    data_frame = data_frame.dropna()
    data_frame = data_frame.reset_index(drop=True)


    # print(data_frame.head())
    df1 = process_keywords(data_frame["Author Keywords"])
    df2 = process_keywords(data_frame["Index Keywords"])

    hypened_words = pd.concat([df1, df2])
    hypened_words = hypened_words.drop_duplicates(subset="word")
    hypened_words = hypened_words.sort_values("word", ascending=True)
    hypened_words = hypened_words.reset_index(drop=True)

    hypened_words = hypened_words.word.str.upper()

    with open("hypened_words.txt", "w") as f:
        for word in hypened_words:
            f.write(word + "\n")

    

if __name__ == "__main__":
    run()