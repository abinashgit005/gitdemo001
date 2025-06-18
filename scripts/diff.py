
# scripts/diff.py

import subprocess
import hcl2
import json
from io import StringIO

def get_file_content(commit, file):
    try:
        result = subprocess.run(["git", "show", f"{commit}:{file}"],
                                capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def parse_abinash_block(content):
    try:
        return hcl2.load(StringIO(content)).get("abinash", {})
    except Exception:
        return {}

# Load current file and previous version from git
current_path = "demo.tfvars"
with open(current_path, "r") as f:
    current_content = f.read()
previous_content = get_file_content("HEAD~1", current_path)

# Parse abinash blocks
current_abinash = parse_abinash_block(current_content)
previous_abinash = parse_abinash_block(previous_content)

# Compare and output diff if changed
if current_abinash != previous_abinash:
    diff = {
        "old": previous_abinash,
        "new": current_abinash
    }
    print("::set-output name=changed::true")
    with open("abinash_diff.txt", "w") as out:
        out.write(json.dumps(diff, indent=2))
else:
    print("::set-output name=changed::false")
