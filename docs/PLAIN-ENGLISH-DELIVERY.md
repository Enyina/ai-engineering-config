# Plain-English delivery standard

**Applies to:** personally owned projects and any employer-owned project that explicitly adopts the policy through its own authorized rules. A company policy or a direct user instruction takes precedence.

## Save completed work

After implementing and checking an authorized change, make a focused Git commit before reporting completion. The commit message should say what the change achieves in clear words. Stage only files belonging to the task. Never stage credentials or unrelated work, and never work around security checks. Do not commit when the project or user disallows it; explain what remains instead.

Committing is different from pushing, publishing or deploying. Follow each project's approved delivery process; never assume one action authorizes the others.

## Write release notes for ordinary readers

For each meaningful delivered change, update the project's existing human-facing release notes, or use `RELEASE_NOTES.md` when none exists. If a change hasn't been released, say **prepared** or **not available yet**; never claim people can use it just because code was committed.

Keep notes short. Explain the result and who benefits, not the code or the process used to build it.

**Use:** 
- **What changed:** a short everyday description
- **Why it matters:** the benefit to a customer or teammate
- **What to know:** anything unavailable, unfinished or needing action

**Avoid:** API, endpoint, payload, hook, refactor, migration, CI/CD, SHA, branch, commit, deployment pipeline, stack, database model, cron, queue, schema, lint, test suite, types, framework, and file paths. Prefer natural descriptions that do not need these words.

### Example

**Too technical:** "Refactored the Socket.IO broadcast service, fixed a status-transition regression, and added Prisma integration tests."

**For a reader:** "Pharmacies now receive order requests more reliably. Orders are less likely to return to an earlier step. We are still checking how the changes work for busy pharmacy teams."

That last statement is allowed only if it accurately matches evidence. Never invent a benefit, an incident or a release.

Technical verification belongs in a separate engineering report, where exact commands and test results can be recorded accurately.

## Delivery checklist

- Scoped change complete and appropriate verification run
- Focused commit created, or the restriction/blocker reported
- Human-facing release note updated (where meaningful)
- Publication status stated truthfully, not inferred from a commit
- No employer/private information exported to personal storage
