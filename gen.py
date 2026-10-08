import math, html
BG='#0a1a2f'; GRID='#12304f'; GRID2='#1b4470'; LINE='#7fd3ff'; DIM='#4f7ea8'; INK='#e8f4ff'; ACC='#ff8a3d'
FONT="font-family:ui-monospace,'JetBrains Mono',SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"
def head(w,h,extra=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><pattern id="s" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M10 0H0V10" fill="none" stroke="{GRID}" stroke-width=".6"/></pattern>
<pattern id="l" width="50" height="50" patternUnits="userSpaceOnUse"><rect width="50" height="50" fill="url(#s)"/><path d="M50 0H0V50" fill="none" stroke="{GRID2}" stroke-width=".8"/></pattern>{extra}</defs>
<style>text{{{FONT};fill:{INK}}} .d{{fill:{DIM}}} .a{{fill:{ACC}}} .c{{fill:{LINE}}}</style>
<rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w}" height="{h}" fill="url(#l)"/>'''
def t(x,y,s,size=11,cls='',anchor='start',ls=0,weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}" text-anchor="{anchor}" letter-spacing="{ls}" font-weight="{weight}">{html.escape(s)}</text>'
def frame(w,h,zones=True):
    o=[f'<rect x="8" y="8" width="{w-16}" height="{h-16}" fill="none" stroke="{LINE}" stroke-width="1.4"/>',
       f'<rect x="20" y="20" width="{w-40}" height="{h-40}" fill="none" stroke="{LINE}" stroke-width=".6" opacity=".7"/>']
    if zones:
        n=8
        for i in range(1,n):
            x=8+(w-16)*i/n; o.append(f'<path d="M{x} 8V20M{x} {h-20}V{h-8}" stroke="{LINE}" stroke-width=".6"/>')
        for i in range(n):
            x=8+(w-16)*(i+.5)/n; o.append(t(x,17.5,str(i+1),8,'d','middle')); o.append(t(x,h-10.5,str(i+1),8,'d','middle'))
        for i,L in enumerate('ABCD'):
            y=8+(h-16)*(i+.5)/4; o.append(t(14,y+3,L,8,'d','middle')); o.append(t(w-14,y+3,L,8,'d','middle'))
            if i: yy=8+(h-16)*i/4; o.append(f'<path d="M8 {yy}H20M{w-20} {yy}H{w-8}" stroke="{LINE}" stroke-width=".6"/>')
    return o

# ---------- HERO ----------
W,H=1000,460
o=[head(W,H)]+frame(W,H)
# title
o+= [t(52,78,'FIG. 01 — GENOME OF A BUILDER',10,'d',ls=2),
     t(50,128,'VENKATA',44,'',ls=10,weight=300), t(50,178,'MANOJ',44,'c',ls=10,weight=700),
     f'<path d="M52 196H360" stroke="{LINE}" stroke-width=".8"/>',
     t(52,216,'AI & DATA SCIENCE  ·  SIMATS ENGINEERING',10,'d',ls=1.2),
     t(52,234,'CLASS OF 2028  ·  CHENNAI  13.08°N 80.27°E',10,'d',ls=1.2)]
# dimension line under name
o+= [f'<path d="M52 250V262M360 250V262M52 256H360" stroke="{DIM}" stroke-width=".7"/>',
     f'<path d="M52 256l7 -3v6zM360 256l-7 -3v6z" fill="{DIM}"/>',
     f'<rect x="168" y="249" width="76" height="14" fill="{BG}"/>', t(206,259.5,'1 HUMAN',9,'d','middle',1)]
# helix
cx0,cx1,cy,amp=480,945,190,62
N=34; per=4.0; turns=2.2
for i in range(N):
    x=cx0+(cx1-cx0)*i/(N-1); ph=i/(N-1)*turns
    def vals(off):
        return ';'.join(f'{cy+amp*math.sin(2*math.pi*(k/24+ph)+off):.1f}' for k in range(25))
    y1=cy+amp*math.sin(2*math.pi*ph); y2=cy+amp*math.sin(2*math.pi*ph+math.pi)
    col=ACC if i in (9,10,23,24) else LINE
    o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y1:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="1.1" opacity=".55">'
             f'<animate attributeName="y1" values="{vals(0)}" dur="{per}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y2" values="{vals(math.pi)}" dur="{per}s" repeatCount="indefinite"/></line>')
    for off,r in ((0,3.2),(math.pi,3.2)):
        yy=cy+amp*math.sin(2*math.pi*ph+off)
        rv=';'.join(f'{2.2+1.6*(1+math.cos(2*math.pi*(k/24+ph)+off))/2:.2f}' for k in range(25))
        o.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="{r}" fill="{col}"><animate attributeName="cy" values="{vals(off)}" dur="{per}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="r" values="{rv}" dur="{per}s" repeatCount="indefinite"/></circle>')
