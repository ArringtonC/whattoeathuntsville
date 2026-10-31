# Copies edits from the shared Restaurant List into the restaurant files.
# Usage: python3 scripts/sync-from-list.py <folder of exported JSON docs>
# Claude exports the list with ArtifactData (list, out_dir) and runs this, then `npm run deploy`.
import glob, json, os, sys

SRC = sys.argv[1]
DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "restaurants")
FIELDS = ["label", "tags", "occasions", "verdict", "bestDish", "status", "draft"]

def frontmatter(text):
    head, body = text.split("\n---\n", 1)
    lines = head.split("\n")[1:]  # drop opening ---
    return lines, body

changed = 0
for path in glob.glob(os.path.join(SRC, "**", "*.json"), recursive=True):
    doc = json.load(open(path))
    slug = doc.get("id") or os.path.basename(path)[:-5]
    data = doc.get("data", doc)
    md = os.path.join(DIR, f"{slug}.md")
    if not os.path.exists(md):
        print("skip, no file:", slug); continue
    lines, body = frontmatter(open(md).read())
    values = {k: v for k, v in (l.split(": ", 1) for l in lines if ": " in l)}
    new = dict(values)
    for k in ("label", "status"):
        if data.get(k): new[k] = data[k]
    for k in ("tags", "occasions"):
        if isinstance(data.get(k), list): new[k] = json.dumps(data[k])
    if data.get("verdict", "").strip(): new["verdict"] = json.dumps(data["verdict"].strip())
    else: new.pop("verdict", None)
    dish = (data.get("bestDish") or {}).get("name", "").strip()
    if dish:
        old = json.loads(values["bestDish"]) if "bestDish" in values else {}
        new["bestDish"] = json.dumps({**old, "name": dish})
    new["draft"] = "false" if data.get("reviewed") else "true"
    if new != values:
        order = [l.split(": ", 1)[0] for l in lines if ": " in l]
        keys = order + [k for k in new if k not in order]
        out = "---\n" + "\n".join(f"{k}: {new[k]}" for k in keys if k in new) + "\n---\n" + body
        open(md, "w").write(out); changed += 1
print(f"{changed} restaurant files updated")
