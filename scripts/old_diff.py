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

def extract_fqdns(hcl_string):
    try:
        parsed = hcl2.load(StringIO(hcl_string))
        return parsed.get("abinash", {}).get("app_rules", {}).get("fqdns", [])
    except Exception:
        return []

current = get_file_content("HEAD", "demo.tfvars")
previous = get_file_content("HEAD~1", "demo.tfvars")

current_fqdns = extract_fqdns(current)
previous_fqdns = extract_fqdns(previous)

added = set(current_fqdns) - set(previous_fqdns)

if added:
    print("✅ Added FQDNs:")
    print("added")
    with open("fqdns_update.txt", "w") as f:
        for fqdn in sorted(added):
            print(f"- {fqdn}")
            f.write(f"{fqdn}\n")
else:
    print("✅ No new FQDNs added.")
