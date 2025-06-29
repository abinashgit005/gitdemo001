readme_file = "README.md"
fqdn_file = "added_fqdns.txt"

# Step 1: Read new FQDNs
try:
    with open(fqdn_file) as f:
        new_lines = []
        for line in f:
            if line.strip():
                fqdn, *comment = [p.strip() for p in line.split("|")]
                comment = comment[0] if comment else "#"
                new_lines.append(
                    f"| dev                               |{fqdn:<21}|TCP       | 443  | {comment:<24} |"
                )
except FileNotFoundError:
    print("❌ 'added_fqdns.txt' not found.")
    exit(1)

# Step 2: Read README.md
with open(readme_file) as f:
    lines = f.readlines()

# Step 3: Locate the firewall rule table block
start = end = None
for i, line in enumerate(lines):
    if line.strip().startswith("### 1.2.1 Default Internet outbound firewall rules"):
        start = i
    elif start and not line.strip().startswith("|") and line.strip():
        end = i
        break

if start is None or end is None:
    print("❌ Could not locate the table section.")
    exit(1)

# Step 4: Insert new lines before table end
# Table header is 2 lines after start
insertion_point = start + 2
while insertion_point < len(lines) and lines[insertion_point].startswith("|"):
    insertion_point += 1

lines = lines[:insertion_point] + [line + "\n" for line in new_lines] + lines[insertion_point:]

# Step 5: Write back updated README.md
with open(readme_file, "w") as f:
    f.writelines(lines)

print("✅ README.md updated with new FQDNs.")

print("\n✅ README.md updated. Here's the new content:\n")
print("".join(lines))
