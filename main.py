from github_api_handler import get_assignment_repos_names, get_repository_information
from dotenv import dotenv_values
from git import Repo, rmtree
from logger import Logger
import os

config = dotenv_values(".env")

BASE_SAVE_DIR = f"../{config['PREFIX']}"
PER_PAGE = 100
PAGES    = 3


if __name__ == "__main__":
  cloned = 0
  failed = 0

  print("(1/6) Initializing")
  logger = Logger()

  print(f"(2/6) Getting repositories names from {config['ORGA']} with prefix: {config['PREFIX']}")
  repo_names = get_assignment_repos_names(config["PREFIX"], PER_PAGE, PAGES)

  print("(3/6) Getting repositories data")
  repositories_data = [get_repository_information(name, config["PREFIX"]) for name in repo_names]

  print("(4/6) Saving repositories data")
  logger.save_repositories_data(repositories_data)

  if not os.path.exists(BASE_SAVE_DIR):
    os.makedirs(BASE_SAVE_DIR)

  print("(5/6) Cloning repositories")
  for repo in repositories_data:
    try:
      cloned_repo = Repo.clone_from(repo["clone_url"], f"{BASE_SAVE_DIR}/{repo['name']}", no_checkout=True)
      cloned_repo.git.checkout(repo["last_commit_sha"])
      rmtree(f"{BASE_SAVE_DIR}/{repo['name']}/.git")

      logger.write_runtime_log(f"Cloned succesfully: {repo['name']}")
      cloned += 1
    except:
      logger.write_runtime_log(f"Couldn't clone: {repo['name']}")
      failed += 1

  logger.finalize()

  print("(6/6) Process completed")
  print(f"- Cloned: {cloned}")
  print(f"- Failed: {failed}")
