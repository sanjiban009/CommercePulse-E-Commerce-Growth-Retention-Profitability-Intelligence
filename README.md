# CommercePulse — E-Commerce Growth, Retention & Profitability Intelligence



**Seven-page, Power BI-style, interactive dashboard built with offline HTML, CSS, JavaScript and SVG, supported by Excel and CSV synthetic datasets.** Designed for an Indian online retailer spanning marketplace, paid-media and direct/organic sales across multiple product categories.

**Author:** Sanjiban Das · Analytics & Business Intelligence  
**Sector:** E-Commerce / D2C / Marketplace Retail · **Currency:** INR · **Reporting:** Indian FY (April–March) · **Snapshot:** actuals modeled through October 2026

> **Data integrity disclosure:** All data, financial results and scenarios are fictional and reproducibly generated for a portfolio demonstration. No real customer, retailer or employer data are included. This is **not** a `.pbix` Power BI file; it is an independent, Power BI-inspired web dashboard.

## 🚀 Open the dashboard

1. **Download / clone** the repository, or extract the ZIP.
2. Open **[`dashboard/index.html`](dashboard/index.html)** by double-clicking it in Chrome, Edge, Firefox or Safari.
3. Use the left navigation to switch between seven pages and top slicers to filter financial year, region, category and channel.
4. Move forecast scenario sliders to recalculate the profit outlook; use **Export filtered CSV** to save the active data selection.

The app runs **offline**, with no paid subscription, server, npm, external chart CDN, API key or login. Keep the `dashboard` folder's four files together: `index.html`, `styles.css`, `data.js`, `app.js`.

**GitHub Pages:** The repository also includes a root `index.html` that forwards visitors to `dashboard/index.html`; configure GitHub Pages to publish from the default branch and root `/` directory. No build step required.

## Business problem

Growth in e-commerce often masks material leakage: excessive discounting, low-conversion acquisition channels, reverse-logistics exposure, COD-related returns and variable delivery costs. CommercePulse connects topline, funnel metrics and variable contribution into a single management reporting framework.

## Seven analytical modules

| Page | Decision areas | Key visuals |
|---|---|---|
| **01 Executive Overview** | Realized revenue, orders, margin, category priorities | Monthly net sales, category concentration, channel margins, region demand |
| **02 Growth & Conversion** | Sessions, conversion, marketing efficiency | Monthly CVR, channel net revenue, channel/region conversion |
| **03 Customer & Repeat-Purchase** | New vs returning order demand | Order mix, monthly repeat-order share, category/channel repeat mix |
| **04 Unit Economics** | Profit leakage and cost-to-serve | Revenue-to-contribution bridge, category profit, channel margin, regional profit |
| **05 Returns & COD Risk** | Refunds, cancellations, payment mix | Category return %, COD/prepaid return %, monthly trend, regional refund exposure |
| **06 Fulfillment Intelligence** | Shipping cost, delivery days, SLA risk | On-time %, regional transit days, monthly shipping spend, category costs |
| **07 Forecast & Scenarios** | FY outlook and operating lever sensitivities | Actual/projection revenue, contribution drivers, interactive scenario simulator |

Each page has **six metric cards**, **four SVG charts with visible values/legends**, and **three dynamic, rule-based business insights** recalculated after slicer changes. The forecast page also has **three interactive scenario sliders**.

## Reporting standard and comparisons

- **FY2024–25:** full Apr 2024–Mar 2025 historical modeled period.
- **FY2025–26:** full Apr 2025–Mar 2026 historical modeled period.
- **FY2026–27:** Apr–Oct 2026 modeled observations available as of the project snapshot.
- **MATCHED FYTD ON:** compare **Apr–Oct** for all selected fiscal years to prevent unequal-period comparisons.
- **MATCHED FYTD OFF:** show full historic FY data when available, but **never pretend FY2026–27 Nov–Mar have actuals**.
- **Forecast:** the current FY's unobserved Nov–Mar months are projected separately using prior-year seasonal shape and a capped YTD growth factor. Projections are **illustrative heuristics**, not rigorously backtested predictive models.

## Core reconciliations

```text
Net realized revenue = gross placed order value
                     − discounts
                     − canceled order value
                     − returned order value

Contribution profit = net realized revenue
                    − cost of goods sold
                    − forward and reverse logistics
                    − payment processing fees
                    − allocated marketing spend

Contribution margin = contribution / net realized revenue
Return rate         = returned orders / shipped orders
Conversion rate     = placed orders / modeled visits
On-time rate        = (shipped orders − late orders) / shipped orders
```

**Important:** Returning-order share is an order classification, **not** customer-level retention. The data do not contain persistent customer IDs, so cohort retention and LTV cannot legitimately be inferred. CAC and ROAS are operating allocation proxies. Contribution excludes overhead, depreciation, interest and taxes.

## Files and datasets

