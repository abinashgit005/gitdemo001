# check_fqdn_additions.py
import re

with open("tfvars_changes/full_diff.txt") as f:
    lines = f.readlines()

stack = []
capture = False
fqdns = []

for line in lines:
    # Track block openings
    open_block = re.search(r'(\w[\w-]*)\s*=\s*{', line)
    if open_block:
        stack.append(open_block.group(1))
    
    # Track block closings
    elif re.match(r'^[ +\-]*}', line):
        if stack:
            stack.pop()

    # Check if we are inside the exact path
    if stack == ['tmac-internet', 'app_rules', 'tsac_all']:
        if line.startswith('+') and not line.startswith('++'):
            domain_match = re.search(r'([a-zA-Z0-9.-]+\.[a-z]{2,})', line)
            comment_match = re.search(r'#(.*)', line)
            if domain_match:
                fqdn = domain_match.group(1).strip()
                comment = comment_match.group(1).strip() if comment_match else "No comment"
                fqdns.append((fqdn, comment))

# Output results
if fqdns:
    print("✅ New FQDNs in tsac-internet > app_rules > tsac_all > fqdns:")
    for fqdn, comment in fqdns:
        print(f"- {fqdn} → {comment}")
else:
    print("🟢 No new FQDNs added in tsac-internet.app_rules.tsac_all.fqdns")
