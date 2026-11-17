import json,csv,collections
from pathlib import Path
R=Path(__file__).parent
rows=list(csv.DictReader((R/'data'/'commercepulse_detailed_monthly_facts.csv').open(encoding='utf-8')))
monthly=list(csv.DictReader((R/'data'/'commercepulse_excel_monthly_facts.csv').open(encoding='utf-8')))
checks={}
checks['detailed_fact_rows']=len(rows);checks['monthly_excel_fact_rows']=len(monthly)
checks['month_count']=len({r['month'] for r in rows})
checks['net_revenue_errors']=sum(abs(float(r['net_revenue'])-(float(r['gross_order_value'])-float(r['discounts'])-float(r['cancelled_value'])-float(r['return_value'])))>0.011 for r in rows)
checks['contribution_errors']=sum(abs(float(r['contribution'])-(float(r['net_revenue'])-float(r['cogs'])-float(r['logistics_cost'])-float(r['payment_fees'])-float(r['marketing_spend'])))>0.011 for r in rows)
checks['logistics_errors']=sum(abs(float(r['logistics_cost'])-float(r['forward_shipping'])-float(r['reverse_shipping']))>0.011 for r in rows)
checks['fy_summary']={}
for fy in ['FY2024-25','FY2025-26','FY2026-27']:
 group=[r for r in rows if r['fy']==fy]
 groupfytd=[r for r in group if int(r['fy_month'])<=7]
 for suffix,rr in [('full_or_available',group),('april_october',groupfytd)]:
  checks['fy_summary'][f'{fy}_{suffix}']={'orders':int(sum(int(r['orders']) for r in rr)),'net_revenue_inr':round(sum(float(r['net_revenue']) for r in rr),2),'contribution_inr':round(sum(float(r['contribution']) for r in rr),2)}
cols=['visits','orders','shipped_orders','cancelled_orders','returned_orders','late_orders','gross_order_value','discounts','cancelled_value','return_value','net_revenue','cogs','forward_shipping','reverse_shipping','logistics_cost','payment_fees','marketing_spend','contribution','weighted_delivery_days']
amounts={k:sum(float(row[k]) for row in rows) for k in cols}
excelamounts={k:sum(float(row[k]) for row in monthly) for k in cols}
checks['excel_vs_detail_total_mismatches']={k:round(excelamounts[k]-amounts[k],6) for k in cols if abs(excelamounts[k]-amounts[k])>.011}
checks['passed']=len(rows)==7440 and len(monthly)==1860 and checks['month_count']==31 and not any([checks['net_revenue_errors'],checks['contribution_errors'],checks['logistics_errors']]) and not checks['excel_vs_detail_total_mismatches']
assert checks['passed'],checks
(R/'data'/'data_quality_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print('data QA PASS',checks['detailed_fact_rows'],'rows',checks['month_count'],'months')
