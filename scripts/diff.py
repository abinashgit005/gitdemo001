import subprocess
import re
from pathlib import Path

# Get the git diff output
diff_file = Path("tfvars_changes/full_diff.txt")
diff_file.parent.mkdir(exist_ok=True)

try:
    diff_output = subprocess.check_output(
        ["git", "diff", "HEAD^", "HEAD", "--", "terraform.tfvars"],
        text=True
    )
except subprocess.CalledProcessError:
    print("❌ Git diff failed. Possibly no previous commit or file not changed.")
    exit(0)

diff_file.write_text(diff_output)

# Parse only tmac-internet > app_rules > tsac_all > fqdns block
in_tmac = in_app = in_tsac = in_fqdns = False
added_fqdns = []

for line in diff_output.splitlines():
    line_stripped = line.strip()

    if re.match(r'^[\+\s-]*tmac-internet\s*=\s*{', line):
        in_tmac = True
        continue
    if in_tmac and re.match(r'^[\+\s-]*app_rules\s*=\s*{', line):
        in_app = True
        continue
    if in_app and re.match(r'^[\+\s-]*tsac_all\s*=\s*{', line):
        in_tsac = True
        continue
    if in_tsac and re.match(r'^[\+\s-]*fqdns\s*=\s*\[', line):
        in_fqdns = True
        continue
    if in_fqdns and "]" in line:
        in_fqdns = False
        continue

    if in_fqdns and line.startswith("+") and not line.startswith("++"):
        cleaned_line = line.lstrip("+").strip()
        if cleaned_line:
            added_fqdns.append(cleaned_line)

if added_fqdns:
    print("✅ Newly added FQDNs (with comments):")
    for fqdn in added_fqdns:
        print(fqdn)
else:
    print("⚠️ No FQDNs were added in tmac-internet > app_rules > tsac_all.")
