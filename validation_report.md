# QA Report — CommercePulse

**Dashboard type:** fully offline HTML/JavaScript + SVG portfolio analytics.  
**Dataset:** deterministic synthetic e-commerce sample; real-world data is not represented.

## Automated checks

| Check | Result |
|---|---|
| Detailed underlying fact rows | 7,440 |
| Consolidated monthly Excel-source rows | 1,860 |
| Reporting calendar | 31 consecutive months, Apr 2024–Oct 2026 |
| Net revenue reconciliation (each detailed record) | PASS |
| Contribution reconciliation (each detailed record) | PASS |
| Logistics forward + reverse reconciliation | PASS |
| Excel monthly aggregate and detailed CSV grand totals | PASS |
| Order/shipped/returned/delayed count constraints | PASS |
| Seven pages load without JavaScript errors | PASS |
| Each page includes six KPI cards, four chart visuals, and three dynamic insights | PASS |
| SVG chart value labels present on every page | PASS |
| FYTD on/off changes comparable period logic | PASS |
| Category, region, channel slicers and Reset function | PASS |
| Export selected data as CSV | PASS |
| Forecast scenario slider updates contribution | PASS |
| GitHub PNG + JPEG cover and seven page screenshots | 8 images each |
| LinkedIn PNG + JPEG cover and seven page screenshots | 8 images each |

Data aggregate checks and FY-period totals are recorded in [`data/data_quality_checks.json`](../data/data_quality_checks.json).

### Reproduction

- `python build_data.py` — produce deterministic synthetic CSV and embedded dashboard data.
- `python build_excel.py` — produce Excel workbook (requires `artifact_tool`).
- `python create_validation.py` — execute data reconciliation checks and create JSON.
- `python tests/smoke_test.py` — UI/CSV/browser smoke test (requires Chromium and Playwright).
- `python create_screenshots.py` — create 32 image files (requires Chromium, Playwright and Pillow).

**Known modeling boundaries:** monthly segment/payment aggregates are not individual orders; user-level retention, causal ROAS and audited P&L cannot be inferred. Forecast projections are heuristic financial sensitivities. Browser screenshot capture uses inline-injected local HTML/CSS/JS for automated testing; the shipped dashboard retains offline file-open behavior with separate asset files.
