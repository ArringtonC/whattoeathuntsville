# Tag grid spreadsheet: one row per restaurant, one yes/no column per popular tag.
#   python3 scripts/tag-grid.py export   writes restaurant-tags.xlsx
#   python3 scripts/tag-grid.py import   copies label, reviewed, and tags back into the restaurant files
# If menu-check.json exists (from the website check), tags the menu did not show are red, unclear ones yellow,
# and a "Menu check" sheet lists websites, closures and suggested tags.
import glob, json, os, sys
from collections import Counter
from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = os.path.join(os.path.dirname(__file__), "..")
DIR = os.path.join(ROOT, "src", "content", "restaurants")
XLSX = os.path.join(ROOT, "restaurant-tags.xlsx")
CHECK = os.path.join(ROOT, "menu-check.json")
FIXED = ["Restaurant", "City", "Label", "Reviewed"]
TAIL = ["Other tags", "slug"]
# Always offered, even before any restaurant uses them.
ALWAYS = ["tacos", "birria", "wings", "pizza", "burgers", "catfish", "fried chicken", "BBQ", "pho", "ramen", "sushi", "brunch",
          "breakfast", "dessert", "coffee", "margaritas", "cocktails", "vegan", "food truck", "Black-owned", "late night",
          "drive-thru", "cash only", "patio", "happy hour", "kid-friendly", "budget-friendly", "date night"]
LABELS = ["great", "good", "first-look", "none"]

def read(path):
    head, body = open(path).read().split("\n---\n", 1)
    keys, vals = [], {}
    for line in head.split("\n")[1:]:
        k, _, v = line.partition(": "); keys.append(k); vals[k] = v
    return keys, vals, body

def files():
    return {os.path.basename(p)[:-3]: p for p in sorted(glob.glob(os.path.join(DIR, "*.md")))}

