section_title = "1.2.1 Default Internet outbound firewall rules"
readme = "README.md"
fqdn_file = "tfvars_changes/added_fqdns.txt"
# Read new FQDNs and comments
try:
    with open(fqdn_file) as f:
        new_rows = [line.strip().split('|') for line in f if line.strip()]
except FileNotFoundError:
    print("⚠️ No FQDN file found.")
    exit(0)

with open(readme) as f:
    lines = f.readlines()

# Find where to insert (after the markdown table header)
insert_at = None
for i, line in enumerate(lines):
    if section_title.lower() in line.lower():
        for j in range(i+1, len(lines)):
            if lines[j].startswith("|---"):
                insert_at = j + 1
                break
        break

if insert_at is None:
    print("❌ Section or table not found.")
    exit(1)

# Format and insert new rows
for fqdn, comment in new_rows:
    row = f"| dev | {fqdn.strip()} | TCP | 443 | {comment.strip()} |\n"
    lines.insert(insert_at, row)
    insert_at += 1

with open(readme, "w") as f:
    f.writelines(lines)

print("✅ README.md updated.")
