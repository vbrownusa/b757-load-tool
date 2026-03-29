import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

CARGO_BIN1 = {
    200: 299.6,
    300: 499.4,
    400: 699.1,
    500: 898.9,
    600: 1098.7,
    700: 1298.2,
    800: 1498.0,
    900: 1697.8,
    1000: 1897.5,
}

CARGO_BIN2 = CARGO_BIN1
CARGO_BIN3 = CARGO_BIN1
CARGO_BIN4 = CARGO_BIN1


# -------------------------
# CARGO AWU FUNCTION
# -------------------------

def cargo_awu_by_rule(table, weight):
    if weight is None or weight <= 0:
        return 0.0

    weight = int(weight)

    # sort AWU values ascending
    awu_values = sorted(table.values())

    for awu in awu_values:
        # truncate last two digits (convert to usable weight)
        equiv_lbs = int(awu) - (int(awu) % 100)

        if weight <= equiv_lbs:
            return awu

    # if above all ranges, return max
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

BOW = 129614.1   

season = st.radio("Season", ["summer", "winter"])

# -------------------------
# PASSENGERS
# -------------------------
st.divider()
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
# BAGGAGE
# -------------------------
st.divider()
st.subheader("Baggage")

cols = st.columns(4)

with cols[0]:
    b1 = st.number_input("Bin 1", min_value=0, value=None, key="bag1")
    b1_awu = bag_awu(int(b1)) if b1 is not None else 0.0
    st.caption(f"{b1_awu:.1f}")

with cols[1]:
    b2 = st.number_input("Bin 2", min_value=0, value=None, key="bag2")
    b2_awu = bag_awu(int(b2)) if b2 is not None else 0.0
    st.caption(f"{b2_awu:.1f}")

with cols[2]:
    b3 = st.number_input("Bin 3", min_value=0, value=None, key="bag3")
    b3_awu = bag_awu(int(b3)) if b3 is not None else 0.0
    st.caption(f"{b3_awu:.1f}")

with cols[3]:
    b4 = st.number_input("Bin 4", min_value=0, value=None, key="bag4")
    b4_awu = bag_awu(int(b4)) if b4 is not None else 0.0
    st.caption(f"{b4_awu:.1f}")


# -------------------------
# CARGO
# -------------------------
st.divider()
st.subheader("Cargo")

cargo_cols = st.columns(4)

with cargo_cols[0]:
    c1 = st.number_input("Bin 1", min_value=0, value=None, key="cargo1")
    c1_awu = cargo_awu_by_rule(CARGO_BIN1, int(c1)) if c1 is not None else 0.0
    st.caption(f"{c1_awu:.1f}")

with cargo_cols[1]:
    c2 = st.number_input("Bin 2", min_value=0, value=None, key="cargo2")
    c2_awu = cargo_awu_by_rule(CARGO_BIN2, int(c2)) if c2 is not None else 0.0
    st.caption(f"{c2_awu:.1f}")

with cargo_cols[2]:
    c3 = st.number_input("Bin 3", min_value=0, value=None, key="cargo3")
    c3_awu = cargo_awu_by_rule(CARGO_BIN3, int(c3)) if c3 is not None else 0.0
    st.caption(f"{c3_awu:.1f}")

with cargo_cols[3]:
    c4 = st.number_input("Bin 4", min_value=0, value=None, key="cargo4")
    c4_awu = cargo_awu_by_rule(CARGO_BIN4, int(c4)) if c4 is not None else 0.0
    st.caption(f"{c4_awu:.1f}")


# -------------------------
# CALCULATIONS
# -------------------------

# Passengers
za = pax_awu("A", int(a), season) if a is not None else 0.0
zb = pax_awu("B", int(b), season) if b is not None else 0.0
zc = pax_awu("C", int(c), season) if c is not None else 0.0

# Baggage
b1_awu = bag_awu(int(b1)) if b1 is not None else 0.0
b2_awu = bag_awu(int(b2)) if b2 is not None else 0.0
b3_awu = bag_awu(int(b3)) if b3 is not None else 0.0
b4_awu = bag_awu(int(b4)) if b4 is not None else 0.0

# Cargo
c1_awu = cargo_awu_by_rule(CARGO_BIN1, int(c1)) if c1 is not None else 0.0
c2_awu = cargo_awu_by_rule(CARGO_BIN2, int(c2)) if c2 is not None else 0.0
c3_awu = cargo_awu_by_rule(CARGO_BIN3, int(c3)) if c3 is not None else 0.0
c4_awu = cargo_awu_by_rule(CARGO_BIN4, int(c4)) if c4 is not None else 0.0


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

st.subheader("Summary")


st.subheader("ZFW")

zfw = (
    BOW
    + za + zb + zc
    + b1_awu + b2_awu + b3_awu + b4_awu
    + c1_awu + c2_awu + c3_awu + c4_awu
)

st.write(f"{zfw:.1f}")




