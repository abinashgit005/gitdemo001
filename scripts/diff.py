import re, os

diff_path = "tfvars_changes/full_diff.txt"
out_path = "tfvars_changes/added_fqdns.txt"
os.makedirs("tfvars_changes", exist_ok=True)

with open(diff_path) as f:
    lines = f.readlines()

inside = False
fqdns = []

for line in lines:
    if re.search(r'abinash\s*=\s*{', line):
        inside = True
    elif inside and re.match(r'^[ +\-]*}', line):
        inside = False
    elif inside and re.match(r'^\+\s*fqdns\s*=\s*\[', line):
        continue
    elif inside and line.startswith('+') and '"' in line:
        fqdn = re.search(r'"([^"]+)"', line)
        comment = re.search(r'#(.*)', line)
        if fqdn:
            fqdns.append((fqdn.group(1).strip(), (comment.group(1).strip() if comment else 'Added automatically')))

with open(out_path, "w") as f:
    for fq, cm in fqdns:
        f.write(f"{fq} | {cm}\n")

if fqdns:
    print("✅ Added FQDNs:")
    for fq, cm in fqdns:
        print(f"- {fq} → {cm}")
else:
    print("🟢 No added FQDNs found.")
