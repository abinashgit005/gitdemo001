import re

with open("tfvars_changes/full_diff.txt") as f:
    lines = f.readlines()

inside_tsac_all = False
context = ""
added = []

for i, line in enumerate(lines):
    if re.search(r'tsac-internet\s*=\s*{', line):
        context = "tsac-internet"
    elif "app_rules" in line:
        context += ".app_rules"
    elif "tsac_all" in line and "=" in line:
        context += ".tsac_all"
        inside_tsac_all = True
    elif inside_tsac_all and re.match(r'^[ +\-]*}', line):
        inside_tsac_all = False
        context = ""

    if inside_tsac_all and line.startswith('+') and not line.startswith('++'):
        domain_match = re.search(r'([a-zA-Z0-9.-]+\.[a-z]{2,})', line)
        comment_match = re.search(r'#(.*)', line)
        if domain_match and context.endswith(".tsac_all"):
            added.append((domain_match.group(1).strip(), comment_match.group(1).strip() if comment_match else "No comment"))

if added:
    print("✅ FQDNs added in tsac-internet > app_rules > tsac_all:")
    for fqdn, comment in added:
        print(f"- {fqdn} → {comment}")
else:
    print("🟢 No new FQDNs added in tsac-internet > app_rules > tsac_all.")
