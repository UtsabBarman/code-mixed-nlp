
import os
import sys
import json
import argparse

import pandas as pd

from ETL.DataHandler import download_dataset, read_text_file_and_process_df, convert_data_set_xy
from Utils.CommonUtils import load_json

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment_config', help='experiment config.json', default="./exp_config.json")
    args = parser.parse_args()

    exp_config = load_json(args.experiment_config)

    dataset_file_path = os.path.join(
        exp_config.get("data", "./data").get("dataset_dir", None),
        exp_config.get("data", "./data").get("dataset_git_file_path", None)
    )
    if not os.path.exists(dataset_file_path):    # dataset download
        download_dataset(
            git_url=exp_config.get("data").get("dataset_git_url"),
            output_dir=exp_config.get("data", "./data").get("dataset_dir", None),
        )
    else:
        read_text_file_and_process_df(
            text_file_path=dataset_file_path,
            output_path=os.path.join(
                exp_config.get("data", "./data").get("dataset_dir", None),
                "code-mixed-lid-dataset"
            )
        )

    expanded_csv_path = os.path.join(
            exp_config.get("data", "./data").get("dataset_dir", None),
            exp_config.get("data").get("dataset_csv", None)
    )
    word_file_path = os.path.join(
            exp_config.get("data", "./data").get("dataset_dir", None),
            exp_config.get("data").get("word_file", None)
    )
    if not os.path.exists(expanded_csv_path) and not os.path.exists(word_file_path):  # if processed files are not present
        print(" Open Jupyter notebook and run Notebooks/Data_visualization.ipynb to get the data")
        sys.exit(0)
    else:
        expanded_df = pd.read_csv(expanded_csv_path, index_col=0)
        word_df = pd.read_csv(word_file_path, index_col=0)
        dataset = convert_data_set_xy(df_dataset=expanded_df, df_word_list=word_df)
        data_json_path = os.path.join(
            exp_config.get("data", "./data").get("dataset_dir", None),
            exp_config.get("data").get("dataset_xy_json", None)
        )
        with open(data_json_path, 'w') as jf:
            json.dump(dataset, jf)