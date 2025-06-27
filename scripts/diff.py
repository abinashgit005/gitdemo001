# check_fqdn_additions.py
import re

with open("tfvars_changes/full_diff.txt") as f:
    lines = f.readlines()

inside = False
path = []

added_fqdns = []

for line in lines:
    # Detect block starts from diff context
    match = re.search(r'(\w[\w-]*)\s*=\s*{', line)
    if match:
        path.append(match.group(1))

    # Detect block end
    elif re.match(r'^[ +\-]*}', line):
        if path:
            path.pop()

    # Check if inside the exact block path
    if path == ['tmac-internet', 'app_rules', 'tsac_all']:
        if line.startswith('+') and not line.startswith('++'):
            fqdn_match = re.search(r'([a-zA-Z0-9.-]+\.[a-z]{2,})', line)
            comment_match = re.search(r'#(.*)', line)
            if fqdn_match:
                fqdn = fqdn_match.group(1).strip()
                comment = comment_match.group(1).strip() if comment_match else "No comment"
                added_fqdns.append((fqdn, comment))

# Final output
if added_fqdns:
    print("✅ Newly added FQDNs in tmac-internet > app_rules > tsac_all > fqdns:")
    for fqdn, comment in added_fqdns:
        print(f"- {fqdn} → {comment}")
else:
    print("🟢 No new FQDNs added in the target block.")
