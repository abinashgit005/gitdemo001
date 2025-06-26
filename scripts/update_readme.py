# update_readme.py

section_title = "1.2.1 Default Internet outbound firewall rules"
readme_path = "README.md"
fqdn_file = "tfvars_changes/added_fqdns.txt"

# Read new entries
try:
    with open(fqdn_file) as f:
        new_rows = [line.strip().split('|') for line in f if line.strip()]
except FileNotFoundError:
    print("⚠️ No new FQDNs found.")
    exit(0)

# Load README
with open(readme_path) as f:
    lines = f.readlines()

# Find table start (heading + separator)
start = None
for i, line in enumerate(lines):
    if section_title.lower() in line.lower():
        for j in range(i + 1, len(lines)):
            if lines[j].startswith('|---'):
                start = j
                break
        break

if start is None:
    print("❌ Could not find table.")
    exit(1)

# Find where table ends (next non-table line)
end = start + 1
while end < len(lines) and lines[end].strip().startswith('|'):
    end += 1

# Create padded new rows
new_lines = [
    f"| dev                               |{fqdn.strip():<21}|TCP       | 443  | {comment.strip():<24}|\n"
    for fqdn, comment in new_rows
]

# Insert at end of table
lines = lines[:end] + new_lines + lines[end:]

# Save and print
with open(readme_path, "w") as f:
    f.writelines(lines)

print("\n✅ README.md updated. Here's the new content:\n")
print("".join(lines))
