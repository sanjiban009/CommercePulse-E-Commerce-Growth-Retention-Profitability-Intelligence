# Technology Stack — CommercePulse

| Layer | Technologies | Purpose |
|---|---|---|
| UI architecture | HTML5, CSS3, native JavaScript (ES2020) | Responsive Power BI-style navigation, slicers, and management reporting |
| Interactive visuals | Native inline SVG with responsive viewBox | Bar, line, horizontal bar, paired bar, donut, and cost-bridge charts with visible value labels |
| Data preparation | Python 3 standard library (`csv`, `json`, `random`) | Reproducible simulation; currency and operational metric reconciliation |
| Data delivery | `data.js` embedded local JS arrays | Offline operation without CORS restrictions or API dependencies |
| Spreadsheet source | Microsoft Excel `.xlsx` generated with `artifact_tool` | 1,860-row monthly source table, FY performance scorecard, formulas and dictionary |
| Source export | CSV | 7,440 rows at segment/payment level, plus Excel-grain CSV |
| Scenario modelling | JavaScript | YTD-informed illustrative seasonal forecast; interactive conversion / returns / shipping sensitivities |
| QA / screenshot | Python, Playwright, Chromium, Pillow | UI flow validation; PNG and JPEG captures for GitHub and LinkedIn |
| Deployment | Static GitHub Pages, local `file://`, any basic web host | No cloud BI subscription, database or backend needed |

This is not a native Microsoft Power BI Desktop `.pbix`, Tableau workbook, or a production customer data platform. It is a self-contained web analytics project that uses a Power BI-inspired UI pattern.
