"""Strijder CB-01 rev B: deterministic vector circuit drawings, not a PCB tool.

Run from any directory. Requires reportlab and PyMuPDF (fitz).
Outputs PDF, SVG, BOM CSV and pin/net CSV beside this file.
All circuitry is NEW PROPOSED DESIGN, not recovered owner-approved wiring.
"""
from pathlib import Path
import csv
import json
import math
from collections import defaultdict
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)
W, H = 1190, 842
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('CircuitSans', str(FONT_DIR/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('CircuitSansBold', str(FONT_DIR/'DejaVuSans-Bold.ttf')))
c = canvas.Canvas(str(OUT / 'strijder-circuit-base-rev-b.pdf'), pagesize=(W, H))
c.setTitle('Strijder CB-01 - preliminary electrical circuits - Rev B')
c.setAuthor('Strijder engineering reconstruction')
parts = {}
page = 0

def text(x, y, s, size=10, bold=False):
    c.setFillColorRGB(0, 0, 0)
    c.setFont('CircuitSansBold' if bold else 'CircuitSans', size)
    c.drawString(x, H-y, s)

def line(*pts):
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], H-a[1], b[0], H-b[1])

def box(x, y, w, h):
    c.setStrokeColorRGB(0, 0, 0)
    c.rect(x, H-y-h, w, h)

def dot(x, y):
    c.setFillColorRGB(0, 0, 0)
    c.circle(x, H-y, 2.5, fill=1, stroke=0)

def polygon(pts, fill=False):
    p = c.beginPath(); p.moveTo(pts[0][0], H-pts[0][1])
    for x, y in pts[1:]: p.lineTo(x, H-y)
    p.close(); c.drawPath(p, fill=int(fill), stroke=1)

def arrow(a, b):
    line(a,b)
    dx,dy=b[0]-a[0],b[1]-a[1]; m=math.hypot(dx,dy); ux,uy=dx/m,dy/m
    polygon([b,(b[0]-8*ux+3*uy,b[1]-8*uy-3*ux),(b[0]-8*ux-3*uy,b[1]-8*uy+3*ux)],True)

def label(x, y, net):
    text(x+4,y-6,net,10,True)

def ground(x, y, net='GND'):
    line((x,y),(x,y+10)); line((x-12,y+10),(x+12,y+10))
    line((x-8,y+15),(x+8,y+15)); line((x-4,y+20),(x+4,y+20))
    text(x+17,y+18,net,9)

def part(ref, value, mpn, pins, package='', note=''):
    assert ref not in parts, ref
    parts[ref] = dict(ref=ref, value=value, mpn=mpn, package=package,
                      sheet=page, note=note, pins={str(k):v for k,v in pins.items()})

def two(ref,value,mpn,x,y,n1,n2,kind='R',vertical=False,reverse=False,package='',note=''):
    # Electrical pin convention: R/C/F 1=start,2=end; diodes A/K explicitly named.
    def p(a,b=0): return (x+b,y+a) if vertical else (x+a,y+b)
    if kind in ('D','Z'):
        part(ref,value,mpn,{'K' if reverse else 'A':n1,'A' if reverse else 'K':n2},package,note)
        sign=-1 if reverse else 1
        line(p(0),p(28)); line(p(52),p(80))
        polygon([p(40-12*sign,-10),p(40-12*sign,10),p(40+12*sign,0)])
        k=40+12*sign; line(p(k,-12),p(k,12))
        if kind=='Z':
            line(p(k,-12),p(k+5*sign,-15));line(p(k,12),p(k-5*sign,15))
        for a,s in [(14,'K' if reverse else 'A'),(65,'A' if reverse else 'K')]:
            q=p(a,15);text(*q,s,8)
    else:
        part(ref,value,mpn,{'1':n1,'2':n2},package,note)
        if kind=='C':
            line(p(0),p(35));line(p(45),p(80))
            line(p(35,-13),p(35,13));line(p(45,-13),p(45,13))
        else:
            line(p(0),p(20));line(p(60),p(80))
            polygon([p(20,-7),p(60,-7),p(60,7),p(20,7)])
            if kind=='F':line(p(20),p(60))
    if vertical:
        text(x+20,y+30,ref,10,True);text(x+20,y+45,value,9)
    else:
        text(x+18,y-27,ref,10,True);text(x+5,y-13,value,9)
    return p(0),p(80)

def r(ref,val,x,y,a,b,v=False,power='0.25 W'):
    return two(ref,val,'VALUE-SPEC',x,y,a,b,vertical=v,package='axial, 1%',note=power)
