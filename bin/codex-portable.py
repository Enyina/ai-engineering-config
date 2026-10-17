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
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__", ".venv"}]
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
        fail("No snapshot manifest. Capture on source machine first.")
    manifest = json.loads(manifest_file.read_text())
    for entry in manifest.get("files", []):
        path = Path(entry["path"])
        if path.is_absolute() or ".." in path.parts or path.parts[0] not in {"codex", "agents"}:
            fail("Unsafe manifest path")
        file = SNAP / path
        if not file.is_file() or not check_file(file) or digest(file) != entry["sha256"]:
            fail("Snapshot changed or unsafe: " + str(path))
    return manifest

def restore(apply, config=False):
    validated_snapshot()
    print("RESTORE", "APPLY" if apply else "PREVIEW", "(existing overwritten paths are backed up)")
    backup = HOME / ".codex-portable-backups" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    for name, destination in SOURCES.items():
        source = SNAP / name
        if not source.exists():
            continue
        print(source, "->", destination)
        if not apply:
            continue
        if destination.exists() or destination.is_symlink():
            old = backup / name
            old.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(destination), str(old))
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    safe = SNAP / "codex" / "config.safe.toml"
    if config and safe.exists():
        print("Safe config merge requested — review and merge manually:", safe)
    if apply:
        print("Restore complete. Restart Codex and audit again. Backups:", backup)
    else:
        print("Dry run. Add --apply after reviewing.")

def reset(apply, confirmed):
    for key, dest in SOURCES.items():
        if dest.exists() or dest.is_symlink():
            print("Would remove:", dest)
    if not apply:
        print("DRY RUN. Use reset --apply --confirmed-remote after verifying a private remote backup.")
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
    for destination in SOURCES.values():
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        elif destination.is_dir():
            shutil.rmtree(destination)
    print("Personal managed rules removed. Credentials, sessions, history and other configs NOT removed.")

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
