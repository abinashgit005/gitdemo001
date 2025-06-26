import subprocess
import re

def get_tfvars_diff():
    result = subprocess.run(
        ["git", "diff", "HEAD~1", "HEAD", "--", "demo.tfvars"],
        capture_output=True, text=True, check=True
    )
    return result.stdout

def extract_added_fqdns_with_comments(diff_text):
    in_abinash = False
    in_app_rules = False
    in_fqdns = False
    added_fqdns = []

    for line in diff_text.splitlines():
        stripped = line.strip()

        if stripped.startswith("+"):
            content = stripped[1:].strip()

            # Track block openings
            if content.startswith("abinash") and "=" in content:
                in_abinash = True
            elif in_abinash and content.startswith("app_rules") and "=" in content:
                in_app_rules = True
            elif in_app_rules and content.startswith("fqdns") and "=" in content:
                in_fqdns = True
                continue
            elif in_fqdns and content.startswith("]"):
                in_fqdns = False
                continue

            # Extract added lines in fqdns list
            if in_abinash and in_app_rules and in_fqdns:
                fqdn_match = re.match(r'"([^"]+)"(?:\s*#.*)?', content)
                if fqdn_match:
                    # Keep the full line (with comment)
                    added_fqdns.append(content)

        # Track block closings
        if "}" in stripped:
            if in_fqdns:
                in_fqdns = False
            elif in_app_rules:
                in_app_rules = False
            elif in_abinash:
                in_abinash = False

    return added_fqdns

# Main flow
diff_text = get_tfvars_diff()
fqdn_lines = extract_added_fqdns_with_comments(diff_text)

if fqdn_lines:
    with open("fqdns_update.txt", "w") as f:
        for fqdn in fqdn_lines:
            print(f"- {fqdn}")
            f.write(f"{fqdn}\n")
else:
    print("✅ No new FQDNs with comments found.")
