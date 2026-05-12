"""
GitHub Commit Stats

Fetches your commit activity from GitHub and prints a pretty stats table.

Dependencies:
    uv add requests rich python-dotenv

Setup:
    Create a .env file with:
        GITHUB_TOKEN=ghp_your_token

Usage:
    uv run git-average-commit.py

Config:
    Edit the time window:
        timedelta(days=60)

Notes:
    - Includes 0-commit days
    - Median = typical day
    - High std dev = bursty workflow

Security:
    If you leak your token → revoke it immediately.
"""


import requests
from datetime import datetime, timedelta, UTC
import statistics
import os

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv

console = Console()

load_dotenv()

# Token from env
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    console.print("[red]Error: Set GITHUB_TOKEN env variable[/red]")
    exit()

headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# Time range
to_date = datetime.now(UTC)
from_date = to_date - timedelta(days=60)

query = f"""
{{
  viewer {{
    contributionsCollection(from: "{from_date.isoformat()}", to: "{to_date.isoformat()}") {{
      contributionCalendar {{
        weeks {{
          contributionDays {{
            contributionCount
            date
          }}
        }}
      }}
    }}
  }}
}}
"""

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
)

data = response.json()

days = [
    day["contributionCount"]
    for week in data["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    for day in week["contributionDays"]
]

# Stats
avg = sum(days) / len(days)
median = statistics.median(days)
std_dev = statistics.stdev(days)
std_dev_pop = statistics.pstdev(days)
active_days = [d for d in days if d > 0]
activity_ratio = len(active_days) / len(days)
mad = statistics.median([abs(x - median) for x in days])
p90 = sorted(days)[int(0.9 * len(days))]
max_day = max(days)

# Table
table = Table(title="GitHub Commit Stats", show_lines=True)

table.add_column("Metric", style="cyan", no_wrap=True)
table.add_column("Value", justify="right", style="bold")

table.add_row("From", str(from_date.date()))
table.add_row("To", str(to_date.date()))
table.add_row("Average commits/day", f"{avg:.2f}")
table.add_row("Median commits/day", str(median))
table.add_row("Std dev (sample)", f"{std_dev:.2f}")
table.add_row("Std dev (population)", f"{std_dev_pop:.2f}")
table.add_row("Active day ratio", f"{activity_ratio:.2%}")
table.add_row("Max commits/day", str(max_day))
table.add_row("MAD", f"{mad:.2f}")
table.add_row("90th percentile", str(p90))

console.print(table)

# Simple interpretation panel
if avg > median * 2:
    pattern = "[yellow]Bursty workflow (spikes dominate)[/yellow]"
else:
    pattern = "[green]Consistent workflow[/green]"

panel = Panel(
    f"""
Median baseline: [bold]{median}[/bold] commits/day
High-intensity days (~p90): [bold]{p90}[/bold]
Activity ratio: [bold]{activity_ratio:.2%}[/bold]

Pattern: {pattern}
""",
    title="Interpretation",
)

console.print(panel)
