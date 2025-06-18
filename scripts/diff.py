import subprocess
import hcl2
import json
from io import StringIO
import os

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

# Load current and previous
current_path = "demo.tfvars"
with open(current_path, "r") as f:
    current_content = f.read()
previous_content = get_file_content("HEAD~1", current_path)

# Parse and compare
current_abinash = parse_abinash_block(current_content)
previous_abinash = parse_abinash_block(previous_content)

# Save diff if changed
output_path = os.environ.get("GITHUB_OUTPUT")
if current_abinash != previous_abinash:
    diff = {
        "old": previous_abinash,
        "new": current_abinash
    }
    with open("abinash_diff.txt", "w") as out:
        out.write(json.dumps(diff, indent=2))
    if output_path:
        with open(output_path, "a") as f:
            f.write("changed=true\n")
else:
    if output_path:
        with open(output_path, "a") as f:
            f.write("changed=false\n")
