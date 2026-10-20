# Public product: shared intelligence, private profiles and reviewed learning

**Status:** functional first public-user onboarding and local proposal routing. This is not a hosted account service, remote learning system or autonomous model training.

## Three scopes, three destinations

| Who | Where accepted guidance belongs | Who can change it |
| --- | --- | --- |
| Everybody | The reviewed open source `rules/shared/BASE.md` and neutral skills | Maintainers through reviewed PRs |
| Signed-in contributor | Their own private local profile and proposals | That contributor, from their own authenticated machine |
| Repository owner | Owner-private local profile and proposals | The verified GitHub account with user ID `91235626` (current login `Enyina`) |

Employer-owned rules always stay inside their respective approved environments. Generic public advice can be **suggested** to employer agents with the source identified; it is not a company policy or authorized write.

The existing `policies/personal/policy.json` is a **legacy, publicly visible example of the original owner's profile**, not a default policy for outside users. Other users must install the neutral shared rules. A follow-up migration should move the maintainer profile to a truly private repository or secured owner-specific storage, then retire the public legacy policy after compatibility tests. Deleting it from a public GitHub branch would not erase its history.

## Use as a non-contributor

Install Python 3, Git, and GitHub CLI; sign in with `gh auth login`. Clone the public repository and from the root of **your own** GitHub project run:

```sh
python3 /path/to/ai-engineering-config/bin/use
python3 /path/to/ai-engineering-config/bin/use --apply
```

The first command previews changes. The second is an explicit opt-in that adds a labeled public guidance block, a Claude import file when none exists and a separate Cursor rule. Codex and Antigravity can use the repository AGENTS file. It only applies when the authenticated GitHub account matches the GitHub origin owner and any workspace ownership marker is personal. It leaves existing unrelated files alone. The presence of instructions does not prove every AI application has loaded them.

Contributors do not need repository write permission to use the software. The product does not phone home, download secrets or automatically share user lessons.

## Learn responsibly, without cross-user leakage

A user submits a **locally reviewed** JSON evidence record to `bin/rule-learn --event my-lesson.json`. Without `--apply`, it previews the classification. With `--apply`, the proposal remains on that user's computer under `~/.config/ai-engineering/learning`. The tool checks basic structure, evidence references, privacy-review confirmation and obvious token patterns; it does **not** prove the evidence is true.

- GitHub identity is read from `gh api user`, not `git config user.name`, a request field, a commit message or a changeable email.
- Only the authenticated ID `91235626` routes to `owner-private/proposals`. Other verified IDs route to `users/<id>/proposals`; unauthenticated requests never gain owner scope.
- No learning event rewrites active rules, uploads data or creates a public PR.
- If a user explicitly consents to share a sanitized general lesson, they may manually submit a GitHub issue or PR. Nothing is auto-published.
- A maintainer evaluates reproducibility, quality of references, falsifiability, transferability, confidentiality, conflicts, and regression checks before approving any shared rule.
- Contributor learnings about a project stay project-scoped until repeated independent evidence justifies a broader principle. No evidence means no automatic global promotion.

## Recommended acceptance criteria

**Account isolation:** 100% of synthetic nonowner test submissions remain out of owner-private storage; no unclassified submission writes active policy.

**Source quality:** public rule proposals need direct/reproducible evidence, a meaningful alternative, limitations, and independent reviewer approval. A positive reaction or popularity score alone is insufficient.

**Tenant privacy:** no internal source, credential, employer-specific instruction or other user profile is incorporated into shared public rules. The regex screen is only one layer, not a complete data-loss-prevention solution.

**Device portability:** a new contributor can install and use neutral rules on a verified personal project without being a repo contributor. Four agent adapters require real app-level verification before claiming cross-agent compatibility.

**System integrity:** owner-only paths must be reviewed under a GitHub ruleset; a CODEOWNERS file and a passing workflow alone **do not enforce protections on direct pushes**.

## Hosted product and learning roadmap

1. Complete branch protection and private maintainer-profile migration.
2. Offer straightforward first-run onboarding for users whose personal GitHub projects are organization-owned or use another Git host, without misclassifying employer property.
3. Add profile-scoped approved user rules, secure local approval/update/rollback and per-agent acceptance tests.
4. Create a public contribution queue with moderation, independent evaluation and provenance. Untrusted proposals never become active automatically.
5. If cloud sync is needed, build an authenticated opt-in service with private per-user encrypted data, explicit consent, deletion and export. This repository does not provide such a service yet.

## Protecting the legacy owner path

`.github/CODEOWNERS` requests owner reviews. `.github/workflows/owner-personal-policy-guard.yml` checks the **trusted GitHub pull-request author ID** against `91235626` when a change touches a personal-policy path. This GitHub-hosted identity is stronger than a locally declared Git author. It still needs a main-branch ruleset with required checks and code-owner reviews to be an effective merge gate, and it cannot prevent a privileged administrator from intentionally changing repository controls.

See [GitHub's protected branches documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
