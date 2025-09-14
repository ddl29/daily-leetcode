import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import date
import subprocess
import re

# Paths
CSV_FILE = Path("problems.csv")
CHARTS_DIR = Path("charts")
CHARTS_DIR.mkdir(exist_ok=True)

# Collect problems
for file_path in Path(".").rglob("*.*"):
    if file_path.suffix not in [".js", ".py", ".java"]:
        continue
    if "scripts" in file_path.parts:  # skip files inside scripts folder
        continue

    # Extract difficulty from folder
    if file_path.parts[0] not in ["Easy", "Medium", "Hard"]:
        continue
    difficulty = file_path.parts[0]

    # Extract problem number + name
    stem = file_path.stem  # e.g. "1_two_sum"
    parts = stem.split("_", 1)
    problem_number = parts[0]
    problem_name = (
        parts[1].replace("_", " ").title() if len(parts) > 1 else f"Problem {problem_number}"
    )

    # Language
    language = {"js": "JavaScript", "py": "Python", "java": "Java"}[file_path.suffix[1:]]

    # Get commit message for this file
    commit_msg = subprocess.getoutput(f'git log -1 --pretty=%B "{file_path}"')

    # Extract hashtags (topics)
    topics = re.findall(r"#(\w+)", commit_msg)
    topics_str = ";".join(topics) if topics else ""

    today = date.today().isoformat()

    # Load or create CSV
    if CSV_FILE.exists():
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(
            columns=["Date", "ProblemNumber", "ProblemName", "Difficulty", "Topics", "Language", "CommitMessage"]
        )

    # Avoid duplicates by problem number
    if int(problem_number) not in df["ProblemNumber"].values:
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [
                        {
                            "Date": today,
                            "ProblemNumber": int(problem_number),
                            "ProblemName": problem_name,
                            "Difficulty": difficulty,
                            "Topics": topics_str,
                            "Language": language,
                            "CommitMessage": commit_msg.strip(),
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )
        df.to_csv(CSV_FILE, index=False)

# Read CSV again for charts
df = pd.read_csv(CSV_FILE)

# -------------------------------
# Difficulty Pie Chart
# -------------------------------
difficulty_order = ["Easy", "Medium", "Hard"]
df["Difficulty"] = pd.Categorical(df["Difficulty"], categories=difficulty_order)
difficulty_counts = df["Difficulty"].value_counts().sort_index()

plt.figure(figsize=(5, 5))
difficulty_counts.plot.pie(
    autopct="%1.1f%%",
    colors=["#8ecae6", "#219ebc", "#023047"],
    startangle=90,
)
plt.title("Problems by Difficulty")
plt.ylabel("")
plt.tight_layout()
plt.savefig(CHARTS_DIR / "difficulty_pie.png")
plt.close()

# -------------------------------
# Line Chart of Cumulative Solves
# -------------------------------
df["Date"] = pd.to_datetime(df["Date"])
df_sorted = df.sort_values("Date")
df_sorted["Cumulative"] = range(1, len(df_sorted) + 1)

plt.figure(figsize=(6, 4))
plt.plot(df_sorted["Date"], df_sorted["Cumulative"], marker="o")
plt.title("Cumulative Problems Solved Over Time")
plt.xlabel("Date")
plt.ylabel("Total Solved")
plt.tight_layout()
plt.savefig(CHARTS_DIR / "cumulative_line.png")
plt.close()

# -------------------------------
# Update README
# -------------------------------
readme_file = Path("README.md")
if readme_file.exists():
    readme_text = readme_file.read_text()
else:
    readme_text = "# Daily LeetCode Practice 🧑‍💻\n\n## Total problems solved: 0\n"

total_problems = len(df)

# -------------------------------
# Update total problems solved
# -------------------------------
pattern_total = r"^## Total problems solved: \d+"
if re.search(pattern_total, readme_text, flags=re.MULTILINE):
    readme_text = re.sub(pattern_total, f"## Total problems solved: {total_problems}", readme_text, flags=re.MULTILINE)
else:
    readme_text = f"## Total problems solved: {total_problems}\n\n" + readme_text

# -------------------------------
# Prepare checklist for HTML table
# -------------------------------
all_topics = sorted(set(";".join(df["Topics"].dropna()).split(";")) - {""})
checklist_html = "\n".join([f"- [x] {t}" for t in all_topics])

# -------------------------------
# Update table cell or insert table if missing
# -------------------------------
pattern_table_cell = r"(<td>\s*## Topics Covered\s*)(.*?)(\s*</td>)"

if re.search(pattern_table_cell, readme_text, flags=re.S):
    # Replace only the checklist inside the Topics cell
    readme_text = re.sub(pattern_table_cell, rf"\1{checklist_html}\3", readme_text, flags=re.S)
else:
    # Insert table at the top after total problems
    table_html = f"""
<table>
<tr>
<td>

![Difficulty Pie](charts/difficulty_pie.png)

</td>
<td>

## Topics Covered
{checklist_html}

</td>
</tr>
</table>
"""
    # Insert table after the total problems line
    readme_text = re.sub(pattern_total, f"## Total problems solved: {total_problems}\n\n{table_html}", readme_text, flags=re.MULTILINE)

# -------------------------------
# Write updated README
# -------------------------------
readme_file.write_text(readme_text)
