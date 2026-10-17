#!/usr/bin/env python3
"""Portable personal Codex rule manager. Python 3.9+, standard library only."""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
CODEX = Path(os.getenv("CODEX_HOME", HOME / ".codex")).expanduser()
SNAP = ROOT / "snapshot"
SOURCES = {
    "codex/AGENTS.md": CODEX / "AGENTS.md",
    "codex/AGENTS.override.md": CODEX / "AGENTS.override.md",
    "codex/rules": CODEX / "rules",
    "agents/skills": HOME / ".agents" / "skills",
    "codex/skills": CODEX / "skills",
}
SAFE_KEYS = {"model", "model_reasoning_effort", "approval_policy", "sandbox_mode"}
TEXT_SUFFIX = {".md", ".rules", ".py", ".toml", ".json", ".yaml", ".yml", ".txt", ".sh"}
SECRET = re.compile(r"-----BEGIN .{0,30}PRIVATE KEY-----|(?:ghp_|github_pat_|sk-proj-)[\w-]{12,}", re.I)

def fail(message):
    raise SystemExit("ERROR: " + message)

def shell(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_file(path):
    if path.is_symlink():
        fail("Symlink refused: " + str(path))
    if path.stat().st_size > 1024 * 1024:
        fail("Oversized file refused: " + str(path))
    if path.name in {"auth.json", "credentials.json"} or path.name.startswith(".env"):
        fail("Secret filename refused: " + str(path))
    if path.suffix.lower() not in TEXT_SUFFIX:
        return False
    try:
        body = path.read_text(encoding="utf-8")
    except UnicodeError:
        fail("Non-text file refused: " + str(path))
    if SECRET.search(body):
        fail("Possible credential; review locally: " + str(path))
    return True

def items(path):
    if not path.exists():
        return []
    if path.is_symlink():
        fail("Symlink refused: " + str(path))
    if path.is_file():
        return [(path, Path(path.name))]
    output = []
    for base, dirs, files in os.walk(path, followlinks=False):
        base = Path(base)
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__", ".venv", ".system"}]
        for d in dirs:
            if (base / d).is_symlink():
                fail("Symlink directory refused: " + str(base / d))
        output.extend((base / f, (base / f).relative_to(path)) for f in files)
    return output

def audit():
    print("CODEX_HOME:", CODEX, "CURRENT PROJECT:", Path.cwd())
    dirs = []
    cur = Path.cwd().resolve()
    while True:
        dirs.append(cur)
        if (cur / ".git").exists() or cur.parent == cur:
            break
        cur = cur.parent
    for scope, directory in [("global", CODEX), *[("project", x) for x in reversed(dirs)]]:
        for name in ("AGENTS.override.md", "AGENTS.md"):
            p = directory / name
            if p.is_file():
                print(scope, p, digest(p)[:12])
                break
        for location in (directory / ".codex" / "config.toml",):
            if location.is_file():
                print(scope, "config:", location)
    for key, target in SOURCES.items():
        if target.exists():
            print("user-owned:", key, str(target))
    print("Runtime CLI flags, model instructions and organization-managed policy are NOT exhaustively audited.")

def capture():
    temp = Path(tempfile.mkdtemp(prefix=".capture-", dir=ROOT))
    try:
        for name, src in SOURCES.items():
            for old, rel in items(src):
                if not check_file(old):
                    continue
                target = temp / name if src.is_file() else temp / name / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(old, target)
        config = CODEX / "config.toml"
        if config.is_file() and not config.is_symlink():
            lines = []
            within_table = False
            for line in config.read_text().splitlines():
                if line.lstrip().startswith("["):
                    within_table = True
                if within_table:
                    continue
                match = re.match(r"^\s*([\w-]+)\s*=\s*(.*?)\s*$", line)
                if match and match.group(1) in SAFE_KEYS and not SECRET.search(match.group(2)):
                    lines.append(line)
            if lines:
                p = temp / "codex" / "config.safe.toml"
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("# Reviewed top-level subset; never a full config backup.\n" + "\n".join(lines) + "\n")
        paths = sorted(p for p in temp.rglob("*") if p.is_file())
        manifest = {"created_at": datetime.now(timezone.utc).isoformat(),
                    "files": [{"path": str(p.relative_to(temp)), "sha256": digest(p)} for p in paths]}
        (temp / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        if SNAP.exists():
            previous = ROOT / ("snapshot.previous-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
            SNAP.rename(previous)
            print("Previous snapshot kept locally:", previous)
        temp.rename(SNAP)
        print("Captured:", SNAP, "— REVIEW ALL FILES BEFORE GIT ADD/PUSH. No upload performed.")
    finally:
        if temp.exists():
            shutil.rmtree(temp)

def validated_snapshot():
    manifest_file = SNAP / "manifest.json"
    if not manifest_file.is_file():
        fail("No snapshot manifest. Capture on your source machine first.")
    manifest = json.loads(manifest_file.read_text())
    checked = []
    for entry in manifest.get("files", []):
        path = Path(entry["path"])
        if path.is_absolute() or ".." in path.parts or ".system" in path.parts:
            fail("Unsafe or bundled-system path in manifest; run capture again")
        if not any(str(path) == key or str(path).startswith(key + "/")
                   for key in SOURCES):
            if str(path) != "codex/config.safe.toml":
                fail("Unexpected snapshot path: " + str(path))
        file = SNAP / path
        if not file.is_file() or not check_file(file) or digest(file) != entry["sha256"]:
            fail("Snapshot changed or unsafe: " + str(path))
        checked.append(path)
    actual = {str(p.relative_to(SNAP)) for p in SNAP.rglob("*") if p.is_file()}
    expected = {str(p) for p in checked} | {"manifest.json"}
    if actual != expected:
        fail("Snapshot contents do not match manifest; recapture and review")
    return manifest

def destination_for(relative):
    key = str(relative)
    for prefix, target in SOURCES.items():
        if key == prefix and target.suffix:
            return target
        if key.startswith(prefix + "/") and not target.suffix:
            return target / relative.relative_to(prefix)
    fail("Unexpected snapshot file: " + key)

def check_destination(destination):
    """Reject symlinks in managed user paths, not macOS system directory aliases.

    macOS tempfile often lives under /var, which links to /private/var.
    The HOME directory itself is a trusted boundary. Symlinks *inside* that
    directory (e.g. ~/.codex/rules) are still rejected as unsafe.
    """
    path = Path(os.path.abspath(destination))
    home = Path(os.path.abspath(HOME))
    codex = Path(os.path.abspath(CODEX))
    if path == home or home in path.parents:
        anchor = home
    elif path == codex or codex in path.parents:
        # Supports an explicitly configured CODEX_HOME outside HOME.
        anchor = codex.parent
    else:
        fail("Destination is outside managed user directories: " + str(path))
    node = path
    while node != anchor:
        if node.is_symlink():
            fail("Symlink destination refused: " + str(node))
        node = node.parent

def require_allowed_managed_file(destination):
    """Disallow arbitrary receipt paths and built-in skill modifications."""
    dest = Path(os.path.abspath(destination))
    for prefix, root in SOURCES.items():
        candidate = Path(os.path.abspath(root))
        if candidate.suffix and dest == candidate:
            return
        if not candidate.suffix and candidate in dest.parents and ".system" not in dest.parts:
            if dest.suffix.lower() in TEXT_SUFFIX:
                return
    fail("Receipt refers to a non-managed path: " + str(destination))

def restore(apply, config=False):
    manifest = validated_snapshot()
    receipt = HOME / ".codex-portable-installed.json"
    if receipt.exists():
        fail("An earlier managed install exists. Audit/reset it before another restore.")
    actions = []
    for entry in manifest["files"]:
        relative = Path(entry["path"])
        if str(relative) == "codex/config.safe.toml":
            continue
        dest = destination_for(relative)
        check_destination(dest)
        actions.append((SNAP / relative, dest, entry["sha256"]))
    print("RESTORE", "APPLY" if apply else "PREVIEW", "— individual files only, never whole directories")
    for _, destination, _ in actions:
        print("  ", destination)
    safe = SNAP / "codex" / "config.safe.toml"
    if config and safe.is_file():
        print("Safe config requires manual review and merge:", safe)
    if not apply:
        print("Dry run. Add --apply to install reviewed snapshot files.")
        return
    backup = HOME / ".codex-portable-backups" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    installed = []
    for source, destination, checksum in actions:
        original = None
        if destination.exists():
            relative = source.relative_to(SNAP)
            original = backup / relative
            original.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destination, original)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        installed.append({"path": str(destination), "sha256": checksum,
                          "backup": str(original) if original else None})
    receipt.write_text(json.dumps({"files": installed, "created_at": datetime.now(timezone.utc).isoformat()}, indent=2) + "\n")
    receipt.chmod(0o600)
    print("Restored selected files; existing unrelated files preserved. Receipt:", receipt)
    print("Backups:", backup)

def reset(apply, confirmed):
    receipt = HOME / ".codex-portable-installed.json"
    if not receipt.is_file():
        print("No managed install receipt. Nothing will be removed. Existing personal files are untouched.")
        return
    installed = json.loads(receipt.read_text()).get("files", [])
    for item in installed:
        print("Managed file:", item["path"])
    if not apply:
        print("DRY RUN. After verifying private Git backup, use reset --apply --confirmed-remote.")
        return
    if not confirmed:
        fail("Explicit --confirmed-remote required")
    status = shell("git", "status", "--porcelain")
    head = shell("git", "rev-parse", "HEAD")
    upstream = shell("git", "rev-parse", "@{upstream}")
    if status.returncode or status.stdout.strip() or head.returncode or upstream.returncode or head.stdout.strip() != upstream.stdout.strip():
        fail("Git checkout must be clean and HEAD equal upstream before reset")
    remote = shell("git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if remote.returncode or "/" not in remote.stdout:
        fail("Cannot identify tracked remote")
    remote_name, branch = remote.stdout.strip().split("/", 1)
    verified = shell("git", "ls-remote", "--exit-code", remote_name, "refs/heads/" + branch)
    if verified.returncode or not verified.stdout or verified.stdout.split()[0] != head.stdout.strip():
        fail("Remote HEAD not confirmed; no changes performed")
    # Refuse any changed or tampered managed file before removing anything.
    for item in installed:
        target = Path(item["path"])
        require_allowed_managed_file(target)
        check_destination(target)
        if not target.is_file() or digest(target) != item["sha256"]:
            fail("Installed rule modified; refusing reset: " + str(target))
        original = item.get("backup")
        if original and (not Path(original).is_file() or Path(original).is_symlink()):
            fail("Previous file backup missing or unsafe: " + original)
    for item in installed:
        target = Path(item["path"])
        target.unlink()
        if item.get("backup"):
            shutil.copy2(item["backup"], target)
    receipt.unlink()
    print("Managed rules reverted. Preexisting files restored. Auth, logs, history and unmanaged rules untouched.")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("audit")
    sub.add_parser("capture")
    for name in ("restore", "reset"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--apply", action="store_true")
        if name == "restore":
            cmd.add_argument("--apply-config", action="store_true")
        else:
            cmd.add_argument("--confirmed-remote", action="store_true")
    args = p.parse_args()
    if args.command == "audit":
        audit()
    elif args.command == "capture":
        capture()
    elif args.command == "restore":
        restore(args.apply, args.apply_config)
    else:
        reset(args.apply, args.confirmed_remote)

if __name__ == "__main__":
    main()