# callouts
calls=[(cx0+ (cx1-cx0)*2/33, 'PYTHON', 'backbone', -1),
       (cx0+ (cx1-cx0)*9.5/33, 'LLM SYSTEMS', 'dominant allele', 1),
       (cx0+ (cx1-cx0)*15/33, 'TYPESCRIPT', 'product layer', -1),
       (cx0+ (cx1-cx0)*23.5/33, 'CURIOSITY', 'mutation rate: high', 1),
       (cx0+ (cx1-cx0)*31/33, 'RL · AGENTS', 'expressing now', -2)]
for x,a,b,s in calls:
    left = s==-2; s = -1 if left else s
    ye = cy - s*(amp+14); yl = cy - s*(amp+44); dx = -14 if left else 14; tx = x-18 if left else x+18; an='end' if left else 'start'
    o.append(f'<path d="M{x:.1f} {ye}V{yl}H{x+dx:.1f}" fill="none" stroke="{DIM}" stroke-width=".7"/><circle cx="{x:.1f}" cy="{ye}" r="1.8" fill="{DIM}"/>')
    o.append(t(tx,yl+4,a,10,'c',an,1.5,600))
    o.append(t(tx,yl+16,b,9,'d',an,.5))
# title block
bx,by,bw,bh=560,340,410,98
o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{BG}" stroke="{LINE}" stroke-width="1"/>')
for yy in (by+24,by+48,by+72): o.append(f'<path d="M{bx} {yy}H{bx+bw}" stroke="{LINE}" stroke-width=".5"/>')
o.append(f'<path d="M{bx+205} {by}V{by+bh}" stroke="{LINE}" stroke-width=".5"/>')
cells=[('DRAWN BY','B. V. MANOJ'),('REV','2.0 · 2026-10'),('DISCIPLINE','AI ENGINEERING'),('SCALE','1:1, SHIPS WEEKLY'),
       ('STATUS','SEEKING INTERNSHIP'),('SHEET','1 OF 1'),('APPROVED BY','__________ (you?)'),('DWG NO.','VM-2028-AI')]
for k,(lab,val) in enumerate(cells):
    col=k%2; row=k//2; x=bx+8+col*205; y=by+10+row*24
    o.append(t(x,y,lab,7,'d',ls=1)); o.append(t(x,y+11,val,10,'a' if lab=='STATUS' else '',ls=.8,weight=600 if lab=='STATUS' else 400))
o.append('</svg>'); open('assets/hero.svg','w').write('\n'.join(o))

# ---------- ELEMENTS ----------
els=[(1,'Nw','News Bot','121','AGENTIC',  '6 sources → 6 LLMs → Telegram'),
     (2,'Vr','VideoReverse','CLI','GENERATIVE','video → prompts for 8 models'),
     (3,'Tx','Transcribo','CI','AUDIO',   'speech → Telugu study notes'),
     (4,'Ro','Resilience-Ops','RL','REINFORCEMENT','agents vs. IT outages')]
for n,sym,name,mass,grp,desc in els:
    w,h=230,250; o=[head(w,h)]
    o.append(f'<rect x="10" y="10" width="{w-20}" height="{h-20}" fill="{BG}" fill-opacity=".85" stroke="{LINE}" stroke-width="1.2"/>')
    o.append(t(22,32,f'{n:03d}',12,'c',weight=600)); o.append(t(w-22,32,mass,11,'a','end',weight=600))
    # orbits
    ox,oy=w/2,108
    for k,(rx,ry,rot,dur) in enumerate([(70,22,-25,6),(70,22,25,8),(46,46,0,10)]):
        o.append(f'<g transform="rotate({rot} {ox} {oy})"><ellipse cx="{ox}" cy="{oy}" rx="{rx}" ry="{ry}" fill="none" stroke="{DIM}" stroke-width=".6" stroke-dasharray="2 3"/>'
                 f'<circle r="2.6" fill="{ACC if k==0 else LINE}"><animateMotion dur="{dur}s" repeatCount="indefinite" path="M{ox+rx} {oy} A{rx} {ry} 0 1 1 {ox-rx} {oy} A{rx} {ry} 0 1 1 {ox+rx} {oy}"/></circle></g>')
    o.append(t(ox,oy+18,sym,50,'',anchor='middle',weight=700))
    o.append(t(w/2,176,name.upper(),12,'c','middle',1.5,600))
    o.append(f'<path d="M30 188H{w-30}" stroke="{DIM}" stroke-width=".5"/>')
    o.append(t(w/2,204,desc,9,'d','middle'))
    o.append(t(w/2,226,grp,8,'a','middle',2))
    o.append('</svg>'); open(f'assets/el-{sym.lower()}.svg','w').write('\n'.join(o))