def cap(ref,val,x,y,a,b):
    return two(ref,val,'VALUE-SPEC',x,y,a,b,kind='C',vertical=True,package='radial/ceramic',note='Voltage and dielectric per displayed value')
def diode(ref,val,mpn,x,y,a,b,v=False,rev=False,z=False,package='DO-41'):
    return two(ref,val,mpn,x,y,a,b,'Z' if z else 'D',v,rev,package)
def fuse(ref,val,x,y,a,b):
    return two(ref,val,'VALUE-SPEC',x,y,a,b,kind='F',package='inline holder',note='DC-rated fast fuse; exact clearing curve and holder TBD')
def conn(ref,x,y,nets,desc):
    # Right-facing logical connector; actual housing/cavity orientation NOT released.
    part(ref,desc,'MECHANICAL-TBD',{i+1:n for i,n in enumerate(nets)},'bench terminal/header', 'Logical pin numbers only; no vehicle connector reuse')
    text(x,y-17,ref+'  '+desc,11,True)
    box(x,y-6,42,len(nets)*25)
    for i,n in enumerate(nets):
        yy=y+7+i*25
        text(x+6,yy+3,str(i+1),9);line((x+25,yy),(x+60,yy));label(x+62,yy,n)

def sheet(title,subtitle):
    global page
    if page: c.showPage()
    page+=1; box(24,24,W-48,H-48)
    text(42,51,'STRIJDER VISION / CB-01',16,True)
    text(42,78,title,18,True);text(42,100,subtitle,10)
    line((24,118),(W-24,118));line((24,758),(W-24,758))
    text(42,780,'REV B  |  PROPOSED BENCH CIRCUIT BASE  |  2026-09-09',11,True)
    text(42,801,'Not vehicle-qualified. No PCB/ERC release. Dots join wires; matching net labels connect across sheets.',10)
    text(1020,789,f'SHEET {page} OF 5',11,True)

def notes(lines,y=610):
    for i,s in enumerate(lines):text(55,y+19*i,s,11)

# 01 -- Actual diode-OR connectivity with explicitly named source returns.
sheet('01  Dual-source low-power entry','12-16 V DC laboratory supplies only; 1 A combined board-input ceiling. Optional backup source is externally managed.')
conn('J101',60,173,['VIN_A','GND'],'MAIN DC INPUT')
conn('J102',60,363,['VIN_B','GND'],'OPTIONAL BACKUP')
fuse('F101','1 A / >=32 VDC',330,180,'VIN_A','A_FUSED')
diode('D101','STPS5L60','STPS5L60',480,180,'A_FUSED','VSYS',package='DO-201AD')
line((285,180),(330,180));label(285,180,'VIN_A');line((410,180),(480,180))
fuse('F102','1 A / >=32 VDC',330,370,'VIN_B','B_FUSED')
diode('D102','STPS5L60','STPS5L60',480,370,'B_FUSED','VSYS',package='DO-201AD')
line((285,370),(330,370));label(285,370,'VIN_B');line((410,370),(480,370))
line((560,180),(1030,180));line((560,370),(650,370),(650,180));dot(650,180);label(975,180,'VSYS')
diode('D103','SMBJ18A','SMBJ18A',760,250,'VSYS','GND',v=True,rev=True,z=True,package='SMB')
line((760,180),(760,250));dot(760,180);ground(760,330)
cap('C101','100 uF / 50 V',935,250,'VSYS','GND');text(915,278,'+',12)
line((935,180),(935,250));dot(935,180);ground(935,330)
part('TP101','VSYS test','TESTPOINT',{'1':'VSYS'},'test pad');c.circle(1030,H-180,4);text(1000,158,'TP101',10)
part('TP102','Return test','TESTPOINT',{'1':'GND'},'test pad');label(935,450,'GND');ground(935,450);text(935,420,'TP102',10)
notes(['F101/F102 must be source-adjacent inline fuses; they protect wiring before this board.',
       'Diode cathodes (banded ends) join VSYS. This is higher-voltage-wins OR-ing, NOT main-source priority.',
       'Common GND is intentional. No galvanic power isolation, battery charger, BMS or undervoltage cutoff is provided.',
       'D103 is a small transient clamp, not an automotive load-dump solution or sustained-overvoltage disconnect.',
       'Do not connect directly to a vehicle or an unprotected battery. Do not parallel independent grounded supplies blindly.',
       'Reference parts: ST STPS5L60; Littelfuse SMBJ18A. VSYS is unregulated and lower than the winning input.'],590)

