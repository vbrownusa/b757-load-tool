import streamlit as st
import math

st.set_page_config(layout="wide")

BOW = 129621.4

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

fuel = rf - tf

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
