# Replace retired Muse Spark with two simultaneous OpenCode reviews

**Context.** The October 17 update on [#36](https://github.com/WilsonXY/kook/issues/36#issuecomment-6235389709) records that the free Muse Spark reviewer is retired and plain OpenCode 2 `run` can write files. In T3 thread `a5d3e7f4-69b2-4db4-9d05-a374cf569567`, the owner chose `opencode/deepseek-v4.1-flash-free` and `opencode/glm-5.3-flash-free`, both at max effort, to replace it.

**Decision.** The normal route still starts with Codex Sol at high effort. Its fallback is now a pair: one fresh review from each chosen OpenCode model, started simultaneously on the same diff and scope. Wait for both, judge both sets of findings, and repeat the pair on every re-review round. A missing, failed or empty review leaves the round incomplete and must be reported. The separate route for Sol implementations stays Claude Opus, then Codex Astra.

Inside T3, the existing delegation and worktree checks apply to each child. If T3 cannot run these models, use the CLI. OpenCode 2.0.32 accepts `--model provider/model#max`; use `--agent plan` in a separate fresh worktree per reviewer and apply the existing no-write instructions, Git checks and cleanup to each. Plan mode is not a read-only sandbox. Model and effort evidence can be read from `opencode session export <session>`.

**Why here.** Model choices and local CLI settings belong in `profile.md`. The portable review skill already defers to this routing, so it needs no change. Scenario profile excerpts are updated alongside it; a new scenario exercises the unavailable-Codex fallback from #36.

**Rejected.** Picking just one replacement, running them sequentially, or treating them as alternatives: the owner explicitly requested both at once. Changing the Sol-implementer exception is outside this request.

**Verification limit.** Both model IDs appear in the installed catalog and session exports record `variant: max`. Live CLI smoke tests on this machine could not produce replies: normal mode returned an expired API key (HTTP 401), and standalone mode returned a free-tier restriction (HTTP 403). These failures do not count as reviews.

**Reference.** The installed 2.0.32 CLI's `run --help` confirms the `provider/model#variant` syntax and `--agent` option; OpenCode's [config schema](https://opencode.ai/config.json) also defines model variants.
