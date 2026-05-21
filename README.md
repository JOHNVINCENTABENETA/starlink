# Starlink Data Usage Scraper 🛰️

A Python scraper that extracts **daily and monthly data usage (GB)** from saved Starlink account HTML pages and exports everything into a single organized CSV file.

---

## Requirements

- Python 3.8+
- pip

---

## Setup & Usage

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/starlink-scraper.git
cd starlink-scraper
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your HTML files
Place the saved Starlink billing-period HTML pages inside the `html_pages/` folder:
```
html_pages/
  Nov-Dec.html
  Dec-Jan.html
  Jan-Feb.html
  Feb-Mar.html
  Mar-Apr.html
  May-Jun.html
```

### 5. Run the scraper
```bash
python scraper.py
```

---

## Output

One CSV file is generated: **`starlink_data_usage.csv`**

It combines monthly totals and daily rows in chronological order:

| Column | Description |
|--------|-------------|
| `type` | `MONTHLY TOTAL` or `daily` |
| `date` | Month + year for totals (e.g. `November 2024`), or `YYYY-MM-DD` for daily rows |
| `data_usage_gb` | Data consumed in GB (2 decimal places) |
| `bar` | Visual bar chart of usage relative to the peak |
| `billing_period` | Starlink billing period label (daily rows only) |

### Example
```
type,          date,           data_usage_gb,  bar,                              billing_period
MONTHLY TOTAL, November 2024,  201.50,         ██████████░░░░░░░░░░  201.50 GB,
daily,         2024-11-17,     17.54,          ████████░░░░░░░░░░░░  17.54 GB,   Nov 17-Dec 16 2024
daily,         2024-11-18,     13.24,          ██████░░░░░░░░░░░░░░  13.24 GB,   Nov 17-Dec 16 2024
...
MONTHLY TOTAL, December 2024,  590.08,         ████████████████████  590.08 GB,
daily,         2024-12-01,     12.17,          ██████░░░░░░░░░░░░░░  12.17 GB,   Nov 17-Dec 16 2024
```

### Terminal output on run
```
  🛰️  Starlink Data Usage — Summary
  ──────────────────────────────────────────────
  📅  Days tracked   : 182
  📊  Total usage    : 1882.90 GB
  📈  Daily average  : 10.35 GB
  🔥  Peak day       : 45.09 GB  (2025-05-17)
  ──────────────────────────────────────────────

  📆  Monthly Breakdown
  ──────────────────────────────────────────────
  November 2024   ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░  201.50 GB
  December 2024   ████████████████████████████████████████  590.08 GB
  January 2025    ██████████████████████████░░░░░░░░░░░░░░  380.55 GB
  February 2025   ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  120.80 GB
  March 2025      █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░  197.55 GB
  April 2025      ████████████████████░░░░░░░░░░░░░░░░░░░░  297.59 GB
  May 2025        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   94.83 GB
  ──────────────────────────────────────────────

  ✅  starlink_data_usage.csv — daily + monthly combined
```

---

## How It Works

The Starlink account page renders a **MUI bar chart (SVG)** for each billing period. The scraper:

1. Reads each HTML file from the `html_pages/` folder
2. Parses the HTML with **BeautifulSoup**
3. Reads the Y-axis tick labels (e.g. `0 GB`, `20 GB`, `40 GB`) and their SVG `translate` positions to compute a pixel-to-GB scale factor
4. Converts each bar's pixel height to a GB value
5. Groups daily data by calendar month to compute monthly totals
6. Writes one combined CSV: a **MONTHLY TOTAL** header row followed by each day in that month

---

## Project Structure
```
starlink-scraper/
├── html_pages/             ← place your Starlink HTML files here
│   ├── Nov-Dec.html
│   ├── Dec-Jan.html
│   ├── Jan-Feb.html
│   ├── Feb-Mar.html
│   ├── Mar-Apr.html
│   └── May-Jun.html
├── scraper.py              ← main scraping script
├── requirements.txt        ← dependencies + usage steps
├── README.md
└── starlink_data_usage.csv ← generated after running scraper.py
```
