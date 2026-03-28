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

st.title("B757 Dispatch Tool")

season = st.radio("Season", ["summer", "winter"])

a = int(st.number_input("Zone A Pax", 0, 54))
za = pax_awu("A", a, season)
st.write(f"AWU: {za:.1f}")

b = int(st.number_input("Zone B Pax", 0, 80))
zb = pax_awu("B", b, season)
st.write(f"AWU: {zb:.1f}")

c = int(st.number_input("Zone C Pax", 0, 84))
zc = pax_awu("C", c, season)
st.write(f"AWU: {zc:.1f}")

# -------------------------
# TOTAL
# -------------------------

st.subheader("Passenger Total AWU")
st.write(round(za + zb + zc, 1))
