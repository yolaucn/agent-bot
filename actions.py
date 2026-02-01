import requests
import os
import yaml
from github import Github

# Load config
cfg = yaml.safe_load(open("config.yaml"))
    
token = cfg["github"]["token"]
repo_name = cfg["github"]["repo"]

if not token:
    raise ValueError("GITHUB_TOKEN not found in config")

def post_to_github(token, repo_name, title, content):
    g = Github(token)
    repo = g.get_repo(repo_name)
    issue = repo.create_issue(title=title, body=content)
    return {
        "post_id": issue.number,
        "title": title,
        "content": content,
        "status": "published"
    }