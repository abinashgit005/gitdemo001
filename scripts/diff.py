import subprocess
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

# 🧠 Smarter block detection based on structure in diff
in_block = False
block_path = []

added_fqdns = []

for line in diff_output.splitlines():
    stripped = line.strip()

    if "tmac-internet" in line:
        block_path = ["tmac-internet"]
    elif "app_rules" in line and "{" in line:
        block_path.append("app_rules")
    elif "tsac_all" in line and "{" in line:
        block_path.append("tsac_all")
    elif "fqdns" in line and "[" in line:
        if block_path == ["tmac-internet", "app_rules", "tsac_all"]:
            in_block = True
        continue
    elif "]" in line and in_block:
        in_block = False
        continue

    if in_block and line.startswith("+") and not line.startswith("++"):
        cleaned = line.lstrip("+").strip()
        if cleaned:
            added_fqdns.append(cleaned)

if added_fqdns:
    print("✅ Newly added FQDNs (with comments):")
    for fqdn in added_fqdns:
        print(fqdn)
else:
    print("⚠️ No FQDNs were added in tmac-internet > app_rules > tsac_all.")
