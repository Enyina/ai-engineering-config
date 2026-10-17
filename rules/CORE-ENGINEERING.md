# Core engineering rules (shared, portable)

Status: approved workflow rules; apply when relevant to the project. These are guidelines to adopt in each agent's supported instruction mechanism, not magically active in all tools.

1. **Inspect before editing.** Establish actual repository state, feature behavior and existing conventions before changing code. Never assume remote code matches uncommitted local work.
2. **Reverse engineer first, proportionately.** Clarify the problem and success criteria; inspect current implementation; study proven public/product/open-source references when useful; compare strengths, weaknesses and constraints; independently implement and measure. Do not blindly copy source, proprietary assets or protected content.
3. **One source of truth.** Identify canonical domain state, ownership and persistence. Derived views should not create conflicting copies of state.
4. **Interaction conflict tests.** Where multiple tools respond to the same pointer/keyboard events, model explicit modes and test transitions. A drawing action must not simultaneously trigger viewport orbit.
5. **Protect existing work.** Prefer small reversible changes, feature branches and migration paths; do not overwrite existing applications based on an incomplete inventory.
6. **Evidence-driven completion.** Clearly distinguish committed, built, tested, reviewed and deployed. Never claim verification without results. Test relevant edge cases and saved-state round trips.
7. **Experience into rules.** Record incidents and repeated patterns in a learning note; promote only validated, reusable rules to shared scope. Keep niche instructions in project-specific modules.
8. **Privacy and ownership.** Do not export company-owned code, customer data, internal system details, credentials or proprietary instructions to the personal config repo.

Review date: 2026-10-17.
