import subprocess
import re
from pathlib import Path

diff_file = Path("tfvars_changes/full_diff.txt")
diff_file.parent.mkdir(exist_ok=True)

try:
    diff_output = subprocess.check_output(
        ["git", "diff", "HEAD~1", "HEAD", "--", "demo.tfvars"],
        text=True
    )
except subprocess.CalledProcessError as e:
    print("❌ git diff failed:", e)
    diff_output = ""

if not diff_output.strip():
    print("📭 No diff found in demo.tfvars between last 2 commits.")
    exit(0)

diff_file.write_text(diff_output)
print("📄 Full git diff:\n", diff_output)

# Initialize state flags
in_tmac = in_app = in_tsac = in_fqdns = False
added_fqdns = []

for line in diff_output.splitlines():
    raw = line.strip()

    if "tmac-internet" in line and "=" in line and "{" in line:
        in_tmac = True
        continue
    if in_tmac and "app_rules" in line and "=" in line and "{" in line:
        in_app = True
        continue
    if in_app and "tsac_all" in line and "=" in line and "{" in line:
        in_tsac = True
        continue
    if in_tsac and "fqdns" in line and "=" in line and "[" in line:
        in_fqdns = True
        continue
    if in_fqdns and "]" in line:
        in_fqdns = False
        continue

    # Now we're inside the fqdns list block
    if in_fqdns and line.startswith("+") and not line.startswith("++"):
        cleaned = line.lstrip("+").strip()
        if cleaned:
            added_fqdns.append(cleaned)

if added_fqdns:
    print("✅ Newly added FQDNs (with comments):")
    for fqdn in added_fqdns:
        print(fqdn)
else:
    print("⚠️ No FQDNs were added in tmac-internet > app_rules > tsac_all.")
