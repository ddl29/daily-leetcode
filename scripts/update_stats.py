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


# Read CSV
df = pd.read_csv(CSV_FILE)

# -------------------------------
# Difficulty Pie Chart
# -------------------------------
# Ensure all difficulties are included even if count is 0
difficulty_order = ['Easy', 'Medium', 'Hard']
df['Difficulty'] = pd.Categorical(df['Difficulty'], categories=difficulty_order)
difficulty_counts = df['Difficulty'].value_counts().sort_index()

plt.figure(figsize=(5,5))  # square figure for pie
difficulty_counts.plot.pie(
    autopct='%1.1f%%',
    colors=['#8ecae6', '#219ebc', '#023047'],
    startangle=90
)
plt.title('Problems by Difficulty')
plt.ylabel('')  # remove default ylabel
plt.tight_layout()
plt.savefig(CHARTS_DIR / "difficulty_pie.png")
plt.close()

# -------------------------------
# Topic Bar Chart
# -------------------------------
# Sort topics alphabetically or by your preferred order
topic_counts = df['Topic'].value_counts().sort_index()
plt.figure(figsize=(6,4))
topic_counts.plot.bar(color='#fb8500')
plt.title('Problems by Topic')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "topics_bar.png")
plt.close()



# Update README total problems solved count
readme_file = Path("README.md")
readme_text = readme_file.read_text()

total_problems = len(df)

# Match line starting with "# Total problems solved:" and any number
pattern = r"^# Total problems solved: \d+"

# Replace with current total
readme_text = re.sub(pattern, f"# Total problems solved: {total_problems}", readme_text, flags=re.MULTILINE)

readme_file.write_text(readme_text)