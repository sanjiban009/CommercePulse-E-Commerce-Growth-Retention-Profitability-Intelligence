import csv, json, math, random, calendar
from collections import defaultdict
from pathlib import Path
R=Path(__file__).parent
random.seed(902617)
CATEGORIES=['Electronics','Fashion','Beauty & Personal Care','Home & Kitchen','Grocery']
REGIONS=['North','South','East','West']
CHANNELS=['Marketplace','Paid Media','Direct & Organic']
SEGMENTS=['New','Returning']
PAYMENTS=['Prepaid','COD']
base_orders={'Electronics':1780,'Fashion':2880,'Beauty & Personal Care':1450,'Home & Kitchen':1320,'Grocery':2500}
avgs={'Electronics':4550,'Fashion':1780,'Beauty & Personal Care':1080,'Home & Kitchen':2670,'Grocery':910}
cogs={'Electronics':.735,'Fashion':.555,'Beauty & Personal Care':.465,'Home & Kitchen':.655,'Grocery':.785}
returns={'Electronics':.077,'Fashion':.172,'Beauty & Personal Care':.057,'Home & Kitchen':.092,'Grocery':.032}
regionw={'North':.30,'South':.275,'East':.185,'West':.24}
channelw={'Marketplace':.44,'Paid Media':.325,'Direct & Organic':.235}
conv={'Marketplace':.032,'Paid Media':.0185,'Direct & Organic':.042}
shipping={'Electronics':164,'Fashion':71,'Beauty & Personal Care':56,'Home & Kitchen':112,'Grocery':45}
adcost={'Marketplace':58,'Paid Media':170,'Direct & Organic':36}
fy_names=['FY2024-25','FY2025-26','FY2026-27']
months=[]
for year in [2024,2025,2026]:
  for month in range(1,13):
    if (year,month)<(2024,4) or (year,month)>(2026,10): continue
    months.append((year,month))
