import csv, json, collections
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile
R=Path(__file__).parent
rows=list(csv.DictReader((R/'data'/'commercepulse_excel_monthly_facts.csv').open(encoding='utf-8')))
fields=list(rows[0].keys())
ints={'fy_month','visits','orders','shipped_orders','cancelled_orders','returned_orders','late_orders'}
dims={'month','fy','category','region','channel'}
vals=[]
for r in rows:
 vals.append([int(r[k]) if k in ints else r[k] if k in dims else float(r[k]) for k in fields])
wb=Workbook.create()
readme=wb.worksheets.add('START HERE')
summ=wb.worksheets.add('FY Scorecard')
fact=wb.worksheets.add('Monthly Facts')
dict_s=wb.worksheets.add('Metric Dictionary')
midnight='#0B1B2A'; teal='#096E71'; blue='#123B58'; white='#FFFFFF'; pale='#E8F6F7'; light='#EAF1F6'; gold='#FFF1D9'
# Cover sheet
readme.merge_cells('A2:J3');readme.get_range('A2').values=[['COMMERCEPULSE  |  E-COMMERCE INTELLIGENCE']]
readme.get_range('A2:J3').format={'fill':midnight,'font':{'bold':True,'size':19,'color':'#FFFFFF'},'vertical_alignment':'center','row_height':25}
readme.merge_cells('A5:J5');readme.get_range('A5').values=[['Indian-market synthetic sample | April 2024 – October 2026 | FY = April – March']]
readme.get_range('A5:J5').format={'font':{'color':'#24516B','size':11},'row_height':28}
intro=[['PROJECT','CommercePulse — Growth, Customer Retention & Profitability Intelligence'],['DATA STATUS','100% synthetic, reproducible, no customer or employer actuals'],['SOURCE GRAIN','Monthly × product category × region × acquisition channel; rolled up from 7,440 granular segment/payment rows'],['EXCEL RECORDS',len(rows)],['FINANCIAL CURRENCY','INR, full-precision transaction-model aggregates'],['AVAILABLE FISCAL YEARS','FY2024-25 | FY2025-26 | FY2026-27 (through Oct 2026)'],['FYTD CUTOFF','April through October inclusive; matched across the comparison years'],['DASHBOARD LAUNCH','../dashboard/index.html (open after extracting ZIP)'],['SOURCE DATA','Detailed CSV includes customer_type and payment_type columns'],['IMPORTANT','Repeat-type order share is NOT customer-level retention; modeled visits are synthetic']]
for i,(label,value) in enumerate(intro,8):
 readme.get_range(f'B{i}:C{i}').values=[[label,str(value)]]
 readme.get_range(f'B{i}').format={'font':{'bold':True,'color':'#1E566C'},'fill':'#DDF3F1'}
 readme.get_range(f'C{i}').format.wrap_text=True
readme.get_range('A:A').format.column_width=4;readme.get_range('B:B').format.column_width=29;readme.get_range('C:C').format.column_width=78
readme.get_range('D:J').format.column_width=12
# Fact table, efficient bulk write
fact.get_range('A1:Y1').values=[[k.replace('_',' ').title() for k in fields]]
fact.get_range('A1:Y1').format={'fill':midnight,'font':{'bold':True,'color':white,'size':10},'row_height':32,'vertical_alignment':'center'}
for start in range(0,len(vals),250):
 data=vals[start:start+250]
 fact.get_range_by_indexes(start+1,0,len(data),len(fields)).values=data
fact.freeze_panes.freeze_rows(1)
fact.get_range('A:A').format.column_width=14
fact.get_range('B:B').format.column_width=15
fact.get_range('C:C').format.column_width=12
fact.get_range('D:D').format.column_width=25
fact.get_range('E:E').format.column_width=13
fact.get_range('F:F').format.column_width=21
fact.get_range('G:Y').format.column_width=16
fact.get_range(f'M2:Y{len(vals)+1}').set_number_format('#,##0.00;[Red](#,##0.00)')
fact.get_range(f'G2:L{len(vals)+1}').set_number_format('#,##0')
try:
 fact.tables.add(f'A1:Y{len(vals)+1}',True,'CommercePulseMonthlyFacts')
except Exception as exc: print('table setup warning:',str(exc)[:150])
# Summary aggregates sourced from detailed facts; ratios formulas
original=list(csv.DictReader((R/'data'/'commercepulse_detailed_monthly_facts.csv').open(encoding='utf-8')))
summ.merge_cells('A1:L2');summ.get_range('A1').values=[['COMMERCEPULSE  /  FISCAL PERFORMANCE SCORECARD']]
summ.get_range('A1:L2').format={'fill':midnight,'font':{'bold':True,'size':17,'color':white},'row_height':21}
summ.merge_cells('A3:L3');summ.get_range('A3').values=[['FYTD = Apr–Oct matched window. Full FY2026–27 remains partial because actuals stop in October 2026.']]
summ.get_range('A3:L3').format={'fill':pale,'font':{'color':'#155567','size':10},'row_height':28}
cols=['Fiscal year','Net revenue INR','Placed orders','Contribution INR','Returned orders','Shipped orders','Modeled visits','Marketing INR','Contribution margin','Return rate','Order conversion','Period coverage']
summ.get_range('A5:L5').values=[cols]
summ.get_range('A5:L5').format={'fill':teal,'font':{'color':white,'bold':True},'row_height':34,'wrap_text':True}
for n,(fy,monthlimit,period) in enumerate([('FY2024-25',12,'FULL YEAR'),('FY2025-26',12,'FULL YEAR'),('FY2026-27',12,'AVAILABLE'),('FY2024-25',7,'FYTD Apr-Oct'),('FY2025-26',7,'FYTD Apr-Oct'),('FY2026-27',7,'FYTD Apr-Oct')],6):
 rec=[r for r in original if r['fy']==fy and int(r['fy_month'])<=monthlimit]
 def S(k):return sum(float(r[k]) for r in rec)
 summ.get_range(f'A{n}:H{n}').values=[[fy,round(S('net_revenue'),2),int(S('orders')),round(S('contribution'),2),int(S('returned_orders')),int(S('shipped_orders')),int(S('visits')),round(S('marketing_spend'),2)]]
 summ.get_range(f'I{n}:K{n}').formulas=[[f'=IFERROR(D{n}/B{n},0)',f'=IFERROR(E{n}/F{n},0)',f'=IFERROR(C{n}/G{n},0)']]
 summ.get_range(f'L{n}').values=[[period]]
 if n in [8,11]:summ.get_range(f'A{n}:L{n}').format.fill=gold
 if n in [9,10]:summ.get_range(f'A{n}:L{n}').format.fill=light
