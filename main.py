import os
from dotenv import dotenv_values
from git import Repo, rmtree
from utilities import get_assignment_repos_names, get_repository_information
from logger import Logger

config = dotenv_values(".env")
SAVE_DIR = os.path.join("..", config["PREFIX"])

if __name__ == "__main__":
  CLONED = 0
  FAILED = 0

  print("(1/6) Initializing")
  logger = Logger()

  print(f"(2/6) Getting repositories list from {config['ORGA']} with prefix: {config['PREFIX']}")
  repo_names = get_assignment_repos_names(config["PREFIX"], int(config["PER_PAGE"]), int(config["PAGES"]))

  print("(3/6) Getting repositories data")
  repositories_data = [get_repository_information(name, config["PREFIX"]) for name in repo_names]

  print("(4/6) Saving repositories data")
  logger.save_repositories_data(repositories_data)

  if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

  print("(5/6) Cloning repositories")
  for repo in repositories_data:
    try:
      cloned_repo = Repo.clone_from(repo["clone_url"], os.path.join(SAVE_DIR, repo["name"]), no_checkout=True)
      cloned_repo.git.checkout(repo["last_commit_sha"])
      rmtree(os.path.join(SAVE_DIR, repo["name"], ".git"))

      logger.write_runtime_log(f"Cloned succesfully: {repo['name']}")
      CLONED += 1
    except Exception:
      logger.write_runtime_log(f"Couldn't clone: {repo['name']}")
      FAILED += 1

  logger.finalize()

  print("(6/6) Process completed")
  print(f"- Cloned: {CLONED}")
  print(f"- Failed: {FAILED}")
