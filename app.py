import streamlit as st
import pandas as pd
import math

st.set_page_config(layout="wide")

# -------------------------
# CONSTANTS
# -------------------------

BOW = 129614.1

# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data
def load_pax_data():
    return pd.read_csv("pax_data.csv")


@st.cache_data
def load_fuel_data():
    df = pd.read_csv("fuel_data.csv")

    # Flatten entire dataframe (handles multi-column OCR mess)
    df = df.stack().reset_index(drop=True)

    # Convert to numeric, drop junk
    df = pd.to_numeric(df, errors="coerce")
    df = df.dropna().reset_index(drop=True)

    # Ensure even number of rows
    if len(df) % 2 != 0:
        df = df.iloc[:-1]

    # Rebuild clean pairs
    fuel_df = pd.DataFrame({
        "weight": df.iloc[::2].values,
        "awu": df.iloc[1::2].values
    })

    # Final type enforcement
    fuel_df["weight"] = fuel_df["weight"].astype(int)
    fuel_df["awu"] = fuel_df["awu"].astype(float)

    return fuel_df


pax_df = load_pax_data()
fuel_df = load_fuel_data()

# -------------------------
# CG LIMIT TABLE
# -------------------------

CG_LIMITS = {
    150: (12.9, 32.0), 155: (12.6, 32.5), 160: (12.3, 32.9),
    165: (12.0, 33.4), 170: (11.7, 33.9), 175: (11.4, 34.3),
    180: (11.2, 34.8), 185: (10.9, 35.3), 190: (10.6, 35.8),
    195: (10.3, 36.2), 200: (10.0, 36.7), 205: (9.7, 37.2),
    210: (9.4, 37.6), 216: (9.1, 38.2), 221: (8.8, 37.8),
    226: (8.8, 37.4), 231: (8.9, 37.0), 233: (9.2, 36.8),
    234: (9.4, 35.1), 235: (9.5, 33.4), 236: (9.7, 31.6),
    237: (9.8, 29.9), 238: (10.0, 28.2), 239: (10.2, 26.4),
    240: (10.3, 24.7), 241: (10.4, 23.0),
}

# -------------------------
# FUNCTIONS
# -------------------------

def pax_awu(zone, pax, season):
    if pax is None:
        return 0.0
    row = pax_df[(pax_df["zone"] == zone) & (pax_df["pax"] == pax)]
    return float(row.iloc[0][season]) if not row.empty else 0.0


def bag_awu(count):
    return 0.0 if count is None else count * 32.0


def cargo_awu_by_rule(table, weight):
    if weight is None:
        return 0.0
    for awu in sorted(table.values()):
        equiv = int(awu) - (int(awu) % 100)
        if weight <= equiv:
            return awu
    return max(table.values())


def fuel_awu_lookup(weight):
    if weight is None or weight <= 0:
        return 0.0

    rounded = int(math.ceil(weight / 100.0) * 100)

    row = fuel_df[fuel_df["weight"] == rounded]
    if not row.empty:
        return float(row.iloc[0]["awu"])

    higher = fuel_df[fuel_df["weight"] > rounded]
    return float(higher.iloc[0]["awu"]) if not higher.empty else float(fuel_df.iloc[-1]["awu"])


def interpolate_limits(weight_k):
    keys = sorted(CG_LIMITS.keys())

    if weight_k <= keys[0]:
        return CG_LIMITS[keys[0]]
    if weight_k >= keys[-1]:
        return CG_LIMITS[keys[-1]]

    for i in range(len(keys) - 1):
        w1, w2 = keys[i], keys[i + 1]
        if w1 <= weight_k <= w2:
            f1, a1 = CG_LIMITS[w1]
            f2, a2 = CG_LIMITS[w2]
            r = (weight_k - w1) / (w2 - w1)
            return f1 + r*(f2-f1), a1 + r*(a2-a1)


def cg_status(cg, fwd, aft):
    if cg < fwd:
        return "OUTSIDE (FWD)", "red"
    elif cg > aft:
        return "OUTSIDE (AFT)", "red"
    return "WITHIN LIMITS", "green"

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
    a = st.number_input("Zone A Pax", 0, 54, value=None, placeholder="Enter")
    za = pax_awu("A", a, season)