# 02 -- Deliberately simple linear rails with explicit heat requirement.
sheet('02  Low-power 5 V and 3.3 V rails','Bench control board only. Combined 5 V regulator load <=200 mA, including all downstream 3.3 V current.')
part('U201','5 V linear regulator','LM7805CT/NOPB',{'1':'VSYS','2':'GND','3':'+5V'},'TO-220', 'Heatsink required; tab=GND')
box(390,185,190,100);text(410,220,'U201  LM7805CT',12,True)
text(402,247,'1 IN',10);text(526,247,'OUT 3',10);text(459,276,'2 GND',10)
line((100,240),(390,240));label(100,240,'VSYS');line((580,240),(1010,240));label(990,240,'+5V')
line((485,285),(485,360));ground(485,360)
cap('C201','330 nF / 50 V X7R',245,285,'VSYS','GND');line((245,240),(245,285));dot(245,240);ground(245,365)
cap('C202','100 nF / 16 V X7R',735,285,'+5V','GND');line((735,240),(735,285));dot(735,240);ground(735,365)
cap('C203','10 uF / 16 V',970,285,'+5V','GND');line((970,240),(970,285));dot(970,240);ground(970,365)
diode('D201','1N5819','1N5819',440,165,'VSYS','+5V',rev=True)
line((440,165),(340,165),(340,240));dot(340,240);line((520,165),(630,165),(630,240));dot(630,240)
part('U202','3.3 V LDO','MCP1700-3302E/TO',{'1':'GND','2':'+5V','3':'+3V3'},'TO-92','Do not swap TO-92 pins with SOT-23 variant')
box(390,455,190,100);text(400,490,'U202  MCP1700-3302',11,True)
text(402,517,'2 IN',10);text(526,517,'OUT 3',10);text(459,546,'1 GND',10)
line((100,510),(390,510));label(100,510,'+5V');line((580,510),(1010,510));label(990,510,'+3V3')
line((485,555),(485,600));ground(485,600)
cap('C204','1 uF / 10 V X7R',245,530,'+5V','GND');line((245,510),(245,530));dot(245,510);ground(245,610)
cap('C205','1 uF / 10 V X7R',745,530,'+3V3','GND');line((745,510),(745,530));dot(745,510);ground(745,610)
notes(['3.3 V total budget: 50 mA. External MCU must be self-powered and use a common GND; do not tie its supply to these rails.',
       'U201: fit heatsink <=15 K/W sink-to-air; allow <=6 K/W junction/interface. Verify case temperature at 16 V input.',
       'Conservative U201 heat at VSYS=16 V, Iout=0.20 A: 2.20 W plus ground-current loss. Not a compute power supply.',
       'D201: anode on +5V, cathode on VSYS. Capacitors close to pins. No external power injection on +5V or +3V3.'],665)

# 03 -- High-side P-channel MOSFET, not a vague switch rectangle.
sheet('03  Switched peripheral DC output','One 0.5 A resistive/low-capacitance bench channel. No PWM, inductive loads, lightbars or vehicle actuator connection.')
fuse('F301','0.75 A / >=32 VDC',140,185,'VSYS','BR_SOURCE');label(70,185,'VSYS');line((70,185),(140,185))
line((220,185),(700,185));label(430,185,'BR_SOURCE');line((700,185),(700,235))
part('Q301','P-channel high-side switch','IRF4905PbF',{'1':'BR_GATE','2':'BR_OUT','3':'BR_SOURCE'},'TO-220','Tab=drain; single FET does not reverse-block external output power')
# PMOS: gate left, source top, drain bottom; body diode D->S explicitly shown.
line((700,235),(670,235),(670,252));line((670,270),(670,285));line((670,303),(670,320),(700,320),(700,355))
line((650,235),(650,320));line((590,275),(650,275));line((670,278),(700,278),(700,235))
arrow((675,278),(695,278))
text(590,262,'1 G',10);text(705,236,'3 S',10);text(705,340,'2 D',10)
text(805,257,'Q301  IRF4905PbF',12,True);text(805,277,'P-MOS / tab = drain',10)
# Internal body diode, cathode at source. It is not a separate BOM device.
line((700,235),(760,235),(760,250));line((760,310),(760,320),(700,320))
polygon([(750,293),(770,293),(760,268)]);line((746,266),(774,266));line((760,250),(760,266));line((760,293),(760,310))
text(800,300,'Body diode: A=D, K=S',10)
r('R301','100 k',360,195,'BR_SOURCE','BR_GATE',True)
line((360,185),(360,195));dot(360,185);line((360,275),(590,275));label(390,275,'BR_GATE')
diode('D301','12 V zener','BZX55C12',510,195,'BR_SOURCE','BR_GATE',True,True,True,'DO-35')
line((510,185),(510,195));dot(510,185);dot(510,275)
r('R302','1 k / 0.5 W',590,315,'BR_GATE','Q302_C',True,'0.5 W');line((590,275),(590,315));dot(590,275)
part('Q302','Gate pull-down','2N3904',{'1':'GND','2':'Q302_B','3':'Q302_C'},'TO-92','onsemi E=1 B=2 C=3')
line((590,395),(590,430),(565,452));line((565,435),(565,485));line((520,460),(565,460));arrow((565,469),(590,493));line((590,493),(590,525));ground(590,525)
text(615,456,'Q302  2N3904',11,True);text(600,429,'3 C',9);text(524,448,'2 B',9);text(600,508,'1 E',9)
r('R303','1 k',300,460,'BR_EN','Q302_B');line((380,460),(520,460));line((220,460),(300,460));label(220,460,'BR_EN')
r('R304','10 k',435,480,'Q302_B','GND',True);line((435,460),(435,480));dot(435,460);ground(435,560)
line((700,355),(1020,355));label(950,355,'BR_OUT')
conn('J301',875,435,['BR_OUT','GND'],'PERIPHERAL')
conn('J302',70,540,['BR_EN','GND'],'3.3 V ENABLE')
notes(['Default OFF: R304 holds Q302 off; R301 returns Q301 gate to source. BR_EN=3.3 V enables the branch.',
       'D301 cathode at SOURCE, anode at GATE. R302 limits zener/collector current. Verify VGS at both input extremes.',
       'F301 is a wire-protection fuse, NOT a 0.5 A electronic current limit. Short-circuit survival is not established.',
       'Use a current-limited supply and resistive dummy load first. External output power backfeeds through Q301 body diode.',
       'No reverse blocking, current telemetry, UVLO, controlled inrush or independent watchdog is implemented in this revision.'],650)

