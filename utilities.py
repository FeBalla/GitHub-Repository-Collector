from datetime import datetime
from dotenv import dotenv_values
from dateutil import tz
import requests

config = dotenv_values(".env")
BASE_URL = "https://github.com"
API_URL = "https://api.github.com"


def get_assignment_repos_names(repository_prefix="", per_page=100, total_pages=2):
  '''Gets names of all private repositories from a organization starting with `repository_prefix`'''
  assignment_repos = set()

  for page in range(total_pages):
    url = f"{API_URL}/orgs/{config['ORGA']}/repos?type=private&per_page={per_page}&page={page + 1}"
    org_repos = requests.get(url, auth=(config["USER"], config["TOKEN"]))

    for repo in org_repos.json():
      if repo["name"].startswith(repository_prefix):
        assignment_repos.add(repo["name"])

  return list(assignment_repos)


def get_last_commit_date(commit_data):
  '''Gets the last commit date in local time (GitHub API returns it in UTC)'''
  commit_date = datetime.strptime(commit_data["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
  commit_date = commit_date.replace(tzinfo=tz.tzutc())
  commit_date = commit_date.astimezone(tz.tzlocal())
  commit_date = commit_date.strftime("%d/%m/%Y-%H:%M")

  return commit_date


def get_repository_information(repository_name, repository_prefix=""):
  '''Gets information for a specific repository'''
  url = f"{API_URL}/repos/{config['ORGA']}/{repository_name}/commits"
  data = requests.get(url, auth=(config["USER"], config["TOKEN"])).json()[0]

  repository_info = {
    "name": repository_name,
    "clone_url": f"{BASE_URL}/{config['ORGA']}/{repository_name}.git",
    "last_commit_sha": data["sha"],
    "last_commit_author": repository_name.replace(f"{repository_prefix}-", ""),
    "last_commit_date": get_last_commit_date(data),
  }

  return repository_info
