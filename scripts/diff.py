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

# 🧠 Fuzzy context-based detection
block_stack = []
in_fqdns_block = False
added_fqdns = []

for line in diff_output.splitlines():
    stripped = line.strip()

    # Track path in HCL hierarchy by watching context lines
    if "tmac-internet" in line:
        block_stack = ["tmac-internet"]
    elif "app_rules" in line:
        block_stack.append("app_rules")
    elif "tsac_all" in line:
        block_stack.append("tsac_all")
    elif "fqdns" in line and "[" in line and block_stack == ["tmac-internet", "app_rules", "tsac_all"]:
        in_fqdns_block = True
    elif "]" in line and in_fqdns_block:
        in_fqdns_block = False

    # Smart detection if only inner lines were added
    if not in_fqdns_block and block_stack == ["tmac-internet", "app_rules", "tsac_all"]:
        if line.startswith("+") and re.search(r'"[^"]+",\s*#.*', line):
            # Entering fqdns block implicitly
            in_fqdns_block = True

    if in_fqdns_block and line.startswith("+") and not line.startswith("++"):
        cleaned = line.lstrip("+").strip()
        if cleaned:
            added_fqdns.append(cleaned)

# Output result
if added_fqdns:
    print("✅ Newly added FQDNs (with comments):")
    for fqdn in added_fqdns:
        print(fqdn)
else:
    print("⚠️ No FQDNs were added in tmac-internet > app_rules > tsac_all.")