# 04 -- Two actual optocoupler input circuits, isolated devices but common board ground.
sheet('04  Ignition and selector input conditioning','Two populated active-high 9-16 V sense channels. Output is active LOW. Common return means no system isolation claim.')
def opto_channel(idx,y,raw,out):
    pfx=400+idx*10
    ref='U'+str(400+idx)
    label(60,y,raw);line((60,y),(180,y))
    r(f'R{pfx+1}','680 / 0.5 W',180,y,raw,f'{raw}_MID',power='0.5 W')
    line((260,y),(300,y));r(f'R{pfx+2}','680 / 0.5 W',300,y,f'{raw}_MID',f'{raw}_LED',power='0.5 W')
    line((380,y),(560,y));box(520,y-50,230,150)
    part(ref,'Phototransistor optocoupler','VO617A-3',{'1':f'{raw}_LED','2':'GND','3':'GND','4':out},'DIP-4','A=1 K=2 E=3 C=4')
    text(540,y-30,ref+'  VO617A-3',11,True)
    line((560,y),(560,y+20));polygon([(550,y+20),(570,y+20),(560,y+40)]);line((547,y+42),(573,y+42));line((560,y+42),(560,y+80))
    text(570,y+4,'1 A',8);text(570,y+76,'2 K',8)
    arrow((583,y+22),(612,y+12));arrow((583,y+42),(612,y+32))
    line((665,y+10),(665,y+65));line((665,y+28),(705,y),(850,y));arrow((665,y+45),(705,y+80));text(711,y-6,'4 C',9);text(711,y+77,'3 E',9)
    line((560,y+80),(560,y+120));ground(560,y+120);line((705,y+80),(705,y+120));ground(705,y+120)
    diode(f'D{400+idx}','1N4148','1N4148',440,y,f'{raw}_LED','GND',True,True,False,'DO-35');dot(440,y)
    line((440,y+80),(440,y+120));ground(440,y+120)
    r(f'R{pfx+3}','10 k',850,y-90,'+3V3',out,True);label(850,y-90,'+3V3');line((850,y-10),(850,y));dot(850,y)
    line((850,y),(1030,y));label(970,y,out)
    cap(f'C{400+idx}','10 nF / 16 V',945,y+25,out,'GND');line((945,y),(945,y+25));dot(945,y);ground(945,y+105)
opto_channel(1,245,'IGN_RAW','IGN_N')
opto_channel(2,525,'SEL_RAW','SEL_N')
notes(['Connector J401: 1=IGN_RAW, 2=SEL_RAW, 3=GND. J402: 1=IGN_N, 2=SEL_N, 3=GND (to 3.3 V MCU inputs).',
       'Both connectors are logical bench assignments. Detect 9-16 V asserted; 0-1 V absent; intermediate voltages undefined.',
       'Specify Schmitt-trigger MCU inputs and >=20 ms software debounce. These circuits do not implement precision thresholds.'],689)
