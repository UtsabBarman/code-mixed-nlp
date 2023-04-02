import os

import pandas as pd
import numpy as np
import random
from tqdm import tqdm
from Utils.CommonUtils import normalize_token


def download_dataset(git_url: str, output_dir: str):
    """
    :param git_url: git base url for dataset
    :param output_dir: dir to download
    :return: None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    os.system(f"git clone {git_url} {output_dir}")


def read_text_file_and_process_df(text_file_path: str, output_path: str):
    """
    :param text_file_path: text file path
    :param output_path: output csv file path
    :return:
    """
    with open(text_file_path, "r") as f:
        lines = f.read().split("\n")
        lines = [l.strip() for l in lines]

    tweets = []
    text = []
    lang = []
    tweet_id = None

    for line in lines:
        arr = " ".join(line.split()).split(" ")
        if len(arr) == 1:
            if arr[0] == "":  # end of tweet
                tweets.append({"tweet_id": tweet_id, "text": text, "lang": lang})
                text = []
                lang = []
            else:
                tweet_id = arr[0]
        else:
            text.append(arr[0])
            lang.append(arr[1])

    if len(text) > 1:
        tweets.append({"tweet_id": tweet_id, "text": text, "lang": lang})

    df = pd.DataFrame(tweets)
    if not output_path.endswith(".csv"):
        output_path = f"{output_path}.csv"
    df.to_csv(output_path)


def convert_data_set_xy(
    df_dataset: pd.DataFrame, df_word_list: pd.DataFrame, max_len: int = 50
):
    words = df_word_list.unique_word_types.tolist()
    words.sort()
    words.insert(0, "_pad_")
    langs = ["_pad_", "en", "hi", "rest"]
    dataset = []
    for ix, row in tqdm(df_dataset.iterrows()):
        tid = row["tweet_id"]
        text = [normalize_token(x=t) for t in eval(row["text"])]
        text = [words.index(x) for x in text]
        lang = [langs.index(x) for x in eval(row["lang"])]
        r = max_len - len(text)
        if r >= 1:  # pre padding with '_pad_'
            temp = [0] * r
            text = temp + text
            lang = temp + lang
        else:
            text = text[:max_len]
            lang = lang[:max_len]

        dataset.append({"id": str(tid), "x": text, "y": lang})
    return dataset


def get_n_fold(num_of_fold: int, dataset: list):
    """
    :param num_of_fold: number of fold
    :param dataset: dataset
    :return: data dict
    """
    data_dict = {(i + 1): None for i in range(num_of_fold)}
    dataset_idx = [i for i in range(len(dataset))]
    items_per_fold = int(len(dataset) / float(num_of_fold))
    for i in range(num_of_fold):
        test_idx = random.sample(range(0, len(dataset) - 1), items_per_fold)
        train_idx = [x for x in dataset_idx if x not in test_idx]
        data_dict[(i + 1)] = {
            "train": [dataset[z] for z in train_idx],
            "test": [dataset[z] for z in test_idx],
        }
    return data_dict
