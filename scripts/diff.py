import subprocess
import hcl2
from io import StringIO
import json

# ---------- Helper functions ----------

def get_commit_sha(ref):
    result = subprocess.run(["git", "rev-parse", ref], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_file_from_commit(commit, filepath):
    try:
        result = subprocess.run(["git", "show", f"{commit}:{filepath}"],
                                capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def extract_abinash_block(hcl_string):
    try:
        parsed = hcl2.load(StringIO(hcl_string))
        return parsed.get("abinash", {})
    except Exception as e:
        print(f"Error parsing HCL: {e}")
        return {}
def print_diff(old, new, prefix=""):
    # Print keys removed
    for key in old:
        if key not in new:
            print(f"❌ Removed: {prefix + key} = {old[key]}")
        elif old[key] != new[key]:
            if isinstance(old[key], dict) and isinstance(new[key], dict):
                print_diff(old[key], new[key], prefix + key + ".")
            else:
                print(f"🔁 Changed: {prefix + key}: {old[key]} → {new[key]}")
    # Print keys added
    for key in new:
        if key not in old:
            print(f"✅ Added: {prefix + key} = {new[key]}")

# ---------- Main logic ----------

file_path = "demo.tfvars"

# Get commit SHAs
current_commit = get_commit_sha("HEAD")
previous_commit = get_commit_sha("HEAD~1")

# Get file content from both commits
current_content = get_file_from_commit(current_commit, file_path)
previous_content = get_file_from_commit(previous_commit, file_path)

# Parse abinash blocks
current_abinash = extract_abinash_block(current_content)
previous_abinash = extract_abinash_block(previous_content)

# Compare and print changes
if current_abinash != previous_abinash:
    print(f"🔁 Detected change in `abinash` block:")
    print(json.dumps({
        "previous": previous_abinash,
        "current": current_abinash
    }, indent=2))
else:
    print("✅ No change in `abinash` block.")
