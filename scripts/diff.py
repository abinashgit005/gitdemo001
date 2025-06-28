import subprocess
import re
import json
from pathlib import Path

def extract_fqdns_from_file(content: str) -> list[str]:
    """
    Extracts the FQDN list from the tmac-internet > app_rules > tsac_all block.
    """
    fqdns = []
    in_tmac = in_app = in_tsac = in_fqdns = False

    for line in content.splitlines():
        if "tmac-internet" in line:
            in_tmac = True
        elif in_tmac and "app_rules" in line:
            in_app = True
        elif in_app and "tsac_all" in line:
            in_tsac = True
        elif in_tsac and "fqdns" in line and "[" in line:
            in_fqdns = True
            continue
        elif in_fqdns and "]" in line:
            in_fqdns = False
            break
        elif in_fqdns:
            line = line.strip().rstrip(",")
            if line:
                # Remove inline comments and quotes
                match = re.match(r'"([^"]+)"(?:,)?(?:\s*#\s*(.*))?', line)
                if match:
                    fqdn = match.group(1).strip()
                    comment = match.group(2).strip() if match.group(2) else ""
                    fqdns.append(fqdn + ("  # " + comment if comment else ""))
    return fqdns

# Get old and new file versions from git
try:
    old_content = subprocess.check_output(["git", "show", "HEAD~1:demo.tfvars"], text=True)
    new_content = subprocess.check_output(["git", "show", "HEAD:demo.tfvars"], text=True)
except subprocess.CalledProcessError as e:
    print("❌ Failed to fetch file versions from Git:", e)
    exit(1)

old_fqdns = extract_fqdns_from_file(old_content)
new_fqdns = extract_fqdns_from_file(new_content)

# Detect added domains
added_fqdns = [fqdn for fqdn in new_fqdns if fqdn not in old_fqdns]

if added_fqdns:
    print("✅ Newly added FQDNs (with comments):")
    for fqdn in added_fqdns:
        print(fqdn)
else:
    print("⚠️ No FQDNs were added in tmac-internet > app_rules > tsac_all.")

output_path = Path("added_fqdns.txt")
output_path.write_text("\n".join(added_fqdns))
