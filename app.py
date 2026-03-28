import streamlit as st
import pandas as pd

# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data
def load_pax_data():
    df = pd.read_csv("pax_data.csv")
    df.columns = df.columns.str.strip().str.lower()
    df["zone"] = df["zone"].str.strip().str.upper()
    df["pax"] = df["pax"].astype(int)
    return df

pax_df = load_pax_data()

# -------------------------
# LOOKUP FUNCTION
# -------------------------

def pax_awu(zone, pax, season):
    if pax == 0:
        return 0.0

    row = pax_df[(pax_df["zone"] == zone) & (pax_df["pax"] == pax)]

    if row.empty:
        return 0.0

    return float(row.iloc[0][season])

# -------------------------
# UI
# -------------------------

st.title("Weight and Balance (B757-200 Adj BOW 129614.1)")

season = st.radio("Season", ["summer", "winter"])

# -------------------------
# PASSENGERS
# -------------------------

st.subheader("Passengers")

a = int(st.number_input("Zone A Pax", 0, 54))
za = pax_awu("A", a, season)
st.caption(f"AWU: {za:.1f}")

b = int(st.number_input("Zone B Pax", 0, 80))
zb = pax_awu("B", b, season)
st.caption(f"AWU: {zb:.1f}")

c = int(st.number_input("Zone C Pax", 0, 84))
zc = pax_awu("C", c, season)
st.caption(f"AWU: {zc:.1f}")

# -------------------------
# BAGGAGE (simple for now)
# -------------------------

st.subheader("Baggage")

def bag_awu(count):
    return count * 32.0

b1 = st.number_input("Bin 1 Bags", 0)
b1_awu = bag_awu(b1)
st.caption(f"AWU: {b1_awu:.1f}")

b2 = st.number_input("Bin 2 Bags", 0)
b2_awu = bag_awu(b2)
st.caption(f"AWU: {b2_awu:.1f}")

b3 = st.number_input("Bin 3 Bags", 0)
b3_awu = bag_awu(b3)
st.caption(f"AWU: {b3_awu:.1f}")

b4 = st.number_input("Bin 4 Bags", 0)
b4_awu = bag_awu(b4)
st.caption(f"AWU: {b4_awu:.1f}")

# -------------------------
# CARGO (your rule)
# -------------------------

st.subheader("Cargo")

CARGO_BIN1 = {
    200:299.6,
    300:499.4,
    400:699.1,
    500:898.9,
    600:1098.7,
    700:1298.2,
    800:1498.0,
    900:1697.8,
    1000:1897.5,
}

def cargo_awu(weight):
    if weight <= 0:
        return 0.0

    awu_values = sorted(CARGO_BIN1.values())

    for awu in awu_values:
        equiv = int(awu) - (int(awu) % 100)
        if equiv >= weight:
            return awu

    return awu_values[-1]

c1 = st.number_input("Cargo Bin 1 (lbs)", 0)
c1_awu = cargo_awu(c1)
st.caption(f"AWU: {c1_awu:.1f}")

c2 = st.number_input("Cargo Bin 2 (lbs)", 0)
c2_awu = cargo_awu(c2)
st.caption(f"AWU: {c2_awu:.1f}")

c3 = st.number_input("Cargo Bin 3 (lbs)", 0)
c3_awu = cargo_awu(c3)
st.caption(f"AWU: {c3_awu:.1f}")

c4 = st.number_input("Cargo Bin 4 (lbs)", 0)
c4_awu = cargo_awu(c4)
st.caption(f"AWU: {c4_awu:.1f}")

# -------------------------
# TOTAL
# -------------------------

st.subheader("Passenger Total AWU")
st.write(round(za + zb + zc, 1))