rows=[]
for year,month in months:
  fy=f'FY{year if month>=4 else year-1}-{str((year+1 if month>=4 else year))[-2:]}'
  fiscal_month=((month-4)%12)+1
  year_scale={2024:1.0,2025:1.15,2026:1.30}[year]
  season={1:1.03,2:.98,3:1.04,4:1.0,5:1.03,6:.98,7:1.02,8:1.11,9:1.07,10:1.35,11:1.47,12:1.16}[month]
  for cat in CATEGORIES:
    for reg in REGIONS:
      for ch in CHANNELS:
        for seg in SEGMENTS:
          segw= (.68 if ch=='Paid Media' else .55 if ch=='Marketplace' else .36) if seg=='New' else (.32 if ch=='Paid Media' else .45 if ch=='Marketplace' else .64)
          for pay in PAYMENTS:
            payw= (.64 if reg!='East' else .53) if pay=='Prepaid' else (.36 if reg!='East' else .47)
            lam=base_orders[cat]*regionw[reg]*channelw[ch]*segw*payw*year_scale*season
            order_count=max(0,round(lam*random.uniform(.91,1.09)))
            if not order_count:continue
            price=avgs[cat]*random.uniform(.92,1.095)*(1+ .025*(year-2024))
            gross=round(order_count*price,2)
            discount_pct=(.067 if ch=='Marketplace' else .085 if ch=='Paid Media' else .045)+(.032 if month in [10,11] else 0)+random.uniform(-.012,.014)
            discount=round(gross*discount_pct,2)
            post_discount=gross-discount
            cancel_rate=(.038 if pay=='Prepaid' else .082)+(.012 if ch=='Marketplace' else 0)+random.uniform(-.012,.012)
            cancelled=min(order_count,round(order_count*cancel_rate))
            cancel_val=round(post_discount*cancelled/order_count,2)
            shipped=order_count-cancelled
            ret_rate=returns[cat]*(1.40 if pay=='COD' else .74)*(1.10 if ch=='Marketplace' else 1.0)
            ret_rate*=random.uniform(.84,1.16)
            returned=min(shipped,round(shipped*ret_rate))
            return_val=round((post_discount-cancel_val)*returned/shipped,2) if shipped else 0
            realized=round(post_discount-cancel_val-return_val,2)
            cogs_cost=round(realized*cogs[cat]*random.uniform(.975,1.025),2)
            reverse=round(returned*(shipping[cat]*.73+random.uniform(7,22)),2)
            fwd=round(shipped*shipping[cat]*(1.13 if reg=='East' else 1.06 if reg=='North' else 1.0)*random.uniform(.95,1.05),2)
            logistics=round(fwd+reverse,2)
            gateway=round(realized*(.019 if pay=='Prepaid' else .012),2)
            mkt=round(order_count*adcost[ch]*(1.0 if seg=='New' else .41)*random.uniform(.90,1.10),2)
            contribution=round(realized-cogs_cost-logistics-gateway-mkt,2)
            conv_rate=conv[ch]*(1.26 if seg=='Returning' else .86)*random.uniform(.94,1.06)
            visits=max(order_count,round(order_count/conv_rate))
            day_factor={'North':3.25,'South':2.65,'East':4.2,'West':2.9}[reg]+(.35 if pay=='COD' else 0)
            avg_days=round(day_factor*random.uniform(.91,1.08),3)
            late_rate={'North':.125,'South':.085,'East':.185,'West':.10}[reg]+(.04 if pay=='COD' else 0)
            late=min(shipped,round(shipped*late_rate*random.uniform(.80,1.14)))
            rec={'month':f'{year}-{month:02d}','fy':fy,'fy_month':fiscal_month,'category':cat,'region':reg,'channel':ch,'customer_type':seg,'payment_type':pay,
                 'visits':visits,'orders':order_count,'shipped_orders':shipped,'cancelled_orders':cancelled,'returned_orders':returned,'late_orders':late,
                 'gross_order_value':gross,'discounts':discount,'cancelled_value':cancel_val,'return_value':return_val,'net_revenue':realized,'cogs':cogs_cost,
                 'forward_shipping':fwd,'reverse_shipping':reverse,'logistics_cost':logistics,'payment_fees':gateway,'marketing_spend':mkt,'contribution':contribution,
                 'weighted_delivery_days':round(shipped*avg_days,3)}
            assert abs((gross-discount-cancel_val-return_val)-realized) < .011
            assert abs(realized-cogs_cost-logistics-gateway-mkt-contribution)<.011
            rows.append(rec)
assert len(rows)>6500
fields=list(rows[0].keys())
with (R/'data'/'commercepulse_detailed_monthly_facts.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
with (R/'dashboard'/'data.js').open('w',encoding='utf-8') as f:
 f.write('/* Synthetic ecommerce portfolio data; FY2026-27 through October 2026. */\nwindow.COMMERCEPULSE_DATA=')
 json.dump([[r[k] for k in fields] for r in rows],f,separators=(',',':'))
 f.write(';\nwindow.COMMERCEPULSE_FIELDS='+json.dumps(fields,separators=(',',':'))+';\n')
agg={}
for r in rows:
 k=(r['month'],r['fy'],r['fy_month'],r['category'],r['region'],r['channel'])
 if k not in agg:
  agg[k]={'month':k[0],'fy':k[1],'fy_month':k[2],'category':k[3],'region':k[4],'channel':k[5]}
  for x in fields[8:]:agg[k][x]=0
 for x in fields[8:]:agg[k][x]+=r[x]
summary=list(agg.values())
with (R/'data'/'commercepulse_excel_monthly_facts.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(summary[0].keys()));w.writeheader();w.writerows(summary)
meta={'rows_detail':len(rows),'rows_excel':len(summary),'months':len(months),'from':'2024-04','through':'2026-10','categories':CATEGORIES,'regions':REGIONS,'channels':CHANNELS,'segment':SEGMENTS,'payment':PAYMENTS}
(R/'data'/'dataset_manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print(meta)
for fy in fy_names:
 selected=[r for r in rows if r['fy']==fy]
 print(fy,'orders',sum(r['orders'] for r in selected),'net_revenue',round(sum(r['net_revenue'] for r in selected)), 'contribution',round(sum(r['contribution'] for r in selected)))