with col2:
    b = st.number_input("Zone B Pax", 0, 80, value=None, placeholder="Enter")
    zb = pax_awu("B", b, season)

with col3:
    c = st.number_input("Zone C Pax", 0, 84, value=None, placeholder="Enter")
    zc = pax_awu("C", c, season)

# -------------------------
# BAGGAGE
# -------------------------

st.subheader("Baggage")

bags = []
cols = st.columns(4)

for i in range(4):
    with cols[i]:
        val = st.number_input(f"Bin {i+1}", 0, value=None, placeholder="Enter")
        bags.append(bag_awu(val))

# -------------------------
# CARGO
# -------------------------

CARGO_BIN = {
    200: 299.6, 300: 499.4, 400: 699.1,
    500: 898.9, 600: 1098.7, 700: 1298.2,
    800: 1498.0, 900: 1697.8, 1000: 1897.5,
}

st.subheader("Cargo")

cargo_vals = []
cols = st.columns(4)

for i in range(4):
    with cols[i]:
        val = st.number_input(f"Bin {i+1}", 0, value=None, key=f"cargo{i}", placeholder="Enter")
        cargo_vals.append(cargo_awu_by_rule(CARGO_BIN, val))

# -------------------------
# CALCULATIONS
# -------------------------

zfw = BOW + za + zb + zc + sum(bags) + sum(cargo_vals)

# -------------------------
# FUEL
# -------------------------

st.subheader("Fuel")

col1, col2 = st.columns(2)

with col1:
    ramp = st.number_input("Ramp Fuel", min_value=0, value=None, placeholder="Enter ramp fuel")
    taxi = st.number_input("Taxi Fuel", min_value=0, value=None, placeholder="Enter taxi fuel")

tof = ramp - taxi if (ramp is not None and taxi is not None) else None
fuel_awu = fuel_awu_lookup(tof) if tof is not None else 0.0
tow = zfw + fuel_awu

# -------------------------
# CG
# -------------------------

zfw_k = zfw / 1000
tow_k = tow / 1000

zfw_cg = zfw % 100
tow_cg = tow % 100

zfw_fwd, zfw_aft = interpolate_limits(zfw_k)
tow_fwd, tow_aft = interpolate_limits(tow_k)

zfw_status, zfw_color = cg_status(zfw_cg, zfw_fwd, zfw_aft)
tow_status, tow_color = cg_status(tow_cg, tow_fwd, tow_aft)

# -------------------------
# DISPLAY
# -------------------------

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### CG Limits")

    st.markdown(
        f"""
        <div style="font-family:monospace; line-height:1.0">

        <b>ZFW</b><br>
        CG: {zfw_cg:6.1f}
        <span style="color:{zfw_color}; font-weight:bold;
        background-color:{'#e6ffe6' if zfw_color=='green' else '#ffe6e6'};
        padding:2px 6px; border-radius:4px;">
        {zfw_status}
        </span><br>
        Limits: {zfw_fwd:.1f} - {zfw_aft:.1f}<br><br>

        <b>TOW</b><br>
        CG: {tow_cg:6.1f}
        <span style="color:{tow_color}; font-weight:bold;
        background-color:{'#e6ffe6' if tow_color=='green' else '#ffe6e6'};
        padding:2px 6px; border-radius:4px;">
        {tow_status}
        </span><br>
        Limits: {tow_fwd:.1f} - {tow_aft:.1f}

        </div>
        """,
        unsafe_allow_html=True
    )

with col_right:
    st.markdown("### Summary")

    label_width = 10
    num_width = 15

    st.markdown(
        f"""
        <div style="font-family:monospace; line-height:1.0">

        {'ZFW:':<{label_width}}{zfw:>{num_width},.1f}<br>
        {'Fuel:':<{label_width}}{fuel_awu:>{num_width},.1f}<br>
        {'TOW:':<{label_width}}{tow:>{num_width},.1f}

        </div>
        """,
        unsafe_allow_html=True
    )
