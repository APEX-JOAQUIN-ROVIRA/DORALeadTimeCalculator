import os

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from github import Github
from github.PullRequest import PullRequest
from typing import List
from rich import print
from rich.console import Console
from rich.live import Live
import util

# This script calculates the average time a piece of code
# take to reach master, and therefore be pushed to production.
# The calculation take into account all pull requests in the last 6 months.

# Read environment variables from .env
# GH_TOKEN  GitHub account access token
# TARGETS   A comma separated list of values of the names of repositories to calculte
load_dotenv()


base_branch = "master"  # TODO: make configurable
targets = set(map(lambda v: v.strip(), os.environ.get("TARGETS").split(",")))
g = Github(os.environ.get("GH_TOKEN"))

# Gather target repo data
with Console().status(
    "[yellow]Fetching repository metadata from GitHub...", spinner="bouncingBar"
) as status:
    repos = list(filter(lambda f: f.name in targets, g.get_user().get_repos()))

six_months_ago = date.today() + relativedelta(months=-6)
print("%-20s %s" % ("Project", "Lead Time (days)"))

# Proceed with the calculate lead time for each repo
# We use rich.Live to give progress feedback to the user
for repo in repos:
    with Live(
        util.gather_pr_message(0, six_months_ago, repo.name),
        transient=True,
        refresh_per_second=4,
    ) as live:
        prs = repo.get_pulls(
            state="closed", sort="created_at", direction="desc", base=base_branch
        )
        relevant_prs: List[PullRequest] = []
        for pr in prs:
            if pr.created_at.date() <= six_months_ago:
                break
            if not pr.merged:
                continue
            relevant_prs.append(pr)
            live.update(
                util.gather_pr_message(len(relevant_prs), six_months_ago, repo.name)
            )

        # Calculate lead time for all relevant PRs
        lead_time: float = 0
        i = 0
        for pr in relevant_prs:
            live.update(
                util.calculate_lead_time_message(i, len(relevant_prs), repo.name)
            )
            # Get first commit date
            first_commit_date = datetime(9999, 1, 1)
            for commit in pr.get_commits():
                if commit.commit.committer.date < first_commit_date:
                    first_commit_date = commit.commit.committer.date
            # Keep track of total lead time
            lead_time += (pr.merged_at - first_commit_date).days
            i += 1

        lead_time /= len(relevant_prs)
        print("%-20s %16.2f" % (repo.name, lead_time))
