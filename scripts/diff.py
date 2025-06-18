
# scripts/check_abinash_app_rules_diff.py

import hcl2
from deepdiff import DeepDiff
import json
import os

def extract_app_rules(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        data = hcl2.load(f)
    return data.get("abinash", {}).get("app_rules", {})

old = extract_app_rules("tmp/old.tfvars")
new = extract_app_rules("tmp/new.tfvars")

diff = DeepDiff(old, new, ignore_order=True)

if diff:
    print("🔁 Detected changes in abinash.app_rules:")
    print(json.dumps(diff, indent=2))
    with open("tmp/app_rules_diff.json", "w") as f:
        json.dump(diff, f, indent=2)
    print("changed=true")  # Used in workflow
    exit(0)
else:
    print("✅ No change in abinash.app_rules")
    print("changed=false")
    exit(0)
