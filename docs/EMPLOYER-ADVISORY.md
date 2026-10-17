# External recommendations for employer projects

This tool can suggest approaches to engineering and interface problems while respecting the ownership of a company project. **Do not wait for an employer to prescribe every implementation detail**: examine the actual problem, research proven public solutions, compare alternatives, and propose the best supported approach. Employer policies, legal obligations and instructions still take precedence.

## Two different things

- **Active company rule:** An employer-approved instruction inside its authorized environment. It is not created by a personal tool.
- **Outside suggestion:** A general principle or design/engineering alternative backed by a credible public reference or the user's approved general personal guidance. It is never binding company policy merely because it is suggested.

A private personal Moatt/portfolio/game rule is **not** a general suggestion for other employers. Only curated generic guidance with public reference links may be considered.

## When the employer has no specific rule

The assistant should still identify working external examples and propose meaningful options with explicit provenance. For each option say:
- **Source:** official public reference, such as W3C or OWASP, or generalized personal guidance from `Enyina/ai-engineering-config`.
- **Why it might help:** the concrete user/task problem.
- **Trade-off:** what can go wrong or cost more.
- **Employer fit:** what must be checked against organizational policies, security, existing code and actual users.
- **Verification:** what to test before adopting it.

The assistant can recommend a direction when evidence supports it. It must not falsely say a public publisher recommended our particular option, or that the organization approved an outside suggestion. Explicit company prohibitions, permissions, contracts and standards are controlling.

## Read-only advisory without an employer policy pack

Use an **abstract, non-confidential** description, even when company rule setup is not complete:

```bash
python3 bin/ai-intelligence suggest \
  --advisory-for-employer \
  --domain design \
  --task "improve accessible dashboard navigation"
```

For engineering, choose `--domain engineering` and a similarly general task. This uses only approved public-source references and broadly reusable personal guidance. It does **not** open any employer repository, read company files, alter any configuration, or upload source code. Its output marks `employer_policy_check=not_checked_no_employer_context_provided`. This mode **cannot** determine whether a company instruction conflicts, so review that before implementing.

When you have an employer-owned policy package stored **outside this personal repository**, plus authorization to inspect the relevant workspace, you can verify ownership and scope first:

```bash
python3 bin/ai-intelligence suggest \
  --advisory-for-employer \
  --policy-root /authorized/company-policy \
  --workspace /authorized/company-workspace \
  --project backend \
  --domain engineering \
  --task "evaluate bounded retry behavior"
```

The engine checks the employer pack, explicit workspace ownership marker, declared repository identity and selected project. It **does not print company rule contents** or treat the generic personal suggestions as employer rules. Passing these checks is not proof of employer permission. The result still states `policy_conflicts_checked=false`; human/authorized agent evaluation of the actual company rules remains essential.

Don't commit or upload private company instructions, code, architecture, identifying tokens or user/customer data into `Enyina/ai-engineering-config` or its issue/PR history. For real employer implementation and tests, stay in the employer-approved project tooling and storage.

## Provenance in every suggestion

- `matches[].origin` identifies the source of the comparison: public research interpreted in a personal catalog; these are hypotheses and have public reference links under `evidence`.
- `candidate_personal_guidance[].source` identifies the original personal rule ID and personal GitHub policy file; `references` provides public research links.
- `status=candidate_only_not_employer_policy` means exactly that: it is available to *consider*, not automatically active.
- Employer-specific or project-specific personal rules never appear in this external advisory list.

Nothing is automatically installed, synchronized, pushed or enacted. A useful general idea may be adopted inside a company project only when compatible with its policy, architecture and authorization; approval and testing occur there.

## Design principle

**Shared research and experience can inform decisions across contexts without transferring ownership of instructions.** Employer silence invites evidence-backed engineering judgment, not unreviewed rule import.