part('J401','Sense input header','MECHANICAL-TBD',{'1':'IGN_RAW','2':'SEL_RAW','3':'GND'},'bench terminal')
part('J402','Sense logic header','MECHANICAL-TBD',{'1':'IGN_N','2':'SEL_N','3':'GND'},'bench header')

# 05 -- Every CAN IC pin is shown and electrically assigned.
sheet('05  Hardware-silent CAN receiver','TCAN1051V-Q1 SOIC-8 only. S and TXD tied HIGH; no MCU transmit conductor and no fitted bus termination.')
part('U501','CAN transceiver, VIO variant','TCAN1051VDRQ1',{'1':'+3V3','2':'GND','3':'+5V','4':'CAN_RX_IC','5':'+3V3','6':'CAN_L','7':'CAN_H','8':'+3V3'},'SOIC-8','S hard-high; receive-only design')
box(470,245,235,250);text(487,273,'U501  TCAN1051V',13,True)
for y,pin,name,net in [(310,1,'TXD','+3V3'),(355,8,'S','+3V3'),(400,5,'VIO','+3V3'),(445,4,'RXD','CAN_RX_IC')]:
    line((350,y),(470,y));text(480,y+4,f'{pin}  {name}',10);label(350,y,net)
for y,pin,name,net in [(325,7,'CANH','CAN_H'),(400,6,'CANL','CAN_L')]:
    line((705,y),(1010,y));text(638,y+4,f'{name}  {pin}',10);label(960,y,net)
line((590,245),(590,200));label(590,200,'+5V');text(598,234,'3 VCC',10)
line((590,495),(590,545));ground(590,545);text(600,518,'2 GND',10)
cap('C501','100 nF / 16 V',180,200,'+5V','GND');label(180,200,'+5V');ground(180,280)
cap('C502','100 nF / 16 V',180,360,'+3V3','GND');label(180,360,'+3V3');ground(180,440)
r('R501','1 k',190,535,'CAN_RX_IC','CAN_RX');label(70,535,'CAN_RX_IC');line((70,535),(190,535));line((270,535),(390,535));label(315,535,'CAN_RX')
conn('J501',800,480,['CAN_H','CAN_L','GND'],'BUS HEADER')
conn('J502',70,610,['CAN_RX','GND'],'MCU RECEIVE')
notes(['C501 at VCC pin 3, C502 at VIO pin 5; short return to pin 2. Do not substitute the non-VIO TCAN1051 variant.',
       'No TVS/filter is fitted in this base: short-cable terminated bench bus only. Vehicle ESD/EMC protection remains open.',
       'MCU CAN controller must also use listen-only mode. S is permanently high in copper; firmware cannot enable TX.',
       'External bench bus must already have its two correct endpoint terminations. Do not add a third 120-ohm load.'],675)

c.save()
# Editable text sources and machine-readable evidence, generated from the same pin assignments.
with (OUT/'bom.csv').open('w',newline='') as f:
    w=csv.writer(f,lineterminator='\n');w.writerow(['Ref','Value','MPN_or_selection','Package','Sheet','Notes'])
    for p in parts.values():w.writerow([p[k] for k in ['ref','value','mpn','package','sheet','note']])
with (OUT/'pin-netlist.csv').open('w',newline='') as f:
    w=csv.writer(f,lineterminator='\n');w.writerow(['Ref','Pin','Net','Sheet'])
    for p in parts.values():
        for pin,net in p['pins'].items():w.writerow([p['ref'],pin,net,p['sheet']])
nets=defaultdict(list)
for p in parts.values():
    for pin,net in p['pins'].items():nets[net].append(p['ref']+'.'+pin)
assert all(len(v)>=2 for v in nets.values()), {k:v for k,v in nets.items() if len(v)<2}
assert parts['Q301']['pins']=={'1':'BR_GATE','2':'BR_OUT','3':'BR_SOURCE'}
assert parts['U501']['pins']['8']=='+3V3' and parts['U501']['pins']['1']=='+3V3'
(OUT/'netlist.json').write_text(json.dumps({'revision':'B','components':parts,'nets':nets},indent=2)+'\n')
pdf=fitz.open(OUT/'strijder-circuit-base-rev-b.pdf')
for i,p in enumerate(pdf):
    (OUT/f'sheet-{i+1:02}.svg').write_text(p.get_svg_image())
print(f'{len(pdf)} sheets, {len(parts)} components, {len(nets)} nets. No single-node nets. NOT an ECAD ERC.')
