"""Run with Python, Playwright and system Chromium. Screenshots are optional."""
from pathlib import Path
import csv, json, collections, math
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent.parent
D=R/'dashboard';SRC=R/'data'/'commercepulse_detailed_monthly_facts.csv'
rows=list(csv.DictReader(SRC.open(encoding='utf-8')))
assert len(rows)==7440
for row in rows:
 v=lambda k:float(row[k])
 assert abs(v('net_revenue')-(v('gross_order_value')-v('discounts')-v('cancelled_value')-v('return_value')))<.011
 assert abs(v('contribution')-(v('net_revenue')-v('cogs')-v('logistics_cost')-v('payment_fees')-v('marketing_spend')))<.011
 assert abs(v('logistics_cost')-v('forward_shipping')-v('reverse_shipping'))<.011
 assert v('orders')>=v('shipped_orders')>=v('returned_orders')>=0
 assert v('shipped_orders')>=v('late_orders')>=0
fy=sum(float(r['net_revenue']) for r in rows if r['fy']=='FY2026-27')
assert 168_585_780<fy<168_585_783
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1600,'height':1080},accept_downloads=True)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 html=(D/'index.html').read_text().replace('<link rel="stylesheet" href="styles.css">','').replace('<script src="data.js"></script><script src="app.js"></script>','')
 page.set_content(html)
 page.add_style_tag(content=(D/'styles.css').read_text())
 page.add_script_tag(content=(D/'data.js').read_text())
 page.add_script_tag(content=(D/'app.js').read_text())
 all_names=['overview','growth','customer','economics','returns','fulfillment','forecast']
 for target in all_names:
  page.locator(f'[data-page="{target}"]').click()
  assert page.locator('.kpi').count()==6
  assert page.locator('.chart-panel').count()==4
  assert page.locator('.insight').count()==3
  assert page.locator('svg.chart-svg').count()==4
  assert page.locator('svg .value').count()>=10
 page.locator('[data-page="overview"]').click()
 initial=page.locator('.kpi-val').first.inner_text()
 page.locator('#category').select_option('Fashion')
 assert page.locator('.kpi-val').first.inner_text()!=initial
 page.locator('#region').select_option('East')
 page.locator('#channel').select_option('Paid Media')
 assert page.locator('.kpi-val').first.inner_text().startswith('₹')
 page.locator('#reset').click()
 assert page.locator('.kpi-val').first.inner_text()==initial
 page.locator('#fy').select_option('FY2025-26')
 fytd_value=page.locator('.kpi-val').first.inner_text()
 page.locator('#fytd').uncheck()
 assert page.locator('.kpi-val').first.inner_text()!=fytd_value
 # Validated browser-side CSV export.
 with page.expect_download(timeout=10000) as dl_info:
  page.locator('#export').click()
 dl=dl_info.value
 assert dl.suggested_filename.endswith('.csv')
 page.locator('[data-page="forecast"]').click()
 page.locator('#fy').select_option('FY2026-27')
 base=page.locator('.kpi-val').nth(4).inner_text()
 page.locator('#convRange').fill('15')
 next_value=page.locator('.kpi-val').nth(4).inner_text()
 assert base!=next_value,(base,next_value)
 assert not errors,errors
 browser.close()
print('PASS | 7,440 record reconciliation | FYTD | filters | 7 pages | SVG labels | CSV export | scenario')
