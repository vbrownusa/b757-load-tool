import streamlit as st
import pandas as pd


# -------------------------
# LOAD PASSENGER DATA
# -------------------------


@st.cache_data
def load_pax_data():
    df = pd.read_csv("pax_data.csv")

    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna()

    df["zone"] = df["zone"].astype(str).str.strip().str.upper()
    df["pax"] = df["pax"].astype(int)

    return df

pax_df = load_pax_data()


# -------------------------
# PASSENGER AWU
# -------------------------


def pax_awu(df, zone, pax, season):
    if pax == 0:
        return 0.0

    row = df[(df["zone"] == zone) & (df["pax"] == pax)]

    if row.empty:
        st.error(f"Missing AWU data for Zone {zone}, Pax {pax}")
        return 0.0

    return float(row.iloc[0][season])


# -------------------------
# BAG AWU (SIMPLE FOR NOW)
# -------------------------


def bag_awu(count):
    return count * 32.0


# -------------------------
# CARGO AWU (YOUR RULE)
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
# UI
# -------------------------


st.title("B757 Dispatch Tool")

season = st.radio("Season", ["summer", "winter"], horizontal=True)

col1, col2, col3 = st.columns(3)

with col1:
    a = int(st.number_input("Zone A", 0, 54))
    b = int(st.number_input("Zone B", 0, 80))
    c = int(st.number_input("Zone C", 0, 84))

with col2:
    b1 = st.number_input("Bin 1 Bags", 0)
    b2 = st.number_input("Bin 2 Bags", 0)
    b3 = st.number_input("Bin 3 Bags", 0)
    b4 = st.number_input("Bin 4 Bags", 0)

with col3:
    c1 = st.number_input("Cargo Bin 1", 0)
    c2 = st.number_input("Cargo Bin 2", 0)
    c3 = st.number_input("Cargo Bin 3", 0)
    c4 = st.number_input("Cargo Bin 4", 0)

rf = st.number_input("Ramp Fuel", 0)
tf = st.number_input("Taxi Fuel", 0)


# -------------------------
# CALCULATIONS
# -------------------------


BOW = 129621.4

za = pax_awu(pax_df, "A", a, season)
zb = pax_awu(pax_df, "B", b, season)
zc = pax_awu(pax_df, "C", c, season)

bag_awus = [
    bag_awu(b1),
    bag_awu(b2),
    bag_awu(b3),
    bag_awu(b4),
]

cargo_awus = [
    cargo_awu_by_rule(CARGO_BIN1, c1),
    cargo_awu_by_rule(CARGO_BIN1, c2),
    cargo_awu_by_rule(CARGO_BIN1, c3),
    cargo_awu_by_rule(CARGO_BIN1, c4),
]

zfw = BOW + za + zb + zc + sum(bag_awus) + sum(cargo_awus)


# -------------------------
# OUTPUT
# -------------------------


st.subheader("ZFW")
st.write(round(zfw, 1))

st.subheader("Passenger AWU")
st.write(f"A: {a} → {za:.1f}")
st.write(f"B: {b} → {zb:.1f}")
st.write(f"C: {c} → {zc:.1f}")

st.subheader("Baggage AWU")
st.write(f"Bin1: {b1} → {bag_awus[0]:.1f}")
st.write(f"Bin2: {b2} → {bag_awus[1]:.1f}")
st.write(f"Bin3: {b3} → {bag_awus[2]:.1f}")
st.write(f"Bin4: {b4} → {bag_awus[3]:.1f}")

st.subheader("Cargo AWU")
st.write(f"Bin1: {c1} → {cargo_awus[0]:.1f}")
st.write(f"Bin2: {c2} → {cargo_awus[1]:.1f}")
st.write(f"Bin3: {c3} → {cargo_awus[2]:.1f}")
st.write(f"Bin4: {c4} → {cargo_awus[3]:.1f}")
