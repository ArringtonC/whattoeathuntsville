# Restaurant spreadsheet <-> restaurant files.
#   python3 scripts/restaurants-csv.py export   writes restaurants.csv from src/content/restaurants
#   python3 scripts/restaurants-csv.py import   copies edits in restaurants.csv back into the files
# In the sheet, separate several tags (or occasions) with commas: birria, food truck, late night
import csv, glob, json, os, sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
DIR = os.path.join(ROOT, "src", "content", "restaurants")
CSV = os.path.join(ROOT, "sheets", "restaurants.csv")
COLS = ["slug", "name", "city", "area", "cuisines", "label", "tags", "occasions", "best_dish", "verdict", "status", "reviewed"]
LABELS = {"great", "good", "first-look", "none"}
OCCASIONS = {"Date night", "Brunch", "Family", "Quick lunch", "Late night", "Group", "Cheap eats", "Birthday"}
STATUSES = {"open", "temporarily-closed", "closed"}

def read(path):
    text = open(path).read()
    head, body = text.split("\n---\n", 1)
    keys, vals = [], {}
    for line in head.split("\n")[1:]:
        k, _, v = line.partition(": ")
        keys.append(k); vals[k] = v
    return keys, vals, body

def val(raw):
    try: return json.loads(raw)
    except Exception: return raw

def split(cell):
    return [x.strip() for x in cell.replace(";", ",").split(",") if x.strip()]

def export():
    rows = []
    for path in sorted(glob.glob(os.path.join(DIR, "*.md"))):
        _, v, _ = read(path)
        rows.append({
            "slug": os.path.basename(path)[:-3], "name": val(v["name"]), "city": v.get("city", ""), "area": val(v.get("area", "")),
            "cuisines": ", ".join(val(v.get("cuisines", "[]"))), "label": v.get("label", "none"),
            "tags": ", ".join(val(v.get("tags", "[]"))), "occasions": ", ".join(val(v.get("occasions", "[]"))),
            "best_dish": (val(v["bestDish"]) or {}).get("name", "") if "bestDish" in v else "", "verdict": val(v.get("verdict", "")),
            "status": v.get("status", "open"), "reviewed": "yes" if v.get("draft") == "false" else "no",
        })
    with open(CSV, "w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig so Excel shows accents correctly
        w = csv.DictWriter(f, COLS); w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows)} restaurants to restaurants.csv")

def imp_rich(row, v):
    """The extended sheet (food_tags, drink_tags, feature_tags, search_keywords…). Returns fields to set."""
    tags = []
    for col in ("food_tags", "verified_food_tags", "drink_tags", "feature_tags"):
        for t in split(row.get(col, "")):
            if t.lower() not in [x.lower() for x in tags]: tags.append(t)
    words = []
    for part in (row.get("search_keywords") or "").replace("|", ",").split(","):
        w = part.strip().lower()
        if w and w not in words and w not in [t.lower() for t in tags] and w != json.loads(v["name"]).lower(): words.append(w)
    out = {"tags": json.dumps(tags), "searchTerms": json.dumps(words[:40])}
    for col, key in (("address", "address"), ("area", "area")):
        if (row.get(col) or "").strip() and key not in v: out[key] = json.dumps(row[col].strip())
    if (row.get("source_type") or "").strip() == "Official website" and (row.get("website_or_source") or "").startswith("http") and "website" not in v:
        out["website"] = json.dumps(row["website_or_source"].strip())
    return out

def imp():
    changed, problems = 0, []
    with open(CSV, newline="", encoding="utf-8-sig") as f:
        for n, row in enumerate(csv.DictReader(f), start=2):
            slug = (row.get("slug") or "").strip()
            path = os.path.join(DIR, f"{slug}.md")
            if not os.path.exists(path):
                problems.append(f"row {n}: no restaurant file for slug '{slug}'"); continue
            keys, v, body = read(path)
            new = dict(v)
            label = (row.get("label") or "none").strip().lower().replace(" ", "-")
            if label not in LABELS: problems.append(f"row {n} ({slug}): label must be great, good, first-look or none"); continue
            rich = "food_tags" in row
            occ = split(row.get("occasion_tags" if rich else "occasions", ""))
            bad = [o for o in occ if o not in OCCASIONS]
            if bad: problems.append(f"row {n} ({slug}): unknown occasion {bad}; use {sorted(OCCASIONS)}"); continue
            status = (row.get("status") or "open").strip().lower()
            if rich and status not in STATUSES: status = v.get("status", "open")  # extended sheet says "unverified"; keep ours
            if status not in STATUSES: problems.append(f"row {n} ({slug}): status must be open, temporarily-closed or closed"); continue
            new["label"] = label
            if rich: new.update(imp_rich(row, v))
            else: new["tags"] = json.dumps(split(row.get("tags", "")))
            new["occasions"] = json.dumps(occ)
            new["status"] = status
            verdict = (row.get("verdict") or "").strip()
            if verdict: new["verdict"] = json.dumps(verdict)
            else: new.pop("verdict", None)
            dish = (row.get("best_dish") or "").strip()
            if dish: new["bestDish"] = json.dumps({**(val(v["bestDish"]) if "bestDish" in v else {}), "name": dish})
            else: new.pop("bestDish", None)
            new["draft"] = "false" if (row.get("reviewed") or "").strip().lower() in ("yes", "y", "true", "x") else "true"
            if new != v:
                order = [k for k in keys if k in new] + [k for k in new if k not in keys]
                open(path, "w").write("---\n" + "\n".join(f"{k}: {new[k]}" for k in order) + "\n---\n" + body)
                changed += 1
    print(f"{changed} restaurants updated from restaurants.csv")
    for p in problems: print("  fix:", p)
    if problems: sys.exit(1)

if len(sys.argv) > 2: CSV = sys.argv[2]  # import a sheet saved somewhere else
{"export": export, "import": imp}[sys.argv[1] if len(sys.argv) > 1 else "export"]()
