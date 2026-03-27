import streamlit as st
import math
from docx import Document
from docx.shared import Pt

from docx import Document

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
