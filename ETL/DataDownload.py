
import os


def download_dataset(git_url:str, output_dir:str):
    """
    :param git_url: git base url for dataset
    :param output_dir: dir to download
    :return: None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    os.system(f"git clone {git_url} {output_dir}")