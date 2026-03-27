import streamlit as st
import math
from docx import Document
from docx.shared import Pt

def generate_release(data):

    doc = Document()

    # --- STYLE ---
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(12)

    pf = style.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0

    def add(text, bold=False, size=12):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = bold
        run.font.name = 'Calibri'
        run.font.size = Pt(size)

    # --- HEADER ---
    add("B757 Weight and Balance Key", True, 14)

    # --- BOW ---
    add("WEIGHT AND BALANCE SUMMARY", True)
    add(f"BOW: {data['bow']:.1f}")

    # --- PASSENGERS ---
    add("PASSENGERS", True)
    add(f"{data['zoneA_pax']} pax  Zone A: {data['zoneA']:.1f}")
    add(f"{data['zoneB_pax']} pax  Zone B: {data['zoneB']:.1f}")
    add(f"{data['zoneC_pax']} pax  Zone C: {data['zoneC']:.1f}")
    ZONE_A = {1:(199.8,199.8),2:(299.6,299.5),3:(499.3,499.3),4:(699.1,699.1),5:(798.9,898.9),
6:(998.7,998.6),7:(1198.5,1198.4),8:(1298.2,1398.2),9:(1498.0,1498.0),
10:(1697.8,1697.7),11:(1797.6,1897.5),12:(1997.4,1997.3),13:(2097.1,2197.1),
14:(2296.9,2396.8),15:(2496.7,2596.6),16:(2596.5,2696.4),17:(2796.3,2896.2),
18:(2996.0,3095.9),19:(3095.8,3195.7),20:(3295.6,3395.5),21:(3495.4,3595.2),
22:(3595.2,3695.0),23:(3795.0,3894.8),24:(3994.7,4094.6),25:(4094.5,4294.3),
26:(4294.3,4394.1),27:(4494.1,4593.9),28:(4593.9,4793.7),29:(4793.6,4893.4),
30:(4993.4,5093.2),31:(5093.2,5293.0),32:(5293.0,5392.8),33:(5392.8,5592.5),
34:(5592.5,5792.3),35:(5792.3,5992.1),36:(5892.1,6091.9),37:(6091.9,6291.6),
38:(6291.7,6491.4),39:(6391.4,6591.2),40:(6591.2,6791.0),41:(6791.0,6990.7),
42:(6890.8,7090.5),43:(7090.6,7290.3),44:(7290.3,7490.0),45:(7390.1,7689.8),
46:(7589.9,7789.6),47:(7789.7,7989.4),48:(7889.5,8189.1),49:(8089.2,8288.9),
50:(8289.0,8488.7),51:(8388.8,8688.5),52:(8588.6,8788.2),53:(8688.4,8988.0),
54:(8888.1,9187.8)
}

ZONE_B = {1:(200.0,200.0),2:(299.9,299.9),3:(499.9,499.9),4:(699.8,699.8),5:(799.8,899.8),
6:(999.7,999.7),7:(1199.7,1199.7),8:(1299.7,1399.7),9:(1499.6,1499.6),
10:(1699.6,1699.6),11:(1799.5,1899.5),12:(1999.5,1999.5),13:(2099.4,2199.4),
14:(2299.4,2399.4),15:(2499.4,2599.3),16:(2599.3,2699.3),17:(2799.3,2899.3),
18:(2999.2,3099.2),19:(3099.2,3199.2),20:(3299.2,3399.1),21:(3499.1,3599.1),
22:(3599.1,3699.0),23:(3799.0,3899.0),24:(3999.0,4099.0),25:(4098.9,4298.9),
26:(4298.9,4398.9),27:(4498.9,4598.8),28:(4598.8,4798.8),29:(4798.8,4898.7),
30:(4998.7,5098.7),31:(5098.7,5298.6),32:(5298.6,5398.6),33:(5398.6,5598.6),
34:(5598.6,5798.5),35:(5798.5,5998.5),36:(5898.5,6098.4),37:(6098.4,6298.4),
38:(6298.4,6498.3),39:(6398.3,6598.3),40:(6598.3,6798.3),41:(6798.3,6998.2),
42:(6898.2,7098.2),43:(7098.2,7298.1),44:(7298.1,7498.1),45:(7398.1,7698.0),
46:(7598.0,7798.0),47:(7797.0,7997.9),48:(7897.0,8197.9),49:(8097.9,8297.9),
50:(8297.9,8497.8),51:(8397.8,8697.8),52:(8597.8,8797.7),53:(8697.8,8997.7),
54:(8897.7,9197.6),55:(9097.7,9397.6),56:(9197.6,9497.6),57:(9397.6,9697.5),
58:(9597.5,9897.5),59:(9697.5,9997.4),60:(9897.5,10197.4),61:(10097.4,10397.3),
62:(10197.4,10497.3),63:(10397.3,10697.2),64:(10597.3,10897.2),65:(10697.2,11097.2),
66:(10897.2,11197.1),67:(11097.2,11397.1),68:(11197.1,11597.0),69:(11397.1,11697.0),
70:(11597.0,11896.9),71:(11697.0,12096.9),72:(11896.9,12196.9),73:(11996.9,12396.8),
74:(12196.9,12596.8),75:(12396.8,12796.7),76:(12496.8,12896.7),77:(12696.7,13096.6),
78:(12996.7,13296.6),79:(12996.6,13396.5),80:(13196.6,13596.5)
}