summ.get_range('A:A').format.column_width=19
summ.get_range('B:B').format.column_width=24
summ.get_range('C:C').format.column_width=19
summ.get_range('D:D').format.column_width=24
summ.get_range('E:G').format.column_width=19
summ.get_range('H:H').format.column_width=22
summ.get_range('I:K').format.column_width=20
summ.get_range('L:L').format.column_width=21
summ.get_range('B6:B11').set_number_format('₹#,##0;[Red](₹#,##0)')
summ.get_range('D6:D11').set_number_format('₹#,##0;[Red](₹#,##0)')
summ.get_range('H6:H11').set_number_format('₹#,##0;[Red](₹#,##0)')
summ.get_range('I6:K11').set_number_format('0.0%')
summ.get_range('C6:G11').set_number_format('#,##0')
summ.merge_cells('A14:L14');summ.get_range('A14').values=[['ACCOUNTING RECONCILIATION']]
summ.get_range('A14:L14').format={'fill':blue,'font':{'color':white,'bold':True},'row_height':26}
summ.merge_cells('A15:L15');summ.get_range('A15').values=[['Net revenue = Gross order value − discounts − cancelled value − returned value']]
summ.merge_cells('A16:L16');summ.get_range('A16').values=[['Contribution = net revenue − COGS − (forward + reverse freight) − payment fees − marketing spend']]
summ.merge_cells('A17:L17');summ.get_range('A17').values=[['These are modeled contribution measures: not audited EBITDA, not free cash flow, and not statutory P&L.']]
for rr in [15,16,17]:summ.get_range(f'A{rr}:L{rr}').format={'font':{'color':'#275C71','size':11},'row_height':25}
try:
 chart=summ.charts.add('bar',{'title':'FY comparison · realized revenue','has_legend':False})
 series=chart.series.add('Net revenue')
 series.category_formula="'FY Scorecard'!$A$9:$A$11"
 series.formula="'FY Scorecard'!$B$9:$B$11"
 chart.bar_options.direction='column';chart.set_position('A20','H36')
except Exception as exc:print('chart warning:',str(exc)[:190])
# Definitions
explain={
 'month':'Calendar month, YYYY-MM','fy':'Indian fiscal year, Apr–Mar','fy_month':'Ordinal month of Indian FY; Apr=1 and Mar=12',
 'category':'Synthetic product department','region':'India modeled broad sales region','channel':'Order source/channel group',
 'visits':'Modeled visits/sessions attributed to order-source grouping, not measured users','orders':'Placed orders; includes canceled and later-returned orders','shipped_orders':'Orders after preshipment cancellation','cancelled_orders':'Canceled before fulfillment','returned_orders':'Returned after fulfillment, not RTO separately','late_orders':'Modeled shipped orders not delivered on time','gross_order_value':'Gross placed order value before promotional discounts','discounts':'Promotional markdown value on placed orders','cancelled_value':'Discounted order value canceled before fulfillment','return_value':'Discounted net value refunded after return','net_revenue':'Gross order value - discounts - canceled value - return value','cogs':'Cost of fulfilled and retained goods','forward_shipping':'Forward freight on shipped orders','reverse_shipping':'Returns shipping/handling costs','logistics_cost':'Forward shipping + reverse shipping','payment_fees':'Modeled prepaid gateway and COD processing fees','marketing_spend':'Allocated marketing spend; not true customer acquisition cost','contribution':'Net revenue - COGS - logistics cost - payment fees - marketing spend','weighted_delivery_days':'Sum of shipped orders × modeled transit days; divide by shipped orders'}
dict_s.get_range('A1:B1').values=[['DATA FIELD','BUSINESS DEFINITION']]
dict_s.get_range('A1:B1').format={'fill':midnight,'font':{'color':white,'bold':True},'row_height':30}
dict_s.get_range(f'A2:B{len(fields)+1}').values=[[k,explain[k]] for k in fields]
dict_s.get_range('A:A').format.column_width=28;dict_s.get_range('B:B').format.column_width=94
dict_s.get_range(f'A2:B{len(fields)+1}').format.row_height=21
dict_s.freeze_panes.freeze_rows(1)
path=R/'data'/'CommercePulse_Synthetic_Ecommerce_Data.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(path))
print('EXPORTED',path,path.stat().st_size)
try:
 print('INSPECT',wb.inspect({'kind':'table','range':'FY Scorecard!A5:L9','include':'values,formulas','table_max_rows':7,'table_max_cols':12}).ndjson[:2500])
except Exception as e:print('inspect non-critical',str(e)[:150])
