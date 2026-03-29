import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

# -------------------------
# CARGO AWU FUNCTION
# -------------------------

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

# for now (to avoid more errors), copy same table:
CARGO_BIN2 = CARGO_BIN1
CARGO_BIN3 = CARGO_BIN1
CARGO_BIN4 = CARGO_BIN1



def cargo_awu_by_rule(table, weight):
    if weight <= 0:
        return 0.0

    awu_values = sorted(table.values())

    for awu in awu_values:
        equiv = int(awu) - (int(awu) % 100)

        if equiv >= weight:
            return awu

    return awu_values[-1]


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
# BAG AWU TABLE (RANGE BASED)
# -------------------------

BAG_TABLE = [
    (0, 0, 0.0),
    (1, 10, 320.0),
    (11, 20, 640.0),
    (21, 30, 960.0),
    (31, 40, 1280.0),
    (41, 50, 1600.0),
    (51, 60, 1920.0),
    (61, 70, 2240.0),
    (71, 80, 2560.0),
]

def bag_awu(count):
    count = int(count)

    for low, high, awu in BAG_TABLE:
        if low <= count <= high:
            return awu

    return BAG_TABLE[-1][2]


# -------------------------
# CARGO AWU FUNCTION
# -------------------------

def cargo_awu_by_rule(table, weight):
    if weight <= 0:
        return 0.0

    awu_values = sorted(table.values())

    for awu in awu_values:
        # ignore last digits → convert to hundreds
        equiv = int(awu) - (int(awu) % 100)

        if equiv >= weight:
            return awu

    return awu_values[-1]




# -------------------------
# UI
# -------------------------

st.title("Weight and Balance")
st.subheader("B757-200 Adj BOW 129614.1")

season = st.radio("Season", ["summer", "winter"])

# -------------------------
# PASSENGERS
# -------------------------

st.subheader("Passengers")

col1, col2, col3 = st.columns(3)

with col1:
    a = st.number_input("Zone A Pax", min_value=0, max_value=54, value=None, key="zoneA")
    za = pax_awu("A", int(a), season) if a is not None else 0.0
    st.caption(f"AWU: {za:.1f}")

with col2:
    b = st.number_input("Zone B Pax", min_value=0, max_value=80, value=None, key="zoneB")
    zb = pax_awu("B", int(b), season) if b is not None else 0.0
    st.caption(f"AWU: {zb:.1f}")

with col3:
    c = st.number_input("Zone C Pax", min_value=0, max_value=84, value=None, key="zoneC")
    zc = pax_awu("C", int(c), season) if c is not None else 0.0
    st.caption(f"AWU: {zc:.1f}")

# -------------------------
# BAGGAGE (simple for now)
# -------------------------

st.subheader("Baggage")

cols = st.columns(4)

with cols[0]:
    b1 = st.number_input("Bin 1", 0, key="bag1")
    b1_awu = bag_awu(b1)
    st.caption(f"{b1_awu:.1f}")

with cols[1]:
    b2 = st.number_input("Bin 2", 0, key="bag2")
    b2_awu = bag_awu(b2)
    st.caption(f"{b2_awu:.1f}")

with cols[2]:
    b3 = st.number_input("Bin 3", 0, key="bag3")
    b3_awu = bag_awu(b3)
    st.caption(f"{b3_awu:.1f}")

with cols[3]:
    b4 = st.number_input("Bin 4", 0, key="bag4")
    b4_awu = bag_awu(b4)
    st.caption(f"{b4_awu:.1f}")


# -------------------------
# CARGO (your rule)
# -------------------------

st.subheader("Cargo")

cargo_cols = st.columns(4)

with cargo_cols[0]:
    c1 = st.number_input("Bin 1", 0, key="cargo1")
    c1_awu = cargo_awu_by_rule(CARGO_BIN1, c1)
    st.caption(f"{c1_awu:.1f}")

with cargo_cols[1]:
    c2 = st.number_input("Bin 2", 0, key="cargo2")
    c2_awu = cargo_awu_by_rule(CARGO_BIN2, c2)
    st.caption(f"{c2_awu:.1f}")

with cargo_cols[2]:
    c3 = st.number_input("Bin 3", 0, key="cargo3")
    c3_awu = cargo_awu_by_rule(CARGO_BIN3, c3)
    st.caption(f"{c3_awu:.1f}")

with cargo_cols[3]:
    c4 = st.number_input("Bin 4", 0, key="cargo4")
    c4_awu = cargo_awu_by_rule(CARGO_BIN4, c4)
    st.caption(f"{c4_awu:.1f}")



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


# -------------------------
# TOTAL
# -------------------------



st.divider()
