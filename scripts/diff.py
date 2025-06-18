import subprocess
import hcl2
from io import StringIO

def get_file_content(commit, filepath):
    try:
        result = subprocess.run(["git", "show", f"{commit}:{filepath}"],
                                capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def parse_abinash(content):
    try:
        parsed = hcl2.load(StringIO(content))
        return parsed.get("abinash", {}).get("app_rules", {}).get("fqdns", [])
    except Exception:
        return []

# Get current and previous commit contents
current = get_file_content("HEAD", "demo.tfvars")
previous = get_file_content("HEAD~1", "demo.tfvars")

# Extract FQDNs
current_fqdns = parse_abinash(current)
previous_fqdns = parse_abinash(previous)

# Compare
added = set(current_fqdns) - set(previous_fqdns)

if added:
    print("✅ Added FQDNs:")
    for fqdn in added:
        print(f"- {fqdn}")
    # Write to file for use in pipeline
    with open("added_fqdns.txt", "w") as f:
        for fqdn in added:
            f.write(f"{fqdn}\n")
else:
    print("✅ No new FQDNs added.")
