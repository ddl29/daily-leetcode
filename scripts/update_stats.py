import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import date
import subprocess
import re
from pathlib import Path

# CSV path
CSV_FILE = Path("problems.csv")
CHARTS_DIR = Path("charts")
CHARTS_DIR.mkdir(exist_ok=True)

# Walk through the repo and find the latest file added
for file_path in Path(".").rglob("*.*"):
    if file_path.suffix not in [".js", ".py", ".java"]:
        continue
    if "scripts" in file_path.parts:  # skip files inside scripts folder
        continue
    # Here you could filter to only new files pushed if needed

    # Extract metadata
    problem_name = " ".join(word.capitalize() for word in file_path.stem.split("_"))
    difficulty = file_path.parent.name.capitalize()
    topic = file_path.parent.parent.name.capitalize()
    language = {"js":"JavaScript","py":"Python","java":"Java"}[file_path.suffix[1:]]
    commit_msg = subprocess.getoutput(f'git log -1 --pretty=%B "{file_path}"')
    today = date.today().isoformat()

    # Append to CSV
    if CSV_FILE.exists():
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["Date","Problem","Link","Difficulty","Topic","Language"])

    # Avoid duplicates
    if problem_name not in df["Problem"].values:
        df = pd.concat([df, pd.DataFrame([{
            "Date": today,
            "Problem": problem_name,
            "Link": commit_msg,
            "Difficulty": difficulty,
            "Topic": topic,
            "Language": language
        }])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

# Generate charts
df = pd.read_csv(CSV_FILE)
# Difficulty pie
df['Difficulty'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#8ecae6','#219ebc','#023047'])
plt.title('Problems by Difficulty')
plt.savefig(CHARTS_DIR / "difficulty_pie.png")
plt.close()

# Topic bar
df['Topic'].value_counts().plot.bar(color='#fb8500')
plt.title('Problems by Topic')
plt.savefig(CHARTS_DIR / "topics_bar.png")
plt.close()

# Update README total problems solved count
readme_file = Path("README.md")
readme_text = readme_file.read_text()

total_problems = len(df)

# This regex matches the line starting with "- Total problems solved:" and bold number
pattern = r"^(\s*-\s*Total problems solved:\s*\*\*)\d+(\*\*)"

# Use lambda to safely replace the number
readme_text = re.sub(
    pattern,
    lambda m: f"{m.group(1)}{total_problems}{m.group(2)}",
    readme_text,
    flags=re.MULTILINE
)

readme_file.write_text(readme_text)