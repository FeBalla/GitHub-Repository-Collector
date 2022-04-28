from datetime import datetime
import os


class Logger:
  def __init__(self, folder_name="logs", encoding="utf-8"):
    self.folder_name = folder_name

    if not os.path.exists(self.folder_name):
      os.makedirs(self.folder_name)

    self.repositories_data_file = open(f"{self.folder_name}/repos.txt", "w", encoding=encoding)
    print("Repositories expected to clone:", file=self.repositories_data_file)

    self.runtime_logs_file = open(f"{self.folder_name}/runtime.txt", "w", encoding=encoding)
    print("Runtime logs:", file=self.runtime_logs_file)

  def save_repositories_data(self, repositories_data):
    '''Writes a log-file with all the information of the repositories that will be cloned'''
    repositories_data = sorted(repositories_data, key=lambda repo: repo['last_commit_date'])
    
    for repo in repositories_data:
      print(repo["name"], end=" ", file=self.repositories_data_file)
      print(repo["last_commit_sha"], end=" ", file=self.repositories_data_file)
      print(repo["last_commit_author"], end=" ", file=self.repositories_data_file)
      print(repo["last_commit_date"], file=self.repositories_data_file)

    self.repositories_data_file.flush()
    os.fsync(self.repositories_data_file.fileno())

  def write_runtime_log(self, msg):
    '''Writes a runtime-log (msg) in the log-file with the current time'''
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print(f"({current_time}){msg}", file=self.runtime_logs_file)
    self.runtime_logs_file.flush()
    os.fsync(self.runtime_logs_file.fileno())

  def finalize(self):
    '''Ends the logger handler, saving and closing the used files'''
    self.runtime_logs_file.close()
    self.repositories_data_file.close()