def export():
    data = {slug: read(p)[1] for slug, p in files().items()}
    counts = Counter(t for v in data.values() for t in json.loads(v.get("tags", "[]")))
    popular = [t for t, n in counts.most_common() if n >= 2]
    tag_cols = ALWAYS + [t for t in popular if t.lower() not in [a.lower() for a in ALWAYS]]
    tag_cols = tag_cols[:60]
    cols = FIXED + tag_cols + TAIL

    wb = Workbook(); ws = wb.active; ws.title = "Tags"
    ws.append(cols)
    for slug, v in sorted(data.items(), key=lambda kv: json.loads(kv[1]["name"]).lower()):
        tags = json.loads(v.get("tags", "[]"))
        lower = {t.lower() for t in tags}
        other = [t for t in tags if t.lower() not in {c.lower() for c in tag_cols}]
        ws.append([json.loads(v["name"]), v.get("city", ""), v.get("label", "none"), "yes" if v.get("draft") == "false" else "no"]
                  + ["yes" if c.lower() in lower else "" for c in tag_cols] + [", ".join(other), slug])

    n = ws.max_row
    first_tag, last_tag = len(FIXED) + 1, len(FIXED) + len(tag_cols)
    yes_no = DataValidation(type="list", formula1='"yes,no"', allow_blank=True); ws.add_data_validation(yes_no)
    yes_no.add(f"D2:D{n}")
    yes_no.add(f"{get_column_letter(first_tag)}2:{get_column_letter(last_tag)}{n}")
    label = DataValidation(type="list", formula1='"' + ",".join(LABELS) + '"', allow_blank=False); ws.add_data_validation(label)
    label.add(f"C2:C{n}")

    green = PatternFill("solid", start_color="C8E6C9"); bold = Font(bold=True)
    check = {c["slug"]: c for c in json.load(open(CHECK))} if os.path.exists(CHECK) else {}
    fills = {"no": PatternFill("solid", start_color="F4B6B6"), "unclear": PatternFill("solid", start_color="FFE9A8")}
    for r in range(2, n + 1):
        found = {t["tag"].lower(): t for t in check.get(ws.cell(row=r, column=len(cols)).value, {}).get("tags", [])}
        for c in range(first_tag, last_tag + 1):
            t = found.get(str(ws.cell(row=1, column=c).value).lower())
            if t and t["result"] in fills:
                cell = ws.cell(row=r, column=c)
                # Added before the green rule, so it wins while the cell still says yes.
                ws.conditional_formatting.add(cell.coordinate, CellIsRule(operator="equal", formula=['"yes"'], fill=fills[t["result"]], stopIfTrue=True))
                cell.comment = Comment(f"Menu check: {t['result']}. {t.get('note', '')}", "menu check")
    ws.conditional_formatting.add(f"D2:{get_column_letter(last_tag)}{n}", CellIsRule(operator="equal", formula=['"yes"'], fill=green))
    for c in range(1, len(cols) + 1):
        cell = ws.cell(row=1, column=c); cell.font = bold
        if first_tag <= c <= last_tag:
            cell.alignment = Alignment(text_rotation=90, horizontal="center")
            ws.column_dimensions[get_column_letter(c)].width = 4.5
    ws.row_dimensions[1].height = 120
    ws.column_dimensions["A"].width = 30; ws.column_dimensions["B"].width = 12
    ws.column_dimensions["C"].width = 11; ws.column_dimensions["D"].width = 9
    ws.column_dimensions[get_column_letter(len(cols) - 1)].width = 40
    ws.column_dimensions[get_column_letter(len(cols))].hidden = True   # slug links the row to its file
    ws.freeze_panes = "B2"
    if check:
        ms = wb.create_sheet("Menu check")
        ms.append(["Restaurant", "Status", "Not on menu", "Unclear", "Suggested tags", "Website", "Menu used", "Notes"])
        names = {slug: json.loads(v["name"]) for slug, v in data.items()}
        for c in sorted(check.values(), key=lambda c: names.get(c["slug"], c["slug"]).lower()):
            pick = lambda res: ", ".join(t["tag"] for t in c["tags"] if t["result"] == res)
            ms.append([names.get(c["slug"], c["slug"]), c["status"], pick("no"), pick("unclear"), ", ".join(c["suggested"]),
                       c["website"], c["menuUrl"], c.get("notes", "")])
        for col, w in zip("ABCDEFGH", (28, 11, 24, 24, 34, 30, 30, 80)): ms.column_dimensions[col].width = w
        for cell in ms[1]: cell.font = bold
        ms.freeze_panes = "B2"
    wb.save(XLSX)
    print(f"Wrote restaurant-tags.xlsx: {n - 1} restaurants x {len(tag_cols)} tag columns")

def imp():
    ws = load_workbook(XLSX).active
    head = [c.value for c in ws[1]]
    tag_cols = head[len(FIXED):-len(TAIL)]
    paths, changed, problems = files(), 0, []
    for r, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        rec = dict(zip(head, row))
        slug = rec.get("slug")
        if slug not in paths: problems.append(f"row {r}: unknown restaurant"); continue
        keys, v, body = read(paths[slug])
        label = str(rec.get("Label") or "none").strip().lower()
        if label not in LABELS: problems.append(f"row {r} ({rec['Restaurant']}): Label must be {', '.join(LABELS)}"); continue
        tags = [c for c in tag_cols if str(rec.get(c) or "").strip().lower() in ("yes", "y", "x")]
        tags += [t.strip() for t in str(rec.get("Other tags") or "").split(",") if t.strip() and t.strip().lower() not in [x.lower() for x in tags]]
        new = dict(v)
        new["label"] = label
        new["tags"] = json.dumps(tags)
        new["draft"] = "false" if str(rec.get("Reviewed") or "").strip().lower() == "yes" else "true"
        if new != v:
            order = [k for k in keys if k in new] + [k for k in new if k not in keys]
            open(paths[slug], "w").write("---\n" + "\n".join(f"{k}: {new[k]}" for k in order) + "\n---\n" + body)
            changed += 1
    print(f"{changed} restaurants updated from restaurant-tags.xlsx")
    for p in problems: print("  fix:", p)
    if problems: sys.exit(1)

{"export": export, "import": imp}[sys.argv[1] if len(sys.argv) > 1 else "export"]()
