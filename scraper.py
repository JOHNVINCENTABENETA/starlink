"""Starlink Data Usage Scraper — python scraper.py -> starlink_data_usage.csv"""
import csv, re
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from bs4 import BeautifulSoup

HTML_DIR = Path("html_pages")

CFG = {
    "Nov-Dec": ("Nov 17-Dec 16 2024",      date(2024,11,17)),
    "Dec-Jan": ("Dec 17 2024-Jan 16 2025", date(2024,12,17)),
    "Jan-Feb": ("Jan 17-Feb 16 2025",      date(2025, 1,17)),
    "Feb-Mar": ("Feb 17-Mar 16 2025",      date(2025, 2,17)),
    "Mar-Apr": ("Mar 17-Apr 16 2025",      date(2025, 3,17)),
    "May-Jun": ("May 17-Jun 16 2025",      date(2025, 5,17)),
}

MONTHS = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
          7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

def parse(stem):
    path = HTML_DIR / f"{stem}.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
    ticks = []
    for t in soup.find_all(class_=lambda c: c and "MuiChartsAxis-tickLabel" in c):
        txt = t.get_text(strip=True)
        if "GB" not in txt: continue
        m = re.search(r"translate\(0,\s*([\d.]+)\)", t.parent.get("transform",""))
        if m: ticks.append((float(m.group(1)), float(re.search(r"[\d.]+", txt).group())))
    ticks.sort(reverse=True)
    ppg = (ticks[0][0] - ticks[-1][0]) / (ticks[-1][1] - ticks[0][1])
    return [round(float(r["height"]) / ppg, 2)
            for r in soup.find_all("rect", class_=lambda c: c and "MuiBarElement-series-y_0" in c if c else False)]

def bar(gb, max_gb, width=30):
    filled = round(gb / max_gb * width) if max_gb else 0
    return "█" * filled + "░" * (width - filled) + f"  {gb:.2f} GB"

# ── Collect data ─────────────────────────────────────────────────────────────
daily, monthly = [], defaultdict(float)
for stem, (label, start) in sorted(CFG.items(), key=lambda x: x[1][1]):
    for i, gb in enumerate(parse(stem)):
        d = start + timedelta(days=i)
        daily.append((d, gb, label))
        monthly[(d.year, d.month)] += gb

all_gb  = [gb for _, gb, _ in daily]
max_day = max(all_gb)
max_mo  = max(monthly.values())

# ── Build combined CSV rows ───────────────────────────────────────────────────
csv_rows, current_mo = [], None
for d, gb, label in daily:
    mo_key = (d.year, d.month)
    if mo_key != current_mo:
        current_mo = mo_key
        mo_total = monthly[mo_key]
        csv_rows.append({
            "type": "MONTHLY TOTAL",
            "date": f"{MONTHS[d.month]} {d.year}",
            "data_usage_gb": f"{mo_total:.2f}",
            "bar": bar(mo_total, max_mo, 40),
            "billing_period": "",
        })
    csv_rows.append({
        "type": "daily",
        "date": str(d),
        "data_usage_gb": f"{gb:.2f}",
        "bar": bar(gb, max_day, 30),
        "billing_period": label,
    })

with open("starlink_data_usage.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, ["type","date","data_usage_gb","bar","billing_period"])
    w.writeheader(); w.writerows(csv_rows)

# ── Terminal summary ──────────────────────────────────────────────────────────
total = sum(all_gb); avg = total/len(all_gb); peak = max(all_gb)
peak_date = str(daily[all_gb.index(peak)][0])
print()
print("  🛰️  Starlink Data Usage — Summary")
print("  " + "─" * 46)
print(f"  📅  Days tracked   : {len(daily)}")
print(f"  📊  Total usage    : {total:.2f} GB")
print(f"  📈  Daily average  : {avg:.2f} GB")
print(f"  🔥  Peak day       : {peak:.2f} GB  ({peak_date})")
print("  " + "─" * 46)
print()
print("  📆  Monthly Breakdown")
print("  " + "─" * 46)
for (y,m), gb in sorted(monthly.items()):
    if gb == 0: continue
    print(f"  {MONTHS[m]} {y:<6} {bar(gb, max_mo, 40)}")
print("  " + "─" * 46)
print()
print("  ✅  starlink_data_usage.csv — daily + monthly combined")
print()
