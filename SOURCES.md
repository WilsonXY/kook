# Sources

What Kook took from other skillsets, so upstream changes can be compared later. "Pinned" is the upstream commit current when the copy was taken. Compare with:
`gh api repos/<repo>/compare/<pinned>...HEAD --jq '.files[].filename'`

## Copied or adapted

| Kook path | Upstream | Pinned | License | Local changes |
|---|---|---|---|---|
| `dev-skills/test-driven-development` | [obra/superpowers](https://github.com/obra/superpowers) `skills/test-driven-development` | `8ca22dba9a94` (2026-09-25) | MIT | Harness-neutral wording; TS/Go/Rust examples |
| `dev-skills/systematic-debugging` | obra/superpowers `skills/systematic-debugging` | `8ca22dba9a94` | MIT | Harness-neutral wording; feedback-loop rule |
| `dev-skills/requesting-code-review` | obra/superpowers `skills/requesting-code-review` | `8ca22dba9a94` | MIT | Rewritten: fresh-context reviewer, static scan, routing via profile |
| `dev-skills/github` | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) `skills/software-development/github` | `688f5d5b28c5` (2026-10-02) | MIT | Trimmed to PR, CI and commit guides; proof attachment |
| `vendor/ponytail` | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `e5ee596c8637` (2026-10-02) | MIT | None |
| `vendor/show-me` | [humanlayer/skills](https://github.com/humanlayer/skills) `plugins/show-me/skills/show-me` | `653b6411c1f7` (2026-10-08) | MIT | None; upstream `LICENSE` copied alongside |

The superpowers pin is the upstream head when the copy was made (2026-10-02); the exact source commit wasn't recorded.

## Ideas borrowed (no files copied)

| Idea | From | Where in Kook |
|---|---|---|
| Scope bar, one file per decision, status buckets, changelog | [mattpocock/skills](https://github.com/mattpocock/skills) `SCOPE.md`, `.out-of-scope/`, buckets | `SCOPE.md`, `decisions/`, `writing/`, `vendor/` |
| "Encode lessons in structure": mechanical rules become checks | poteto's [pstack](https://github.com/cursor/plugins/tree/main/pstack) | `scripts/doctor.py` |
| Skill guards in CI | [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin), [garrytan/gstack](https://github.com/garrytan/gstack) | `.github/workflows/check.yml` |
| Watch a skill fail before changing it; grade with a fresh agent | [obra/superpowers](https://github.com/obra/superpowers) `writing-skills`; compound-engineering `ce-skill-work/references/evaluate.md` | `evals/`, `scripts/eval.sh` |
| Prove UI changes on the real surface | pstack / p3-stack | `full-cycle` step 3, `github` `pr-workflow.md` |
