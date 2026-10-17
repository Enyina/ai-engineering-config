# New computer setup

Install Git and Python 3, and sign in to GitHub. Clone the private personal configuration and whichever personal projects you want to work on. From the configuration repository, run `python3 bin/setup`.

The installer identifies supported coding assistants and verified personal projects. It previews the proposed additions and asks before installing them. It preserves existing project instructions, writes only labeled personal guidance, and saves local backups. It never edits employer workspaces or global command permissions.

Afterward, open a personal project in your AI coding assistant and describe the outcome you want in ordinary language. The project instructions and selected shared guidance will be available there. Confirm automatic instruction loading inside each installed agent; a file being present is not proof that the app read it.

For a noninteractive setup use `python3 bin/setup --apply`; for a recheck use `python3 bin/setup --check`; to restore only unchanged files recorded by setup use `python3 bin/setup --rollback`. If your projects are in another directory, pass `--projects-root` with their parent directory.

This setup does not download every repository or configure your AI tool accounts. Missing or unverified personal project checkouts are skipped rather than guessed. The public-source checks remain on GitHub twice daily and need no setup on this computer.
