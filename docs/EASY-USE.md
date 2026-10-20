# Just ask for what you want

For an investigation, simply say **\"Investigate why this failed; show the evidence and don't fix anything yet.\"** The project rules now require an evidence-first sequence before claiming a cause. In a new chat, browser or assistant that cannot read the configuration, open [Use Anywhere](../USE-ANYWHERE.md) and copy its short self-contained instruction. A GitHub link alone does not install behavior in all AI products.

The default user experience is **no commands, no rule names, and no choosing an AI model**. Open your project in Codex, Claude Code, Cursor or Antigravity and describe the actual outcome:

> Make the garment editor easier to use on a phone.

> Improve how my portfolio presents my work.

> Find a safer way to handle retries.

The agent reads the project's existing instructions, then does the research and compares relevant approaches. It should explain the choice in ordinary English, show credible source links, carry out authorized work when asked, test it, create a focused commit when allowed and add readable release notes. For a substantial design choice it should offer genuinely different options; for small changes it should follow existing conventions without excessive research.

The agent **may** use the shared private configuration's intelligence advisor if that repository is available in its environment. It must not claim it used the library unless it actually accessed it. Private repositories do not automatically become available to all applications just because a link was added. No project-specific rule is to be copied across employers.

## Optional one-sentence terminal helper

From the folder of a verified personal project, the optional helper accepts ordinary English and automatically identifies the project by its registered GitHub origin and ownership marker:

```sh
python3 /path/to/ai-engineering-config/bin/ask "improve the garment editor layout"
```

It infers whether the question is about design or engineering, checks that it is the right project, then shows a short set of sourced options. No project ID, feature ID, or JSON output is required.

From an employer project that has an explicit employer ownership marker, the same command shows **external advice only**, not applied rules.

For public, general employer advice from elsewhere:

```sh
python3 /path/to/ai-engineering-config/bin/ask --work "make retries safer"
```

Use a non-confidential description. Do not paste private company facts into a public or personal research process. This is entirely read-only.

If you prefer the shortest possible terminal command, you can configure your shell's own shortcut to run that helper. The repository **does not modify your shell settings automatically**.

## Important limits

- If an app cannot read your private central repository, agents can still follow the local project instructions and independently research public references. Automatic central library access is **not guaranteed**.
- Personal project detection intentionally refuses a missing or unfamiliar GitHub origin or missing ownership marker. Never add an arbitrary origin just to bypass checks.
- Research suggestions are *hypotheses* to evaluate, not approved organizational rules, and nothing is written until an authorized development task proceeds.
- Source checks still run twice daily and flag changes for review; they do not automatically rewrite policies.

## Short investigation questions

The optional one-sentence helper recognizes questions like `python3 bin/ask "investigate why this failed"` and shows the evidence-first steps instead of unrelated design options. That output is only a plan, not a finding: an assistant with authorized tools still needs to inspect real evidence.
