import subprocess
import re
from pathlib import Path

diff_file = Path("tfvars_changes/full_diff.txt")
diff_file.parent.mkdir(exist_ok=True)

try:
    diff_output = subprocess.check_output(
        ["git", "diff", "HEAD~1", "HEAD", "--", "terraform.tfvars"],
        text=True
    )
except subprocess.CalledProcessError as e:
    print("❌ Git diff failed:", e)
    diff_output = ""
if not diff_output.strip():
    print("📭 No diff found in terraform.tfvars between last 2 commits.")
    exit(0)

diff_file.write_text(diff_output)
print("📄 Full git diff:\n", diff_output)

# Start parsing
in_tmac = in_app = in_tsac = in_fqdns = False
added_fqdns = []

for line in diff_output.splitlines():
    line_stripped = line.strip()

    if re.match(r'^[\+\s-]*tmac-internet\s*=\s*{', line):
        in_tmac = True
        print("🔍 Entered tmac-internet")
        continue
    if in_tmac and re.match(r'^[\+\s-]*app_rules\s*=\s*{', line):
        in_app = True
        print("🔍 Entered app_rules")
        continue
    if in_app and re.match(r'^[\+\s-]*tsac_all\s*=\s*{', line):
        in_tsac = True
        print("🔍 Entered tsac_all")
        continue
    if in_tsac and re.match(r'^[\+\s-]*fqdns\s*=\s*\[', line):
        in_fqdns = True
        print("🔍 Entered fqdns list")
        continue
    if in_fqdns and "]" in line:
        in_fqdns = False
        print("✅ End of fqdns list")
        continue

    if in_fqdns and line.startswith("+") and not line.startswith("++"):
        cleaned_line = line.lstrip("+").strip()
        if cleaned_line:
            print("➕ Found added domain:", cleaned_line)
            added_fqdns.append(cleaned_line)

if added_fqdns:
    print("✅ Newly added FQDNs (with comments):")
    for fqdn in added_fqdns:
        print(fqdn)
else:
    print("⚠️ No FQDNs were added in tmac-internet > app_rules > tsac_all.")
