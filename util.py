from datetime import date


def gather_pr_message(n_gathered_prs: int, from_date: date, repo_name: str) -> str:
    return f"[yellow]{'%-5d' % n_gathered_prs} Gathering all closed Pull Requests since {from_date} for [bold]{repo_name}"


def calculate_lead_time_message(
    current_index: int, max_index: int, repo_name: str
) -> str:
    return f"[yellow]{current_index}/{max_index} Calculating lead time for [bold]{repo_name}"