ZONE_C = {1:(200.1,200.2),2:(300.3,300.3),3:(500.4,500.5),4:(700.6,700.6),5:(800.7,900.8),
6:(1000.9,1000.9),7:(1201.0,1201.1),8:(1301.2,1401.2),9:(1501.3,1501.4),
10:(1701.5,1701.5),11:(1801.6,1901.7),12:(2001.8,2001.8),13:(2101.9,2202.0),
14:(2302.0,2402.1),15:(2502.2,2602.3),16:(2602.3,2702.4),17:(2802.5,2902.6),
18:(3002.6,3102.7),19:(3102.8,3202.9),20:(3302.9,3403.0),21:(3503.1,3603.2),
22:(3603.2,3703.3),23:(3803.4,3903.5),24:(4003.5,4103.6),25:(4103.7,4303.8),
26:(4303.8,4403.9),27:(4503.9,4604.1),28:(4604.1,4804.2),29:(4804.2,4904.4),
30:(5004.4,5104.5),31:(5104.5,5304.7),32:(5304.7,5404.8),33:(5404.8,5605.2),
34:(5605.0,5805.1),35:(5805.1,6005.3),36:(5905.3,6105.4),37:(6105.4,6305.6),
38:(6305.6,6505.7),39:(6405.7,6605.9),40:(6605.8,6806.0),41:(6806.0,7006.2),
42:(6906.1,7106.3),43:(7106.3,7306.5),44:(7306.4,7506.6),45:(7406.6,7706.8),
46:(7606.7,7806.9),47:(7806.9,8007.1),48:(7907.0,8207.2),49:(8107.2,8307.4),
50:(8307.3,8507.5),51:(8407.5,8707.7),52:(8607.6,8807.8),53:(8707.7,9008.0),
54:(8907.9,9208.1),55:(9108.0,9408.3),56:(9208.2,9508.4),57:(9408.3,9708.6),
58:(9608.5,9908.7),59:(9708.6,10008.9),60:(9908.8,10209.2),61:(10108.9,10409.5),
62:(10209.1,10509.3),63:(10409.2,10709.5),64:(10609.4,10909.6),65:(10709.5,11109.8),
66:(10909.7,11209.9),67:(11109.8,11410.1),68:(11209.9,11610.2),69:(11410.1,11710.4),
70:(11610.2,11910.5),71:(11710.4,12110.7),72:(11910.5,12210.8),73:(12010.7,12411.0),
74:(12210.8,12611.1),75:(12411.0,12811.3),76:(12511.1,12911.5),77:(12711.3,13111.6),
78:(12911.4,13311.8),79:(13011.6,13411.9),80:(13211.7,13612.1),81:(13411.8,13812.2),
82:(13512.0,13912.4),83:(13712.1,14112.5),84:(13912.3,14312.7)}

 # --- BAGGAGE ---