```text
CommercePulse_Ecommerce_Intelligence/
├── index.html                                # Root entry (GitHub Pages redirect)
├── README.md
├── dashboard/
│   ├── index.html                            # Double-click this to launch offline
│   ├── styles.css
│   ├── app.js                                # Filters, SVG charts, dynamic decisions, scenarios
│   └── data.js                               # Embedded synthetic dataset; works under file://
├── data/
│   ├── CommercePulse_Synthetic_Ecommerce_Data.xlsx
│   ├── commercepulse_detailed_monthly_facts.csv       # 7,440 rows
│   ├── commercepulse_excel_monthly_facts.csv          # 1,860 rows
│   ├── dataset_manifest.json
│   └── data_quality_checks.json
├── docs/
│   ├── linkedin_post.txt
│   ├── linkedin_role_description_under_250_chars.txt
│   ├── technology_stack.md
│   ├── metric_definitions.md
│   └── validation_report.md
├── screenshots/
│   ├── GitHub/PNG/                         # Cover + 7 pages
│   ├── GitHub/JPEG/                        # Cover + 7 pages
│   ├── LinkedIn/PNG/                       # Cover + 7 pages
│   └── LinkedIn/JPEG/                      # Cover + 7 pages
├── build_data.py                           # Deterministic pure-Python data generator
├── build_excel.py                          # Rebuild XLSX (requires artifact_tool)
└── create_screenshots.py                   # Screenshot utility (requires Chromium, Playwright, Pillow)
```

**The XLSX workbook** contains a start guide, a financial-year scorecard with spreadsheet margin/return/conversion formulas, monthly analytics fact table, and metric dictionary. The detailed CSV contains the **New/Returning** and **COD/Prepaid** breakdowns used by the interactive app, while the workbook uses their aggregated monthly sums.

For LinkedIn, use the prepared images under **`screenshots/LinkedIn/PNG/`** or **`screenshots/LinkedIn/JPEG/`**. Use `docs/linkedin_post.txt` as a starter caption.

## Technology and engineering choices

- **Front end:** semantic HTML5, modern CSS, vanilla ES2020 JavaScript.
- **Visualizations:** browser-native responsive SVG with chart-level data labels. No Chart.js dependency or network request.
- **Data preparation:** deterministic Python standard-library generation; precomputed monthly analytics with reconciliation assertions.
- **Spreadsheet:** XLSX formatted with `artifact_tool` and Excel formulas.
- **Tested interaction:** 7 pages, page navigation, filtering, FYTD, export handler, and scenario reactivity using Chromium and Playwright.
- **Data lineage:** Every dashboard calculation is derived from the included locally embedded facts; no hidden remote source.

-**Tech Stacks:** HTML5 | CSS3 | JavaScript | Python | Advanced Excel | SVG Data Visualization | Business Intelligence | Data Analytics | Financial Modeling | Forecasting | What-If Analysis | Interactive Dashboards | 

## Limitations & responsible use

Synthetic datasets are invented and **not a measured Indian market sample**. Date, mix, revenue and shipping figures are illustrative. The forecast is a scenario-oriented baseline, not validated statistical inference. Order-type grouping cannot establish real retention; true ROAS and CAC would require attribution modeling and identity-level data. Treat the output as a professional architecture and demonstration project rather than a claimed deployment at a real company.

**License:** MIT for the code; synthetic sample data may be reused with attribution.  

<img width="1600" height="1546" alt="07_Forecast_and_Scenarios" src="https://github.com/user-attachments/assets/2c664555-b92b-4a80-b3cf-7efa0884d63c" />
<img width="1600" height="1256" alt="06_Fulfillment_Intelligence" src="https://github.com/user-attachments/assets/d32c781f-82b5-44cf-b876-71ac64e3607d" />
<img width="1600" height="1256" alt="05_Returns_and_COD_Risk" src="https://github.com/user-attachments/assets/fed5e6d8-9688-43d6-9f8a-5838b3ba8a8a" />
<img width="1600" height="1256" alt="04_Unit_Economics" src="https://github.com/user-attachments/assets/d64aaf33-5da2-4fc6-ae3b-c78622f61cda" />
<img width="1600" height="1256" alt="03_Customer_and_Retention" src="https://github.com/user-attachments/assets/4029395d-a94b-47fc-8b23-8044baa2e97e" />
<img width="1600" height="1256" alt="02_Growth_and_Conversion" src="https://github.com/user-attachments/assets/1abbb903-7910-4935-b31b-e2ac9c5bada2" />
<img width="1600" height="1256" alt="01_Executive_Overview" src="https://github.com/user-attachments/assets/415a2d6f-2e5d-4e39-8a66-c1f6da752c73" />
<img width="1600" height="900" alt="00_Project_Cover" src="https://github.com/user-attachments/assets/efbec60a-22f9-4672-a722-92ca0635c1b4" />




