import uuid
from pathlib import Path
from openpecha.github_utils import github_publish
import os 
import csv
import time
import random
import string

token = os.getenv("GITHUB_TOKEN")
home_path = "data"

def get_four_digit_uuid():
    characters = string.ascii_uppercase + string.digits
    random_id = ''.join(random.choices(characters, k=4))
    return random_id


def get_pairs(main_dir):
    files = list(Path(main_dir).iterdir())
    return sorted(files) 


def log(row, csv_file):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def create_tm_repo(file):
    bo_text = Path(file / "bo.txt").read_text(encoding="utf-8")
    en_text = Path(file / "en.txt").read_text(encoding="utf-8")
    uuid = get_four_digit_uuid()
    repo_path = f"{home_path}/TM{uuid}_LH"
    Path(repo_path).mkdir()
    Path(f"{repo_path}/bo.txt").write_text(bo_text)
    Path(f"{repo_path}/en.txt").write_text(en_text)
    github_publish(
        path=repo_path,
        org="MonlamAI",
        not_includes=[],
        token = token
    )

    log(f"TM{uuid}_LH","tm.csv")


def create_tp_repo(file):
    bo_text = Path(file / "bo.txt").read_text(encoding="utf-8")
    en_text = Path(file / "en.txt").read_text(encoding="utf-8")
    uuid = get_four_digit_uuid()
    bo_repo_path = f"{home_path}/BO{uuid}_LH"
    en_repo_path = f"{home_path}/EN{uuid}_LH"
    Path(bo_repo_path).mkdir()
    Path(en_repo_path).mkdir()
    Path(f"{bo_repo_path}/bo.txt").write_text(bo_text)
    Path(f"{en_repo_path}/en.txt").write_text(en_text)
    github_publish(path=bo_repo_path,org="MonlamAI",not_includes=[],token=token)
    github_publish(path=en_repo_path,org="MonlamAI",not_includes=[],token=token)
    row = [f"EN{uuid}_LH",f"BO{uuid}_LH",en_text.split('\n')[0],bo_text.split('\n')[0]]
    log(row,"tp.csv")


def main(home_dir):
    files  = get_pairs(home_dir)
    do = False
    for file in files:
        if file.as_posix() == "lotsawa_house_text_pairs/TM00006":
            do = True
        if do:    
            print(file)
            create_tp_repo(file)
            time.sleep(20)


if __name__ == "__main__":
    path = "lotsawa_house_text_pairs"
    main(path)
