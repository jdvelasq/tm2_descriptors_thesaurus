"""Sort"""

import re


def _load_file(file_path):

    with open(file_path, "rt", encoding="utf-8") as file:
        return file.readlines()


def _save_file(file_path, data):

    with open(file_path, "wt", encoding="utf-8") as file:
        file.writelines(data)


def _main():

    for file in [
        "results/raw_starting_words.txt",
        "results/raw_ending_words.txt",
        # "results/hypened_words.txt",
    ]:

        words = _load_file(file)
        # words = [w.replace("_", "-") for w in words]

        # words = sorted(set(words), key=lambda x: "{:03d}".format(len(x)) + x)
        words = sorted(set(words), key=lambda x: x)
        _save_file(file, words)


if __name__ == "__main__":
    _main()
