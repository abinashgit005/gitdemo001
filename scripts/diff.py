import re
import os

# Paths
diff_path = "tfvars_changes/full_diff.txt"
readme_path = "README.md"

# Step 1: Extract added FQDNs from abinash block
with open(diff_path) as f:
    lines = f.readlines()

inside_abinash = False
fqdn_block = False
added_fqdns = []

for line in lines:
    stripped = line.strip()

    # Enter abinash block
    if re.match(r'^[ +-]*abinash\s*=\s*{', stripped):
        inside_abinash = True
        continue

    if inside_abinash:
        # Exit block
        if re.match(r'^[ +-]*}', stripped):
            inside_abinash = False
            fqdn_block = False
            continue

        # Detect fqdns list
        if re.match(r'^[ +-]*fqdns\s*=\s*\[', stripped):
            fqdn_block = True
            continue

        if fqdn_block:
            # End of fqdns list
            if re.match(r'^[ +-]*\]', stripped):
                fqdn_block = False
                continue

            # Capture added lines
            if line.startswith('+') and '"' in line:
                match = re.search(r'"(.*?)"', line)
                if match:
                    added_fqdns.append(match.group(1))
