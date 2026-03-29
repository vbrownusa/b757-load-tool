import streamlit as st
import pandas as pd
import math

st.set_page_config(layout="wide")

# -------------------------
# CONSTANTS
# -------------------------

BOW = 129614.1

# -------------------------
# CARGO TABLES
# -------------------------

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
# FUEL AWU TABLE (REPLACE WITH YOUR REAL DATA)
# -------------------------

FUEL_AWU_TABLE = {
    1000: 998.0,
    2000: 1996.0,
    3000: 2994.0,
    4000: 3992.0,
    5000: 4990.0,
    6000: 5988.0,
    7000: 6986.0,
    8000: 7984.0,
    9000: 8982.0,
    10000: 9980.0,
    11000: 10978.0,
    12000: 11976.0,
    13000: 12974.0,
    14000: 13972.0,
    15000: 14970.0,
}

# -------------------------
# LOAD PAX DATA
# -------------------------

@st.cache_data
def load_pax_data():
    return pd.read_csv("pax_data.csv")

pax_df = load_pax_data()

# -------------------------
# FUNCTIONS
# -------------------------

def pax_awu(zone, pax, season):
    if pax is None or pax == 0:
        return 0.0

    row = pax_df[(pax_df["zone"] == zone) & (pax_df["pax"] == pax)]

    if row.empty:
        st.error(f"Missing AWU data: Zone {zone}, Pax {pax}")
        return 0.0

    return float(row.iloc[0][season])


def bag_awu(count):
    if count is None or count == 0:
        return 0.0
    return int(count) * 32.0  # replace later with real table


def cargo_awu_by_rule(table, weight):
    if weight is None or weight <= 0:
        return 0.0

    weight = int(weight)

    for awu in sorted(table.values()):
        equiv_lbs = int(awu) - (int(awu) % 100)
        if weight <= equiv_lbs:
            return awu

    return max(table.values())


def fuel_awu_lookup(weight):
    if weight is None or weight <= 0:
        return 0.0

    rounded = int(math.ceil(weight / 100.0) * 100)

    if rounded in FUEL_AWU_TABLE:
        return FUEL_AWU_TABLE[rounded]

    keys = sorted(FUEL_AWU_TABLE.keys())
    for k in keys:
        if rounded <= k:
            return FUEL_AWU_TABLE[k]

    return FUEL_AWU_TABLE[keys[-1]]

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
    a = st.number_input("Zone A Pax", 0, 54, value=None, key="zoneA")
    za = pax_awu("A", int(a), season) if a is not None else 0.0
    st.caption(f"{za:.1f}")

with col2:
    b = st.number_input("Zone B Pax", 0, 80, value=None, key="zoneB")
    zb = pax_awu("B", int(b), season) if b is not None else 0.0
    st.caption(f"{zb:.1f}")

with col3:
    c = st.number_input("Zone C Pax", 0, 84, value=None, key="zoneC")
    zc = pax_awu("C", int(c), season) if c is not None else 0.0
    st.caption(f"{zc:.1f}")

# -------------------------
# BAGGAGE
# -------------------------

st.subheader("Baggage")

cols = st.columns(4)

with cols[0]:
    b1 = st.number_input("Bin 1", 0, value=None, key="bag1")
    b1_awu = bag_awu(b1)
    st.caption(f"{b1_awu:.1f}")

with cols[1]:
    b2 = st.number_input("Bin 2", 0, value=None, key="bag2")
    b2_awu = bag_awu(b2)
    st.caption(f"{b2_awu:.1f}")

with cols[2]:
    b3 = st.number_input("Bin 3", 0, value=None, key="bag3")
    b3_awu = bag_awu(b3)
    st.caption(f"{b3_awu:.1f}")

with cols[3]:
    b4 = st.number_input("Bin 4", 0, value=None, key="bag4")
    b4_awu = bag_awu(b4)
    st.caption(f"{b4_awu:.1f}")

# -------------------------
# CARGO
# -------------------------

st.subheader("Cargo")

cargo_cols = st.columns(4)

with cargo_cols[0]:
    c1 = st.number_input("Bin 1", 0, value=None, key="cargo1")
    c1_awu = cargo_awu_by_rule(CARGO_BIN1, c1)
    st.caption(f"{c1_awu:.1f}")

with cargo_cols[1]:
    c2 = st.number_input("Bin 2", 0, value=None, key="cargo2")
    c2_awu = cargo_awu_by_rule(CARGO_BIN2, c2)
    st.caption(f"{c2_awu:.1f}")

with cargo_cols[2]:
    c3 = st.number_input("Bin 3", 0, value=None, key="cargo3")
    c3_awu = cargo_awu_by_rule(CARGO_BIN3, c3)
    st.caption(f"{c3_awu:.1f}")

with cargo_cols[3]:
    c4 = st.number_input("Bin 4", 0, value=None, key="cargo4")
    c4_awu = cargo_awu_by_rule(CARGO_BIN4, c4)
    st.caption(f"{c4_awu:.1f}")

# -------------------------
# CALCULATIONS
# -------------------------

zfw = (
    BOW
    + za + zb + zc
    + b1_awu + b2_awu + b3_awu + b4_awu
    + c1_awu + c2_awu + c3_awu + c4_awu
)

# -------------------------
# ZFW / FUEL + CG LIMITS
# -------------------------

col_left, col_right = st.columns(2)

# -------------------------
# LEFT: ZFW / FUEL
# -------------------------
with col_left:

    st.subheader("ZFW / Fuel")

    cols = st.columns(4)

    with cols[0]:
        ramp_fuel = st.number_input("Ramp Fuel", 0, value=None, key="ramp")
        taxi_fuel = st.number_input("Taxi Fuel", 0, value=None, key="taxi")

    # --- Calculations ---
    tof = (ramp_fuel - taxi_fuel) if (ramp_fuel is not None and taxi_fuel is not None) else 0.0
    takeoff_fuel_awu = fuel_awu_lookup(tof)

    zfw = (
        BOW
        + za + zb + zc
        + b1_awu + b2_awu + b3_awu + b4_awu
        + c1_awu + c2_awu + c3_awu + c4_awu
    )

    tow = zfw + takeoff_fuel_awu

    st.write(f"Takeoff Fuel: {tof:.1f}")

    # --- Summary ---
    st.markdown("**Summary**")

    label_width = 12
    num_width = 14

    st.text(f"{'ZFW:':<{label_width}}{zfw:>{num_width},.1f}")
    st.text(f"{'Fuel AWU:':<{label_width}}{takeoff_fuel_awu:>{num_width},.1f}")
    st.text(f"{'TOW:':<{label_width}}{tow:>{num_width},.1f}")


# -------------------------
# RIGHT: CG LIMITS
# -------------------------
with col_right:

    st.subheader("CG LIMITS")

    # --- ZFW LIMITS ---
    st.markdown("**ZFW Limits**")
    st.write("ZFW Forward Limit:")
    st.write("ZFW Aft Limit:")

    st.divider()

    # --- TOW LIMITS ---
    st.markdown("**TOW Limits**")
    st.write("TOW Forward Limit:")
    st.write("TOW Aft Limit:")
