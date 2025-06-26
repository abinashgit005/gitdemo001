# check_abinash_changes.py
import re

diff_path = "tfvars_changes/full_diff.txt"

try:
    with open(diff_path) as f:
        lines = f.readlines()
except FileNotFoundError:
    print("No diff file found.")
    exit(1)

inside_block = False
collected = []

for line in lines:
    # Start of abinash block
    if re.match(r'^[+-]\s*abinash\s*=\s*{', line):
        inside_block = True
        collected.append(line)
        continue

    if inside_block:
        # End of block
        if re.match(r'^[+-]\s*}', line):
            collected.append(line)
            inside_block = False
        elif line.startswith("+") or line.startswith("-"):
            collected.append(line)

# Print changes (if any)
if collected:
    print("Detected changes in 'abinash' block:")
    for l in collected:
        print(l.strip())
else:
    print("No changes in 'abinash' block.")
