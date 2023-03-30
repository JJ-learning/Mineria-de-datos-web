import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

if __name__ == "__main__":

    github_url = "https://github.com/search?q=python"

    req = requests.get(github_url)

    soup = BeautifulSoup(req.content, "html5lib")

    final_df_github = pd.DataFrame(
        columns=["nombre", "num_estrellas", "num_issues", "num_forks"]
    )

    names = []
    num_starts = []
    refs = []

    for row_name, row_starts in zip(
        soup.findAll(
            "div",
            attrs={"class": "f4 text-normal"},
        ),
        soup.findAll(
            "div",
            attrs={"class": "d-flex flex-wrap text-small color-fg-muted"},
        ),
    ):

        names.append(row_name.a.text)
        num_starts.append(row_starts.a.text.strip())
        refs.append(
            json.loads(row_name.a["data-hydro-click"])["payload"]["result"]["url"]
        )

    num_forks = []
    num_issues = []

    for url in refs:

        req = requests.get(url)

        soup = BeautifulSoup(req.content, "html5lib")

        num_forks.append(soup.find("span", attrs={"id": "repo-network-counter"}).text)

        num_issues.append(soup.find("span", attrs={"id": "issues-repo-tab-count"}).text)

    final_df_github["nombre"] = names
    final_df_github["num_estrellas"] = num_starts
    final_df_github["num_issues"] = num_issues
    final_df_github["num_forks"] = num_forks