add("BAGGAGE (DOMESTIC)", True)
add(f"{data['bag1_ct']} bags  Bin 1: {data['bag1']:.1f}")
add(f"{data['bag2_ct']} bags  Bin 2: {data['bag2']:.1f}")
add(f"{data['bag3_ct']} bags  Bin 3: {data['bag3']:.1f}")
add(f"{data['bag4_ct']} bags  Bin 4: {data['bag4']:.1f}")

    # --- CARGO ---
    add("REVENUE CARGO", True)
    add(f"{data['cargo1']} lbs  Bin 1: {data['cargo_vals'][0]:.1f}")
    add(f"{data['cargo2']} lbs  Bin 2: {data['cargo_vals'][1]:.1f}")
    add(f"{data['cargo3']} lbs  Bin 3: {data['cargo_vals'][2]:.1f}")
    add(f"{data['cargo4']} lbs  Bin 4: {data['cargo_vals'][3]:.1f}")

    # --- ZFW ---
    add(f"ADJUSTED ZFW: {data['zfw']:.1f} lbs", True)

    # --- FUEL ---
    add("FUEL", True)
    add(f"Ramp Fuel: {data['ramp']:.1f} lbs")
    add(f"Taxi Fuel: {data['taxi']:.1f} lbs")
    add(f"Takeoff Fuel: {data['tof']:.1f} lbs")
    add(f"Fuel AWU: {data['fuel_awu']:.1f}")

    # --- TOW ---
    add(f"PLANNED TAKEOFF WEIGHT: {data['tow']:.1f} lbs", True)

    # --- CG ---
    add("CG LIMIT CHECK (INTERPOLATED)", True)
    add(
        f"ZFW ({data['zfw_w']:,} lbs): CG {data['zfw_cg']:.1f}% | "
        f"{data['zfw_fwd']:.2f}–{data['zfw_aft']:.2f}"
    )
    add(
        f"TOW ({data['tow_w']:,} lbs): CG {data['tow_cg']:.1f}% | "
        f"{data['tow_fwd']:.2f}–{data['tow_aft']:.2f}"
    )

    # --- TRIM ---
    add("STABILIZER TRIM", True)
    add(f"Planned TOW: {data['tow_w']:,} lbs")
    add(f"Planned CG: {data['tow_cg']:.1f}%")
    add(f"Trim: {data['trim']} ANU")

    file = "B757_Release.docx"
    doc.save(file)

    return file


st.set_page_config(layout="wide")
season = st.radio("Season", ["summer", "winter"], horizontal=True)
BOW = 129621.4
zone_A = {
    1:(199.8,199.8),
    2:(299.6,299.5),
    54:(8888.1,9187.8)
}

zone_B = {
    1:(200.0,200.0),
    2:(299.9,299.9),
    80:(13196.6,13596.5)
}

zone_C = {
    1:(200.1,200.2),
    2:(300.3,300.3),
    84:(13912.3,14312.7)
}
def round100(x): return int(round(x/100))*100
def cg(x): return (x%1000)/10
def interp(x,x1,x2,y1,y2): return y1+(y2-y1)*(x-x1)/(x2-x1)
def qtr(x): return round(x*4)/4

def frac(x):
    w=int(x);f=round(x-w,2)
    return f"{w}{ {0.25:'¼',0.5:'½',0.75:'¾'}.get(f,'') }"

st.title("✈️ B757 Dispatch Tool")

col1,col2,col3 = st.columns(3)

with col1:
    a = st.number_input("Zone A",0,54)
    b = st.number_input("Zone B",0,80)
    c = st.number_input("Zone C",0,84)

with col2:
    b1 = st.number_input("Bin1",0)
    b2 = st.number_input("Bin2",0)
    b3 = st.number_input("Bin3",0)
    b4 = st.number_input("Bin4",0)

with col3:
    c1 = st.number_input("Cargo1",0)
    c2 = st.number_input("Cargo2",0)
    c3 = st.number_input("Cargo3",0)
    c4 = st.number_input("Cargo4",0)

rf = st.number_input("Ramp Fuel",0)
tf = st.number_input("Taxi Fuel",0)

za = a * 190
zb = b * 190
zc = c * 190

bag_rows = [
    (1,31,499.4,499.6,500.3,500.6),
    (32,53,998.7,999.2,1000.7,1001.3),
    (54,74,1498.1,1498.8,1501.0,1501.9),
    (75,95,1997.5,1998.4,2001.4,2002.6),
    (96,117,2496.8,2498.0,2501.7,2503.2),
]

def bag_awu(bags, idx):
    for r in bag_rows:
        if r[0] <= bags <= r[1]:
            return r[2+idx]
    return 0

bags = [
    bag_awu(b1,0),
    bag_awu(b2,1),
    bag_awu(b3,2),
    bag_awu(b4,3)
]
import math

