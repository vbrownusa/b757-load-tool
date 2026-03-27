import streamlit as st
import pandas as pd
from docx import Document

# -------------------------
# LOAD PASSENGER DATA
# -------------------------
@st.cache_data
def load_pax_data():
    df = pd.read_csv("pax_data.csv")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Drop bad rows
    df = df.dropna()

    # Clean values
    df["zone"] = df["zone"].astype(str).str.strip().str.upper()
    df["pax"] = df["pax"].astype(int)

    return df
# -------------------------
# ✅ ADD TABLES HERE (TOP LEVEL)
# -------------------------

ZONE_A = { ... }
ZONE_B = { ... }
ZONE_C = { ... }

# -------------------------
# FUNCTIONS
# -------------------------

pax_df = load_pax_data()


def pax_awu(df, zone, pax, season):
    if pax == 0:
        return 0

    row = df[(df["zone"] == zone) & (df["pax"] == int(pax))]

    if row.empty:
        st.error(f"Missing AWU data for Zone {zone}, Pax {pax}")
        return 0

    return float(row.iloc[0][season])

def generate_release(data):
    ...
    
# -------------------------
# UI (BOTTOM)
# -------------------------

st.title("B757 Weight and Balance Tool")

# -------------------------
# TEST FUNCTION (CLEAN)
# -------------------------

def generate_release(data):
    doc = Document()

    def add(text, bold=False):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = bold

    add("B757 Weight and Balance Key", True)

    add("PASSENGERS", True)
    add(f"Zone A: {data['zoneA']}")
    add(f"Zone B: {data['zoneB']}")
    add(f"Zone C: {data['zoneC']}")

    add("BAGGAGE (DOMESTIC)", True)
    add(f"Bin 1: {data['bag1']}")
    add(f"Bin 2: {data['bag2']}")
    add(f"Bin 3: {data['bag3']}")
    add(f"Bin 4: {data['bag4']}")

    add("REVENUE CARGO", True)
    add(f"Bin 1: {data['cargo_vals'][0]}")
    add(f"Bin 2: {data['cargo_vals'][1]}")
    add(f"Bin 3: {data['cargo_vals'][2]}")
    add(f"Bin 4: {data['cargo_vals'][3]}")

    file = "release.docx"
    doc.save(file)

    return file


# -------------------------
# SIMPLE TEST UI
# -------------------------

season = st.radio("Season", ["summer", "winter"], horizontal=True)

col1, col2, col3 = st.columns(3)


with col1:
    a = int(st.number_input("Zone A", min_value=0, max_value=54, step=1))
    b = int(st.number_input("Zone B", min_value=0, max_value=80, step=1))
    c = int(st.number_input("Zone C", min_value=0, max_value=84, step=1))

with col2:
    b1 = st.number_input("Bin 1 Bags", 0)
    b2 = st.number_input("Bin 2 Bags", 0)
    b3 = st.number_input("Bin 3 Bags", 0)
    b4 = st.number_input("Bin 4 Bags", 0)

with col3:
    c1 = st.number_input("Cargo Bin 1", min_value=0, value=0)
    c2 = st.number_input("Cargo Bin 2", min_value=0, value=0)
    c3 = st.number_input("Cargo Bin 3", min_value=0, value=0)
    c4 = st.number_input("Cargo Bin 4", min_value=0, value=0)

rf = st.number_input("Ramp Fuel", 0)
tf = st.number_input("Taxi Fuel", 0)


BOW = 129621.4

za = pax_awu(pax_df, "A", a, season)
zb = pax_awu(pax_df, "B", b, season)
zc = pax_awu(pax_df, "C", c, season)

bags = [b1*20, b2*20, b3*20, b4*20]
cargo = [c1, c2, c3, c4]

zfw = BOW + za + zb + zc + sum(bags) + sum(cargo)

st.write("ZFW:", round(zfw,1))
