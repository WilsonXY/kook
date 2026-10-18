"""Dump / replace narration string literals in a chapter script.
python narration.py dump ch01.py        -> prints  id|text  for every narration literal (and likely on-screen sentences)
python narration.py apply ch01.py map.json  -> replaces texts by id (JSON {"id": "new text"})
Use it to rewrite a whole script at once, e.g. after a humanizer pass. Ids come from dump; dump again after applying."""
import ast, json, sys
FUNCS = {"say", "narrate", "chapter_intro", "new_section", "say_only"}

def literals(src):
    tree = ast.parse(src)
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and getattr(n.func, "attr", getattr(n.func, "id", None)) in FUNCS:
            args = n.args[:]
            if getattr(n.func, "attr", "") == "chapter_intro":
                args = args[3:4]
            elif getattr(n.func, "attr", "") == "new_section":
                args = args[1:2]
            else:
                args = args[:1]
            for a in args:
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    out.append(a)
    # string lists said in loops: any long sentence-like literal not already caught
    seen = {(a.lineno, a.col_offset) for a in out}
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and (n.lineno, n.col_offset) not in seen:
            v = n.value
            if len(v) > 25 and " " in v and v.rstrip()[-1:] in ".?!" and "\n" not in v and not v.startswith("("):
                out.append(n)
    out.sort(key=lambda a: (a.lineno, a.col_offset))
    return out

src = open(sys.argv[2], encoding="utf-8").read()
lits = literals(src)
if sys.argv[1] == "dump":
    for i, a in enumerate(lits):
        print(f"{i}|L{a.lineno}|{a.value}")
else:
    m = {int(k): v for k, v in json.load(open(sys.argv[3], encoding="utf-8")).items()}
    lines = src.splitlines(keepends=True)
    offs = [0]
    for l in lines:
        offs.append(offs[-1] + len(l))
    def pos(ln, col):  # col is utf-8 byte offset
        line = lines[ln - 1]
        return offs[ln - 1] + len(line.encode("utf-8")[:col].decode("utf-8"))
    for i in sorted(m, reverse=True):
        a = lits[i]
        s, e = pos(a.lineno, a.col_offset), pos(a.end_lineno, a.end_col_offset)
        src = src[:s] + json.dumps(m[i], ensure_ascii=False) + src[e:]
    ast.parse(src)
    open(sys.argv[2], "w", encoding="utf-8").write(src)
    print("replaced", len(m))
