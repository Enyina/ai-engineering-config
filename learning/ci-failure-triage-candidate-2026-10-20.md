# Proposed learning: distinguish test infrastructure failures from product defects

Status: **candidate for human review, not an active global rule**
Scope: General engineering verification / CI investigation
Source: Generalized investigation practice; no employer implementation details or confidential logs retained

## Observation
A CI run can report many failed test files even when most failures are third-party test discovery or missing test tooling. The summary alone cannot show which actual product assertions failed or which files are responsible.

## Candidate rule
**When diagnosing a failing CI run, first classify failures by layer before changing production behavior.** Inspect the exact checked-out commit, relevant repo-specific instructions, test discovery rules, lockfile/tool versions, and the steps that passed. Separate:
- build/install failures;
- misplaced or third-party test collection;
- missing environment or framework dependencies;
- genuine failing product assertions;
- existing baseline failures versus introduced regressions;
- unverified integration and runtime behavior.

Do not relax access-control or financial protections just to make tests pass. When tests and implementation disagree, identify the owning contract and decision authority before choosing which to change.

## Exceptions
Use proportionate depth; a single isolated, reproducible test failure does not require an extensive audit. Treat missing logs or inaccessible CI as unknown, not as passed.

## Verification before approving
Reproduce a sample failure with a narrow test selection and the declared toolchain. Confirm relevant tests execute after any discovery exclusions. Compare failure counts before/after and identify tests that changed behavior. Review with an independent example before promoting this candidate into the shared engineering policy.

## Review checklist
- [ ] No duplicate rule under core engineering or evidence requirements
- [ ] No employer-owned information, identifying traces or raw logs included
- [ ] A regression or synthetic CI example demonstrates the benefit
- [ ] Rule is appropriately scoped and does not hide test failures
- [ ] User approves promotion to shared scope
