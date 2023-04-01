
import os
import argparse
from ETL.DataDownload import download_dataset
from Utils.CommonUtils import load_json

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment_config', help='experiment config.json', default="./exp_config.json")
    args = parser.parse_args()

    exp_config = load_json(args.experiment_config)

    dataset_path = os.path.join(
        exp_config.get("data", "./data").get("dataset_dir", None),
        exp_config.get("data", "./data").get("dataset_git_file_path", None)
    )
    if not os.path.exists(dataset_path):
        download_dataset(
            git_url=exp_config.get("data").get("dataset_git_url"),
            output_dir=exp_config.get("data", "./data").get("dataset_dir", None),
        )
