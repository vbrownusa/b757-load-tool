import streamlit as st
from docx import Document

import streamlit as st
from docx import Document

# -------------------------
# ✅ ADD TABLES HERE (TOP LEVEL)
# -------------------------

ZONE_A = { ... }
ZONE_B = { ... }
ZONE_C = { ... }

# -------------------------
# FUNCTIONS
# -------------------------

def pax_awu(zone_dict, pax, season):
    if pax == 0:
        return 0
    return zone_dict[pax][0] if season == "summer" else zone_dict[pax][1]

def generate_release(data):
    ...
    
# -------------------------
# UI (BOTTOM)
# -------------------------

st.title("B757 Dispatch Tool")

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

st.title("Test App")

data = {
    "zoneA": 1000,
    "zoneB": 2000,
    "zoneC": 3000,
    "bag1": 100,
    "bag2": 200,
    "bag3": 300,
    "bag4": 400,
    "cargo_vals": [100, 200, 300, 400]
}

if st.button("Generate"):
    file = generate_release(data)
    with open(file, "rb") as f:
        st.download_button("Download", f, file_name=file)