# ---------- SPECTRUM ----------
W,H=1000,170
spec=[('Python',.05),('PyTorch',.13),('FastAPI',.2),('LLMs',.28),('RAG · FAISS',.36),('Ollama · Groq',.44),('RL',.52),
      ('TypeScript',.6),('React',.67),('Next.js',.74),('Node',.8),('SQLite',.86),('Docker',.92),('Actions',.97)]
o=[head(W,H,'<linearGradient id="sp" x1="0" x2="1"><stop offset="0" stop-color="#6a3dff"/><stop offset=".2" stop-color="#2f7bff"/><stop offset=".4" stop-color="#21d4c2"/><stop offset=".55" stop-color="#7cff6b"/><stop offset=".72" stop-color="#ffe14d"/><stop offset=".86" stop-color="#ff8a3d"/><stop offset="1" stop-color="#ff3d5a"/></linearGradient>')]
o+=frame(W,H,False)
o.append(t(40,46,'FIG. 03 — EMISSION SPECTRUM OF THE STACK',10,'d',ls=2)); o.append(t(W-40,46,'λ  →  frequency of use',9,'d','end',1))
x0,x1,y0,y1=40,W-40,62,104
o.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#050d18" stroke="{DIM}" stroke-width=".6"/>')
o.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="url(#sp)" opacity=".10"/>')
import colorsys
for i,(lab,p) in enumerate(spec):
    x=x0+(x1-x0)*p
    # colour from gradient approx via hue
    hue=(0.72-0.72*p)%1; r,g,b=colorsys.hsv_to_rgb(hue,.75,1); c='#%02x%02x%02x'%(int(r*255),int(g*255),int(b*255))
    wdt=3.2 if lab in ('Python','LLMs','TypeScript') else 1.8
    o.append(f'<rect x="{x-wdt/2:.1f}" y="{y0}" width="{wdt}" height="{y1-y0}" fill="{c}"><animate attributeName="opacity" values="1;.55;1" dur="{2.5+(i%5)*.6:.1f}s" repeatCount="indefinite"/></rect>')
    yy=122 if i%2==0 else 140
    o.append(f'<path d="M{x:.1f} {y1}V{yy-10}" stroke="{DIM}" stroke-width=".5"/>')
    o.append(t(x,yy,lab,9,'',anchor='middle',ls=.5))
o.append('</svg>'); open('assets/spectrum.svg','w').write('\n'.join(o))

# ---------- ECG ----------
W,H=1000,170
o=[head(W,H)]+frame(W,H,False)
beat=[(0,0),(30,0),(38,-6),(46,0),(56,0),(60,8),(66,-40),(72,16),(78,0),(96,0),(108,-12),(122,0),(160,0)]
pts=[];x=40
while x<W-60:
    for dx,dy in beat: pts.append((x+dx,104+dy))
    x+=160
d='M'+' L'.join(f'{a:.0f} {b:.0f}' for a,b in pts if a<W-40)
o.append(t(40,44,'FIG. 04 — VITALS',10,'d',ls=2))
o.append(t(W-40,44,'HR 72  ·  STATUS: SHIPPING  ·  OPEN TO AI/ML INTERNSHIPS',10,'a','end',1.2,600))
o.append(f'<path d="{d}" fill="none" stroke="{DIM}" stroke-width="1" opacity=".35"/>')
o.append(f'<path d="{d}" fill="none" stroke="{ACC}" stroke-width="1.8" stroke-linejoin="round" stroke-dasharray="140 1400" stroke-dashoffset="1540"><animate attributeName="stroke-dashoffset" from="1540" to="0" dur="3.2s" repeatCount="indefinite"/></path>')
o.append(t(40,142,'build fast · learn faster · ship',9,'d',ls=1.5))
o.append('</svg>'); open('assets/ecg.svg','w').write('\n'.join(o))
