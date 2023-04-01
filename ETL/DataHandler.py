
import os

import pandas as pd


def download_dataset(git_url:str, output_dir:str):
    """
    :param git_url: git base url for dataset
    :param output_dir: dir to download
    :return: None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    os.system(f"git clone {git_url} {output_dir}")


def read_text_file_and_process_df(text_file_path:str, output_path:str):
    """
    :param text_file_path: text file path
    :param output_path: output csv file path
    :return:
    """
    with open(text_file_path, 'r') as f:
        lines = f.read().split("\n")
        lines = [l.strip() for l in lines]

    tweets = []
    text = []
    lang = []
    tweet_id = None

    for line in lines:
        arr = " ".join(line.split()).split(" ")
        if len(arr) == 1:
            if arr[0] == '': # end of tweet
                tweets.append(
                    {
                        "tweet_id":tweet_id,
                        "text":text,
                        "lang":lang
                    }
                )
                text = []
                lang = []
            else:
                tweet_id = arr[0]
        else:
            text.append(arr[0])
            lang.append(arr[1])

    if len(text) > 1:
        tweets.append(
            {
                "tweet_id": tweet_id,
                "text": text,
                "lang": lang
            }
        )

    df = pd.DataFrame(tweets)
    if not output_path.endswith(".csv"):
        output_path = f"{output_path}.csv"
    df.to_csv(output_path)