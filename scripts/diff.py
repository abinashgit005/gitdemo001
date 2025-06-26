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
    # Remove newline and trailing spaces
    stripped = line.strip()

    # Track unmodified context lines to enter the abinash block
    if not inside_abinash:
        if re.search(r'abinash\s*=\s*{', stripped):
            inside_abinash = True
            # Search backward to include context
            context_start = i
            while context_start > 0 and not lines[context_start].strip().endswith('{'):
                context_start -= 1
            collected.append(f"# Context start at line {context_start}")
            continue

    if inside_abinash:
        # End block when closing brace detected
        if re.match(r'^[ +\-]*}', stripped):
            inside_abinash = False
            continue

        # Collect added or removed lines
        if stripped.startswith('+') or stripped.startswith('-'):
            collected.append(line)

# Output result
if collected:
    print("✅ Detected changes inside 'abinash' block:")
    for l in collected:
        print(l.strip())
else:
    print("🟢 No changes in 'abinash' block.")
