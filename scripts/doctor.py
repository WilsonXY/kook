#!/usr/bin/env python3
"""Fast structural checks for the skills in this repo. No network, no LLM.
FAIL lines exit 1 (CI blocks the PR); WARN lines are advice.
Usage: scripts/doctor.py [repo-root]
Install state (links, live copy) is checked by sync-skills.sh --check, not here.
"""
import pathlib, re, sys

try:
    import yaml
except ImportError:
    sys.exit("doctor.py needs PyYAML: pip install pyyaml (or apt install python3-yaml)")

PORTABLE = "dev-skills"  # rules for this folder: dev-skills/README.md
WORD_BUDGET = 1200  # SKILL.md body words before detail should move to references/
# Personal setup (models, CLIs, hosts, projects) belongs in profile.md, not in portable skills.
BANNED = re.compile(
    r"gpt-\d[\w.-]*|claude-(?:opus|sonnet|haiku|fable)[\w.-]*|opencode/[\w.-]+"
    r"|\b(?:codex exec|opencode run|codex|opencode|claude code|cursor|gemini cli|antigravity|windsurf|copilot)\b"
    r"|\b(?:claude -p|gemini -p)\b|\btailscale\b|\bbokli\b|\bpenguin\b",
    re.I,
)
# An instruction to go use another skill. Single-word names only after load/invoke/follow, so "use `gh`" is not a route.
ROUTE = re.compile(
    r"\b(?:use|follow|see|run|load|invoke|skill)\W+`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`"
    r"|\b(?:load|invoke|follow)\W+`([a-z][a-z0-9]*)`"
    r"|`([a-z][a-z0-9-]*)` skill\b",
    re.I,
)

repo = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parents[1]).resolve()
results = []


def report(level, where, msg):
    results.append((level, str(where), msg))


skills = {}
for md in sorted(repo.rglob("SKILL.md")):
    if ".git" in md.parts:
        continue
    rel = md.relative_to(repo)
    m = re.match(r"---\n(.*?)\n---\n(.*)", md.read_text(), re.S)
    if not m:
        report("FAIL", rel, "no frontmatter")
        continue
    fm, body = m.groups()
    try:
        meta = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        report("FAIL", rel, f"invalid YAML frontmatter, so the skill won't load (quote values containing ': '): {e.problem}")
        meta = None
    meta = meta if isinstance(meta, dict) else {}
    if meta.get("name") != md.parent.name:
        report("FAIL", rel, f"frontmatter name must equal the folder name '{md.parent.name}'")
    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        report("FAIL", rel, "no description")
    elif len(desc) > 1024:
        report("FAIL", rel, f"description is {len(desc)} characters, over 1024")
    words = len(body.split())
    if words > WORD_BUDGET:
        report("WARN", rel, f"{words} words (budget {WORD_BUDGET}); move detail into references/")
    skills[md.parent.name] = (rel, md.parent)

portable_root = repo / PORTABLE
portable = {n for n, (rel, _) in skills.items() if rel.parts[0] == PORTABLE}

for f in sorted(portable_root.rglob("*.md")) if portable_root.is_dir() else []:
    for ln, line in enumerate(f.read_text().splitlines(), 1):
        for hit in BANNED.finditer(line):
            report("FAIL", f"{f.relative_to(repo)}:{ln}", f"portable text names '{hit.group(0)}'; move it to profile.md")

for name, (rel, folder) in skills.items():  # the skill and its reference files
    for f in sorted(folder.rglob("*.md")):
        for ln, line in enumerate(f.read_text().splitlines(), 1):
            for ref in {"".join(groups) for groups in ROUTE.findall(line)} - set(skills):
                report("FAIL", f"{f.relative_to(repo)}:{ln}", f"routes to `{ref}`, which is not a skill in this repo")

# Behaviour scenarios for scripts/eval.sh: evals/<skill>/<scenario>.md
for f in sorted((repo / "evals").glob("*/*.md")):
    rel, folder = f.relative_to(repo), f.parent.name
    text = f.read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    try:
        meta = yaml.safe_load(m.group(1)) if m else None
    except yaml.YAMLError:
        meta = None
    if folder not in portable:
        report("FAIL", rel, f"evals/{folder}/ does not match a skill in {PORTABLE}/")
    skill_lines = re.findall(r"^skill:.*$", m.group(1), re.M) if m else []
    if not isinstance(meta, dict) or skill_lines != [f"skill: {folder}"]:
        report("FAIL", rel, f"frontmatter must have the plain line 'skill: {folder}' (no quotes or comments)")
    for heading in ("Task", "Pass if"):
        sec = re.search(rf"^## {heading}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        if not sec or not sec.group(1).strip():
            report("FAIL", rel, f"needs a non-empty '## {heading}' section")

readme = portable_root / "README.md"
if portable or readme.exists():
    listed = set(re.findall(r"^\|\s*([a-z][a-z0-9-]*)\s*\|", readme.read_text(), re.M)) if readme.exists() else set()
    for n in sorted(portable - listed):
        report("FAIL", skills[n][0], "not listed in dev-skills/README.md")
    for n in sorted(listed - portable):
        report("FAIL", readme.relative_to(repo), f"lists '{n}', which has no SKILL.md")

for level, where, msg in sorted(results, key=lambda r: r[0]):
    print(f"{level}  {where}  {msg}")
fails = sum(r[0] == "FAIL" for r in results)
print(f"{fails} FAIL, {len(results) - fails} WARN across {len(skills)} skills")
sys.exit(1 if fails else 0)
