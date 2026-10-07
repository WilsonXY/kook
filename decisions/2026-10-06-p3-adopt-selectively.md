# p3-stack / pstack: adopt methods, not the stack

**Context.** p3-stack (a T3 fork of poteto's pstack) was studied as a possible base (threads e23c2096, 41fdc5c2).

**Decision.** Kook keeps its own delivery cycle and takes individual methods (UI proof, later others). Don't run p3's installer.

**Why.** p3's 51 skills and 23 playbooks are far more than this workflow needs. Its installer writes into `~/.agents/skills`, which links into Kook.

**Rejected.** A 12-file integration plan. A 4-file version shipped instead: Kook PR #5 (2 files) and Bokli PR #67 (its proof script and `AGENTS.md`).
