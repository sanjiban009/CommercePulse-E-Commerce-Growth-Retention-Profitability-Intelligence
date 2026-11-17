from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import io
r=Path(__file__).parent; d=r/'dashboard'; ss=r/'screenshots'
nav=[('01_Executive_Overview','overview'),('02_Growth_and_Conversion','growth'),('03_Customer_and_Retention','customer'),('04_Unit_Economics','economics'),('05_Returns_and_COD_Risk','returns'),('06_Fulfillment_Intelligence','fulfillment'),('07_Forecast_and_Scenarios','forecast')]
html=(d/'index.html').read_text().replace('<link rel="stylesheet" href="styles.css">','').replace('<script src="data.js"></script><script src="app.js"></script>','')
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1600,'height':1100},device_scale_factor=1)
 errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
 page.set_content(html,wait_until='load')
 page.add_style_tag(content=(d/'styles.css').read_text())
 page.add_script_tag(content=(d/'data.js').read_text())
 page.add_script_tag(content=(d/'app.js').read_text())
 page.wait_for_timeout(190)
 for name,target in nav:
  page.locator(f'[data-page="{target}"]').click();page.wait_for_timeout(110)
  assert page.locator('.kpi').count()==6 and page.locator('.chart-panel').count()==4 and page.locator('.insight').count()==3
  pic=page.screenshot(full_page=True,type='png',animations='disabled')
  im=Image.open(io.BytesIO(pic)).convert('RGB')
  github=ss/'GitHub';link=ss/'LinkedIn'
  (github/'PNG'/f'{name}.png').write_bytes(pic)
  im.save(github/'JPEG'/f'{name}.jpg','JPEG',quality=91,optimize=True,subsampling=0)
  # LinkedIn carousel assets: legible portrait-friendly native dashboard at 1350 px width.
  newwidth=1350;newheight=round(im.height*newwidth/im.width)
  lin=im.resize((newwidth,newheight),Image.Resampling.LANCZOS)
  lin.save(link/'PNG'/f'{name}.png',optimize=True)
  lin.save(link/'JPEG'/f'{name}.jpg','JPEG',quality=93,optimize=True,subsampling=0)
  print(name,'captured',im.size,'LinkedIn',lin.size)
 assert not errs,errs
 b.close()
# Cover artwork contains a genuine thumbnail of the dashboard; not a fabricated screenshot.
cover=Image.new('RGB',(1200,675),'#071524');draw=ImageDraw.Draw(cover)
for y in range(675):
 t=y/674
 draw.line((0,y,1200,y),fill=(int(9+4*t),int(22+13*t),int(38+19*t)))
preview=Image.open(ss/'GitHub'/'PNG'/'01_Executive_Overview.png').convert('RGB')
# Cropped preview showing actual KPI and chart panels.
mini=preview.crop((245,215,1510,1005)).resize((592,390),Image.Resampling.LANCZOS)
mini=mini.filter(ImageFilter.UnsharpMask(radius=1.3,percent=125))
cover.paste(mini,(577,141))
draw.rounded_rectangle((558,122,1184,550),radius=15,outline='#3b7e86',width=3)

fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';fontbold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f=lambda sz,bold=False:ImageFont.truetype(fontbold if bold else fontpath,sz)
draw.rounded_rectangle((43,61,93,111),radius=13,fill='#47dbc6')
draw.text((55,67),'◈',fill='#032337',font=f(32,True))
draw.text((110,66),'CommercePulse',fill='#f0fbff',font=f(27,True))
draw.text((44,158),'E-COMMERCE',fill='#54e3c7',font=f(19,True),stroke_width=0)
draw.text((44,200),'GROWTH, RETENTION',fill='#f4faff',font=f(28,True))
draw.text((44,247),'& PROFITABILITY',fill='#f4faff',font=f(28,True))
draw.text((44,310),'INTELLIGENCE',fill='#f4faff',font=f(28,True))
draw.rounded_rectangle((43,389,450,432),radius=8,fill='#153849',outline='#286b6e',width=2)
draw.text((56,400),'07  INTERACTIVE DASHBOARD PAGES',fill='#c4f7e5',font=f(14,True))
draw.text((44,480),'Indian FY / Matched FYTD / Scenarios',fill='#c0d4e3',font=f(14))
draw.text((44,508),'Dynamic executive decision insights',fill='#c0d4e3',font=f(14))
draw.line((43,593,1128,593),fill='#386074',width=1)
draw.text((43,610),'SYNTHETIC PORTFOLIO PROJECT     •     SANJIBAN DAS',fill='#92afc0',font=f(13,True))
for target in ['GitHub','LinkedIn']:
 w=1600 if target=='GitHub' else 1200
 dest=cover.resize((w,round(cover.height*w/1200)),Image.Resampling.LANCZOS)
 dest.save(ss/target/'PNG'/'00_Project_Cover.png',optimize=True)
 dest.save(ss/target/'JPEG'/'00_Project_Cover.jpg','JPEG',quality=92,optimize=True,subsampling=0)
print('complete:',len(list(ss.rglob('*.png'))),'PNGs',len(list(ss.rglob('*.jpg'))),'JPEGs')
