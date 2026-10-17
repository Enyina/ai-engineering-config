#!/usr/bin/env python3
"""Read-only workspace trust-domain preflight.

This is a guard for future AI-rule orchestration, not an OS sandbox or proof
of repository ownership. Refuses to enable personal-rule operations in an
unclassified or employer-owned workspace.
"""
import argparse
import json
import sys
from pathlib import Path

DECLARATIONS = (".ai-rules/workspace.json", ".ai-rules/workspace.local.json")
ACTIONS = ("inspect", "personal-rules", "personal-export", "personal-onboard")
OWNERS = {"personal": "personal", "employer": "organization"}

def assess(root, action):
    if (root / ".ai-rules").is_symlink():
        return {"trust_domain": "unclassified", "operation": action,
                "allowed": action == "inspect", "reason": "unsafe_declaration"}
    matches = [root / item for item in DECLARATIONS
               if (root / item).exists() or (root / item).is_symlink()]
    if len(matches) != 1:
        reason = "missing_declaration" if not matches else "multiple_declarations"
        return {"trust_domain": "unclassified", "operation": action,
                "allowed": action == "inspect", "reason": reason}
    file = matches[0]
    if file.is_symlink() or not file.is_file() or file.stat().st_size > 8192:
        return {"trust_domain": "unclassified", "operation": action,
                "allowed": action == "inspect", "reason": "unsafe_declaration"}
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError, OSError):
        data = None
    if (not isinstance(data, dict) or set(data) !=
            {"schema_version", "trust_domain", "policy_owner"} or
            type(data.get("schema_version")) is not int or data["schema_version"] != 1 or
            data.get("trust_domain") not in OWNERS or
            data.get("policy_owner") != OWNERS[data["trust_domain"]]):
        return {"trust_domain": "unclassified", "operation": action,
                "allowed": action == "inspect", "reason": "invalid_declaration"}
    domain = data["trust_domain"]
    allowed = action == "inspect" or domain == "personal"
    return {"trust_domain": domain, "operation": action, "allowed": allowed,
            "reason": "inspect_only" if action == "inspect" else
                      ("personal_workspace" if allowed else "employer_boundary")}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, default=Path.cwd(),
                   help="Local project root; never transmitted.")
    p.add_argument("--operation", choices=ACTIONS, default="inspect")
    p.add_argument("--json", action="store_true",
                   help="Emit only a sanitized decision, without paths or contents.")
    args = p.parse_args()
    report = assess(args.workspace, args.operation)
    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print("Trust domain:", report["trust_domain"])
        print("Requested operation:", report["operation"])
        print("Decision:", "ALLOWED" if report["allowed"] else "DENIED")
        print("Reason:", report["reason"])
        print("No files, credentials, instructions or permissions were changed.")
    if not report["allowed"]:
        sys.exit(2)

if __name__ == "__main__":
    main()
