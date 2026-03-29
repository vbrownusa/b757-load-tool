import streamlit as st
import pandas as pd

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
    return int(count) * 32.0  # placeholder


def cargo_awu_by_rule(table, weight):
    if weight is None or weight <= 0:
        return 0.0

    weight = int(weight)

    awu_values = sorted(table.values())

    for awu in awu_values:
        equiv_lbs = int(awu) - (int(awu) % 100)

        if weight <= equiv_lbs:
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
# ZFW + FUEL
# -------------------------

st.subheader("TOTALS")

col1, col2 = st.columns(2)

# --- ZFW (left) ---
with col1:
    st.write(f"ZFW: {zfw:.1f}")

# --- Fuel (right, stacked) ---
with col2:
    ramp_fuel = st.number_input("Ramp Fuel", 0, value=None, key="ramp")
    taxi_fuel = st.number_input("Taxi Fuel", 0, value=None, key="taxi")

    tof = (ramp_fuel - taxi_fuel) if (ramp_fuel is not None and taxi_fuel is not None) else 0.0

    st.write(f"Takeoff Fuel: {tof:.1f}")
st.write(f"Takeoff Fuel: {tof:.1f}")
