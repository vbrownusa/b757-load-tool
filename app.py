import streamlit as st
import pandas as pd


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
    a = int(st.number_input("Zone A Pax", 0, 54))
    za = pax_awu("A", a, season)
    st.caption(f"AWU: {za:.1f}")

with col2:
    b = int(st.number_input("Zone B Pax", 0, 80))
    zb = pax_awu("B", b, season)
    st.caption(f"AWU: {zb:.1f}")

with col3:
    c = int(st.number_input("Zone C Pax", 0, 84))
    zc = pax_awu("C", c, season)
    st.caption(f"AWU: {zc:.1f}")

# -------------------------
# BAGGAGE (simple for now)
# -------------------------




st.subheader("Baggage")



cols = st.columns(4)

with cols[0]:
    c1 = st.number_input("Bin 1", min_value=0, value=0)
    c1_awu = cargo_awu_by_rule(CARGO_BIN1, c1)
    st.caption(f"AWU: {c1_awu:.1f}")

with cols[1]:
    c2 = st.number_input("Bin 2", min_value=0, value=0)
    c2_awu = cargo_awu_by_rule(CARGO_BIN2, c2)
    st.caption(f"AWU: {c2_awu:.1f}")

with cols[2]:
    c3 = st.number_input("Bin 3", min_value=0, value=0)
    c3_awu = cargo_awu_by_rule(CARGO_BIN3, c3)
    st.caption(f"AWU: {c3_awu:.1f}")

with cols[3]:
    c4 = st.number_input("Bin 4", min_value=0, value=0)
    c4_awu = cargo_awu_by_rule(CARGO_BIN4, c4)
    st.caption(f"AWU: {c4_awu:.1f}")



# -------------------------
# CARGO (your rule)
# -------------------------


st.write("DEBUG: cargo section")






st.subheader("Cargo")


cols = st.columns(4)

# --- BIN 1 ---
with cols[0]:
    st.markdown("**Bin 1**")
    c1 = st.number_input("", min_value=0, value=0, key="cargo1")
    c1_awu = cargo_awu_by_rule(CARGO_BIN1, c1)
    st.caption(f"AWU: {c1_awu:.1f}")

# --- BIN 2 ---
with cols[1]:
    st.markdown("**Bin 2**")
    c2 = st.number_input("", min_value=0, value=0, key="cargo2")
    c2_awu = cargo_awu_by_rule(CARGO_BIN2, c2)
    st.caption(f"AWU: {c2_awu:.1f}")

# --- BIN 3 ---
with cols[2]:
    st.markdown("**Bin 3**")
    c3 = st.number_input("", min_value=0, value=0, key="cargo3")
    c3_awu = cargo_awu_by_rule(CARGO_BIN3, c3)
    st.caption(f"AWU: {c3_awu:.1f}")

# --- BIN 4 ---
with cols[3]:
    st.markdown("**Bin 4**")
    c4 = st.number_input("", min_value=0, value=0, key="cargo4")
    c4_awu = cargo_awu_by_rule(CARGO_BIN4, c4)
    st.caption(f"AWU: {c4_awu:.1f}")







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
c1_awu = cargo_awu_by_rule(CARGO_BIN1, c1)
st.caption(f"AWU: {c1_awu:.1f}")

c2 = st.number_input("Cargo Bin 2 (lbs)", 0)
c2_awu = cargo_awu_by_rule(CARGO_BIN2, c2)
st.caption(f"AWU: {c2_awu:.1f}")

c3 = st.number_input("Cargo Bin 3 (lbs)", 0)
c3_awu = cargo_awu_by_rule(CARGO_BIN3, c3)
st.caption(f"AWU: {c3_awu:.1f}")

c4 = st.number_input("Cargo Bin 4 (lbs)", 0)
c4_awu = cargo_awu_by_rule(CARGO_BIN4, c4)
st.caption(f"AWU: {c4_awu:.1f}")













# -------------------------
# TOTAL
# -------------------------

st.subheader("Passenger Total AWU")
st.write(round(za + zb + zc, 1))
