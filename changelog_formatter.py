import csv
import os

version = input("Please enter the version: ").strip()
out = os.path.join(os.path.dirname(__file__), f"CHANGELOG_{version}.md")

base_commits = {
    "Main": "https://github.com/FunkinCrew/Funkin/commit/",
    "Assets": "https://github.com/FunkinCrew/funkin.assets/commit/"
}

base_pulls = {
    "Main": "https://github.com/FunkinCrew/Funkin/pull/",
    "Assets": "https://github.com/FunkinCrew/funkin.assets/pull/"
}

sections = {
    "Added": {"Assets": [], "Main": []},
    "Changed": {"Assets": [], "Main": []},
    "Fixed": {"Assets": [], "Main": []},
    "Removed": {"Assets": [], "Main": []}
}

new_contributors = []

# Use absolute path for sheet.csv
sheet_path = os.path.join(os.path.dirname(__file__), "sheet.csv")

with open(sheet_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get("Version", "").strip() != version:
            continue

        desc = row.get("Entry Description", "").strip()
        t = row.get("Type", "").strip()
        author = row.get("Author", "").strip()
        pr = row.get("PR #", "").strip()
        repo = row.get("Repo", "").strip()
        commit = row.get("Commit Hash", "").strip()
        is_new = row.get("New?", "").strip() == "Yes"

        if not desc or not commit or t not in sections:
            continue

        short = commit[:7]
        commit_url = base_commits.get(repo, base_commits["Main"]) + commit
        pr_url = base_pulls.get(repo, base_pulls["Main"]) + pr

        if repo == "Assets":
            line = f"- {desc} ([{short}]({commit_url})) - by @{author} in [funkin.assets#{pr}]({pr_url})"
        else:
            line = f"- {desc} ([{short}]({commit_url})) - by @{author} in [#{pr}]({pr_url})"

        sections[t][repo if repo in sections[t] else "Main"].append(line)

        if is_new and author not in [contributor[0] for contributor in new_contributors]:
            if repo == "Assets":
                new_contributors.append((author, pr, pr_url, "funkin.assets"))
            else:
                new_contributors.append((author, pr, pr_url, repo))

with open(out, "w", encoding="utf-8") as f:
    for name in ["Added", "Changed", "Fixed", "Removed"]:
        assets = sections[name]["Assets"]
        main = sections[name]["Main"]
        if not assets and not main:
            continue

        f.write(f"## {name}\n\n")
        for l in sorted(main):
            f.write(l + "\n")
        for l in sorted(assets):
            f.write(l + "\n")
        f.write("\n")

    if new_contributors:
        sorted_contributors = sorted(new_contributors, key=lambda x: x[3] != "Main")
        f.write(f"## New Contributors for {version}\n\n")
        for author, pr, pr_url, repo in sorted_contributors:
            if repo == "funkin.assets":
                f.write(f"* @{author} made their first contribution in [funkin.assets#{pr}]({pr_url})\n")
            else:
                f.write(f"* @{author} made their first contribution in [#{pr}]({pr_url})\n")

    print(f"CHANGELOG for version {version} has been generated and saved to {out}")