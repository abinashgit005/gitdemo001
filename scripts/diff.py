# check_abinash_changes.py
import re

diff_path = "tfvars_changes/full_diff.txt"

try:
    with open(diff_path) as f:
        lines = f.readlines()
except FileNotFoundError:
    print("No diff file found.")
    exit(1)

inside_abinash = False
collected = []

for i, line in enumerate(lines):
    stripped = line.strip()

    # Enter the abinash block
    if not inside_abinash and re.search(r'abinash\s*=\s*{', stripped):
        inside_abinash = True
        continue

    if inside_abinash:
        # Exit on closing brace
        if re.match(r'^[ +\-]*}', stripped):
            inside_abinash = False
            continue

        # Collect only added lines (starting with '+')
        if stripped.startswith('+'):
            collected.append(line)

# Output added lines only
if collected:
    print("✅ Added lines inside 'abinash' block:")
    for l in collected:
        print(l.strip())
else:
    print("🟢 No added lines in 'abinash' block.")
