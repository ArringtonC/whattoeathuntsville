# Builds src/data/to-try.json: restaurants within 50 miles of Huntsville that we have NOT been to.
#   python3 scripts/to-try.py [osm.json]
# Source: OpenStreetMap (Overpass). Big chains and places we already reviewed are left out.
import glob, json, os, re, sys, urllib.parse, urllib.request
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "src", "data", "to-try.json")
QUERY = '[out:json][timeout:120];nwr["amenity"~"^(restaurant|fast_food|cafe|ice_cream|food_court)$"]["name"](around:80467,34.7304,-86.5861);out tags center;'
CHAINS = {  # shortcut: hand list of national chains; extend when one slips through
    "mcdonalds", "burgerking", "wendys", "tacobell", "kfc", "subway", "chickfila", "sonic", "sonicdrivein", "arbys", "popeyes",
    "popeyeslouisianakitchen", "dominos", "dominospizza", "pizzahut", "papajohns", "littlecaesars", "littlecaesarspizza", "starbucks",
    "dunkin", "dunkindonuts", "wafflehouse", "cracker barrel", "crackerbarrel", "crackerbarreloldcountrystore", "applebees", "chilis",
    "olivegarden", "redlobster", "outback", "outbacksteakhouse", "texasroadhouse", "longhornsteakhouse", "ihop", "dennys", "hardees",
    "zaxbys", "bojangles", "wingstop", "buffalowildwings", "jimmyjohns", "jerseymikes", "jerseymikessubs", "firehousesubs", "panerabread",
    "chipotle", "chipotlemexicangrill", "moes", "moessouthwestgrill", "qdoba", "fivebuys", "fiveguys", "whataburger", "culvers", "dairyqueen",
    "krispykreme", "baskinrobbins", "cookout", "checkers", "rallys", "krystal", "jackinthebox", "captainds", "longjohnsilvers", "churchs",
    "churchschicken", "churchstexaschicken", "raisingcanes", "pandaexpress", "marcospizza", "hungryhowies", "cicis", "cicispizza",
    "goldencorral", "redrobin", "ruby tuesday", "rubytuesday", "logansroadhouse", "ohcharleys", "bonefishgrill", "carrabbas",
    "smoothieking", "tropicalsmoothiecafe", "mcalistersdeli", "newkpubrestaurant", "zoeskitchen", "cookoutrestaurant", "huddlehouse",
    "shoneys", "jimnnicks", "jimnnicksbarbq", "dickeysbarbecuepit", "tacojohns", "steaknshake", "steaknshakes", "bigtee",
}
# Nearest town when the map has no city (shortcut: straight-line to town centers; fine for a label).
TOWNS = {"Huntsville": (34.7304, -86.5861), "Madison": (34.6993, -86.7483), "Harvest": (34.8556, -86.7508), "Hazel Green": (34.9323, -86.5717),
         "Meridianville": (34.8515, -86.5722), "New Market": (34.9101, -86.4278), "Owens Cross Roads": (34.5882, -86.4589), "Gurley": (34.7012, -86.3758),
         "Athens": (34.8029, -86.9717), "Decatur": (34.6059, -86.9833), "Hartselle": (34.4434, -86.9353), "Priceville": (34.5251, -86.8947),
         "Guntersville": (34.3582, -86.2947), "Arab": (34.3281, -86.4958), "Scottsboro": (34.6723, -86.0341), "Albertville": (34.2676, -86.2089),
         "Boaz": (34.2001, -86.1664), "Cullman": (34.1748, -86.8436), "Moulton": (34.4812, -87.2934), "Ardmore": (34.9921, -86.8467),
         "Fayetteville, TN": (35.1520, -86.5705), "Tullahoma, TN": (35.3620, -86.2094), "Winchester, TN": (35.1859, -86.1122), "Pulaski, TN": (35.1998, -87.0308)}
def town(e):
    lat, lon = (e.get("lat"), e.get("lon")) if "lat" in e else (e.get("center", {}).get("lat"), e.get("center", {}).get("lon"))
    if lat is None: return ""
    return min(TOWNS, key=lambda t: (TOWNS[t][0] - lat) ** 2 + ((TOWNS[t][1] - lon) * 0.82) ** 2)
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("'s", "s").replace("’s", "s"))

def fetch():
    req = urllib.request.Request("https://overpass-api.de/api/interpreter", urllib.parse.urlencode({"data": QUERY}).encode(),
                                 headers={"User-Agent": "WhatToEatHuntsville/1.0 (hello@whattoeathuntsville.com)"})
    return json.load(urllib.request.urlopen(req, timeout=180))

def ours():
    names = []
    for p in glob.glob(os.path.join(ROOT, "src", "content", "restaurants", "*.md")):
        m = re.search(r'^name: "(.*)"$', open(p).read(), re.M)
        if m: names.append(norm(re.sub(r"\s*\(.*?\)", "", m.group(1))))
    return names

def main():
    data = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else fetch()
    els = [e for e in data["elements"] if e.get("tags", {}).get("name")]
    counts = Counter(norm(e["tags"]["name"]) for e in els)
    tried = ours()
    seen, out = set(), []
    for e in els:
        t = e["tags"]; n = norm(t["name"])
        if not n or n in seen: continue
        if n in CHAINS or t.get("brand:wikidata") or counts[n] >= 3: continue  # chains
        if any(n == o or (len(o) > 5 and (o in n or n in o)) for o in tried): continue  # we've been
        seen.add(n)
        cuisine = (t.get("cuisine") or "").split(";")[0].replace("_", " ").strip().title()
        out.append({"name": t["name"].strip(), "cuisine": cuisine, "city": t.get("addr:city", "").strip() or town(e),
                    "street": " ".join(x for x in (t.get("addr:housenumber"), t.get("addr:street")) if x)})
    out.sort(key=lambda r: r["name"].lower())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"{len(out)} places to try (from {len(els)} on the map; chains and our {len(tried)} reviewed places left out)")

main()
