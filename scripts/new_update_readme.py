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
                new_line = f"| dev                               |{fqdn:<21}|TCP       | 443  | {comment:<24} |"
                new_lines.append(new_line.rstrip() + "\n")  # Ensure newline
except FileNotFoundError:
    print("❌ 'added_fqdns.txt' not found.")
    exit(1)

# Step 2: Read current README
with open(readme_file) as f:
    lines = f.readlines()

# Step 3: Locate the table under section 1.2.1
start = header = end = None
for i, line in enumerate(lines):
    if line.strip().startswith("### 1.2.1 Default Internet outbound firewall rules"):
        start = i
    if start is not None and "| From" in line:
        header = i
    if header is not None and "---" in line:
        # Find where table rows stop
        for j in range(i + 1, len(lines)):
            if not lines[j].startswith("|"):
                end = j
                break
        else:
            end = len(lines)
        break

# Validation check
if start is None or header is None or end is None:
    print("❌ Could not locate the firewall table section.")
    exit(1)

# ✅ Fix: Ensure last row ends with newline
if not lines[end - 1].endswith("\n"):
    lines[end - 1] += "\n"

# Step 4: Insert new FQDN lines
lines = lines[:end] + new_lines + lines[end:]

# Step 5: Write back updated README
with open(readme_file, "w") as f:
    f.writelines(lines)

# Step 6: Print final result
print("\n✅ README.md updated. Here's the new content:\n")
print("".join(lines))
