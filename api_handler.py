from datetime import datetime, timedelta
from dotenv import dotenv_values
import requests

config = dotenv_values(".env")

BASE_URL = "https://github.com"
API_URL  = "https://api.github.com"

# The last commit date returned by GitHub API is in UTC timezone, so you can adjust it to another 
# timezone using this parameter. For GMT-4 the difference in april is around 4 hours. This is used 
# just for logs and does not affect anything else.
TIME_DIFF_TO_UTC = timedelta(hours=4)


def get_assignment_repos_names(REPOSITORY_PREFIX="", PER_PAGE=100, TOTAL_PAGES=2):
  '''Returns a set with the name of all private repositories from a organization that starts with a 
  specific prefix'''
  assignment_repos = set()

  for page in range(TOTAL_PAGES):
    url = f"{API_URL}/orgs/{config['ORGA']}/repos?type=private&per_page={PER_PAGE}&page={page + 1}"
    org_repos = requests.get(url, auth=(config["USER"], config["TOKEN"]))

    for repo in org_repos.json():
      if repo["name"].startswith(REPOSITORY_PREFIX):
        assignment_repos.add(repo["name"])

  return list(assignment_repos)


def get_repository_information(repository_name, REPOSITORY_PREFIX=""):
  '''Gets the repository information by name, including the last commit sha, the last commit date 
  and the standard url for cloning'''
  url = f"{API_URL}/repos/{config['ORGA']}/{repository_name}/commits"
  data = requests.get(url, auth=(config["USER"], config["TOKEN"])).json()[0]

  commit_date  = datetime.strptime(data["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
  commit_date -= TIME_DIFF_TO_UTC
  commit_date  = commit_date.strftime("%d/%m/%Y-%H:%M")

  repository_info = {
    "name": repository_name,
    "clone_url": f"{BASE_URL}/{config['ORGA']}/{repository_name}.git",
    "last_commit_sha": data["sha"],
    "last_commit_author": repository_name.replace(f"{REPOSITORY_PREFIX}-", ""),
    "last_commit_date": commit_date,
  }
  
  return repository_info