cargo_rows = [
    (499.4,499.6,500.3,500.6),
    (998.7,999.2,1000.7,1001.3),
    (1498.1,1498.8,1501.0,1501.9),
    (1997.5,1998.4,2001.4,2002.6),
    (2496.8,2498.0,2501.7,2503.2),
    (2996.2,2997.5,3002.1,3003.8),
    (4494.3,4495.6,4503.0,4504.7),
    (5495.5,5496.8,5503.9,5505.7),
    (7004.8,7006.2,7014.6,7016.6),
]

def cargo_awu(vals):
    rounded = [math.ceil(v/100)*100 for v in vals]
    for row in cargo_rows:
        caps = [int(x//1000)*1000 for x in row]
        if all(c >= r for c,r in zip(caps,rounded)):
            return row
    return [0,0,0,0]

cargo = cargo_awu([c1,c2,c3,c4])

fuel_raw = rf - tf

def fuel_awu(f):
    r = math.ceil(f/100)*100
    table = {
        29100: 29104.1,
        30000: 30004.0,
        35000: 35003.3,
        40000: 40002.5
    }
    for k in sorted(table):
        if k >= r:
            return table[k]
    return table[max(table)]

fuel = fuel_awu(fuel_raw)

zfw = BOW + za + zb + zc + sum(bags) + sum(cargo)
tow = zfw + fuel

zfw_w = round100(zfw)
tow_w = round100(tow)

zfw_cg = cg(zfw)
tow_cg = cg(tow)

zfw_fwd = interp(zfw_w,175000,180000,11.4,11.2)
zfw_aft = interp(zfw_w,175000,180000,34.3,34.8)

tow_fwd = interp(tow_w,205000,210000,9.7,9.4)
tow_aft = interp(tow_w,205000,210000,37.2,37.6)

def status(val,f,a):
    return "🟢" if f<=val<=a else "🔴"

t1 = interp(tow_cg,29,34,3.5,3.0)
t2 = interp(tow_cg,29,34,3.75,3.25)
trim = frac(qtr(interp(tow_w,200000,220000,t1,t2)))

st.divider()
st.subheader("Results")

st.write(f"ZFW: {zfw:.1f}")
st.write(f"TOW: {tow:.1f}")

st.write(f"{status(zfw_cg,zfw_fwd,zfw_aft)} ZFW CG {zfw_cg:.1f}%")
st.write(f"{status(tow_cg,tow_fwd,tow_aft)} TOW CG {tow_cg:.1f}%")

st.write(f"### Trim: {trim} ANU")


report_data = {
    "bow": BOW,

    "zoneA_pax": a,
    "zoneB_pax": b,
    "zoneC_pax": c,

    "zoneA": za,
    "zoneB": zb,
    "zoneC": zc,

    "bag1_ct": b1,
    "bag2_ct": b2,
    "bag3_ct": b3,
    "bag4_ct": b4,

    "bag1": bags[0],
    "bag2": bags[1],
    "bag3": bags[2],
    "bag4": bags[3],

    "cargo1": c1,
    "cargo2": c2,
    "cargo3": c3,
    "cargo4": c4,

    "cargo_vals": cargo,

    "zfw": zfw,
    "tow": tow,

    "ramp": rf,
    "taxi": tf,
    "tof": rf - tf,
    "fuel_awu": fuel,

    "zfw_w": zfw_w,
    "tow_w": tow_w,

    "zfw_cg": zfw_cg,
    "tow_cg": tow_cg,

    "zfw_fwd": zfw_fwd,
    "zfw_aft": zfw_aft,
    "tow_fwd": tow_fwd,
    "tow_aft": tow_aft,

    "trim": trim

def generate_release(data):

    doc = Document()

    def add(text, bold=False):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = bold

    add("B757 Weight and Balance Key", True)

    add("PASSENGERS", True)
    add(f"A: {data['zoneA']}")
    add(f"B: {data['zoneB']}")
    add(f"C: {data['zoneC']}")

    add("BAGGAGE (DOMESTIC)", True)
    add(f"Bin1: {data['bag1']}")
    add(f"Bin2: {data['bag2']}")
    add(f"Bin3: {data['bag3']}")
    add(f"Bin4: {data['bag4']}")

    doc.save("release.docx")

    return "release.docx"
