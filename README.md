# GitHub Classroom Collector
It's a simple Python script to collect all **private** repositories from a GitHub Organization. Is intended to be used for downloading all the submissions of a GitHub Classroom assignment, getting information like last commit date.

## How to use?
1. First of all, you need to install all the dependencies specified in `requirements.txt`. You can use:
```bash
pip install -r requirements.txt
```

2. Now you need to create a `.env` file like [example.env](./example.env):
- `PREFIX`: Sets a prefix for the repositories name. This is usefull to download only repositories from a specific assignment.
- `TOKEN`: Here you need to use a [personal access token](https://docs.github.com/es/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for your GitHub account.
- `USER`: Sets the username of your's GitHub account.
- `ORGA`: Sets the organization's name where the repositories are located.
- `PER_PAGE`: Represents how many repositories you want to get from a single API call (it works paginated). You can use 100 as default.
- `PAGES`: Represents how many pages of size _PER_PAGE_ will be called to GitHub API. For example, if you have 500 repositories and _PER_PAGE=100_, then _PAGES_ should be 5. However, if you don't want to overthink, just set a higher value and it only will take a little longer.

3. Run the [main.py](./main.py) module and wait until all the repositories are downloaded.

## Logs
Once the execution started, will be created a directory with 2 files:
- `repos.txt`: Has the information of the repositories that will be cloned. Each line has the following format:
```txt
repository-name last-commit-sha last-commit-author last-commit-date
```

- `runtime.txt`: Has the runtime logs with the clone results for each repository.

