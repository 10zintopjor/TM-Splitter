import csv
import os
from github import Github 


def get_contents(g, repo_name,bo_path,en_path):
    try:
        repo = g.get_repo(f"MonlamAI/{repo_name}")
        bo_contents = repo.get_contents(bo_path)
        en_contents = repo.get_contents(en_path)
        bo_text = bo_contents.decoded_content.decode()
        en_text = en_contents.decoded_content.decode()
        return bo_text,en_text
    except:
        print(f'{repo_name} Not Found')
        return None


def log(repo_name,bo_title,en_title):
    csv_file = "updated_tm.csv"
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([repo_name,en_title,bo_title])


if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    g = Github(token)
    with open('tm.txt', 'r') as file:
        repos = [line.strip() for line in file]
        for repo in repos:
            bo_path = f"./{repo}/bo.txt"
            en_path = f"./{repo}/en.txt"        
            bo_text,en_text = get_contents(g, repo,bo_path,en_path)
            bo_title = bo_text.split('\n')[0]
            en_title = en_text.split('\n')[0]
            log(repo,bo_title,en_title)
            break
            

    
            

