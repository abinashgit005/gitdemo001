# extract_fqdns.py

import re
import os

diff_path = "tfvars_changes/full_diff.txt"
output_path = "tfvars_changes/added_fqdns.txt"

# Ensure output dir exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(diff_path) as f:
    lines = f.readlines()

inside_abinash = False
fqdn_block = False
added_fqdns = []

for line in lines:
    stripped = line.strip()

    if re.match(r'^[ +-]*abinash\s*=\s*{', stripped):
        inside_abinash = True
        continue

    if inside_abinash:
        if re.match(r'^[ +-]*}', stripped):
            inside_abinash = False
            fqdn_block = False
            continue

        if re.match(r'^[ +-]*fqdns\s*=\s*\[', stripped):
            fqdn_block = True
            continue

        if fqdn_block:
            if re.match(r'^[ +-]*\]', stripped):
                fqdn_block = False
                continue

            if line.startswith('+') and '"' in line:
                fqdn_match = re.search(r'"([^"]+)"', line)
                comment_match = re.search(r'#(.*)', line)
                fqdn = fqdn_match.group(1).strip() if fqdn_match else ''
                comment = comment_match.group(1).strip() if comment_match else ''
                if fqdn:
                    added_fqdns.append(f"{fqdn} | {comment or 'Added automatically'}")

# Save results
with open(output_path, "w") as f:
    for fq in added_fqdns:
        f.write(f"{fq}\n")

# Log to console
if added_fqdns:
    print("✅ Added FQDNs found:")
    for fq in added_fqdns:
        print(f"- {fq}")
else:
    print("🟢 No new FQDNs found.")
