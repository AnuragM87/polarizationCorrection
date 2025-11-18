# import streamlit as st
# import numpy as np
# from hardware.hwp import get_polarization_vector, apply_hwp, jones_to_stokes
# from plot_utils import plot_poincare

# st.title("Polarization Simulator: HWP + QWP")

# st.sidebar.header("Controls")

# # Choose plate type (HWP or QWP)
# plate_type = st.sidebar.radio("Select Waveplate:", ["Half-Wave Plate (HWP)", "Quarter-Wave Plate (QWP)"])

# # Choose input polarization
# pol = st.sidebar.selectbox("Input Polarization", ["H", "V", "D", "A", "R", "L"])
# if plate_type == "Half-Wave Plate (HWP)":
#     E_out = apply_hwp(E_in, angle)
# # else:
# #     E_out = apply_qwp_pdf(E_in, angle)

# pol = st.selectbox("Input Polarization", ["H", "V", "D", "A", "R", "L"])
# angle = st.number_input("HWP Orientation (degrees)", 0.0, 180.0, 0.0, 0.5)

# E_in = get_polarization_vector(pol)
# E_out = apply_hwp(E_in, angle)

# st.write("### Input Jones Vector")
# # st.write(E_in)
# st.code(f"{E_in}", language="text")

# st.write("### Output Jones Vector")
# # st.write(E_out)
# st.code(f"{E_out}", language="text")



# # S_in = jones_to_stokes(E_in)
# # S_out = jones_to_stokes(E_out)

# # fname = plot_poincare(S_in, S_out, "poincare_plot.png")

# # st.image("poincare_plot.png", caption="Poincaré Sphere Plot")
import streamlit as st
# import numpy as np
# from hardware.hwp import get_polarization_vector, apply_hwp, jones_to_stokes
# from hardware.qwp import apply_qwp_pdf   # your QWP (PDF formula) function
# from plot_utils import plot_poincare

# # ------------------------------------------------------
# # Sidebar (LEFT) — BUTTONS
# # ------------------------------------------------------
# st.sidebar.title("Waveplate Menu")

# mode = st.sidebar.radio(
#     "Select Mode",
#     ["Half Wave Plate (HWP)", "Quarter Wave Plate (QWP)"]
# )

# # ------------------------------------------------------
# # Main Page (RIGHT SIDE)
# # ------------------------------------------------------
# st.title("Waveplate Simulator")

# # Inputs on RIGHT SIDE
# col1, col2 = st.columns(2)

# with col1:
#     pol = st.selectbox("Input Polarization", ["H", "V", "D", "A", "R", "L"])

# with col2:
#     angle = st.number_input(
#         "Orientation (degrees)", 
#         min_value=0.0, 
#         max_value=180.0, 
#         value=0.0, 
#         step=0.5
#     )

# E_in = get_polarization_vector(pol)

# # ------------------------------------------------------
# # Run Depending on Button Pressed
# # ------------------------------------------------------
# if st.sidebar.button("Run Waveplate"):

#     if mode == "Half Wave Plate (HWP)":
#         E_out = apply_hwp(E_in, angle)

#     elif mode == "Quarter Wave Plate (QWP)":
#         E_out = apply_qwp_pdf(E_in, angle)

#     # --------- DISPLAY RESULTS (right side) ----------
#     st.subheader("Input Jones Vector")
#     st.code(f"{E_in}", language="text")

#     st.subheader("Output Jones Vector")
#     st.code(f"{E_out}", language="text")

#     # Stokes + Poincare
#     S_in = jones_to_stokes(E_in)
#     S_out = jones_to_stokes(E_out)

#     fname = plot_poincare(S_in, S_out, "poincare_plot.png")
#     st.image("poincare_plot.png", caption="Poincaré Sphere Plot")


import streamlit as st
import numpy as np

from hardware.states import get_polarization_vector
from hardware.hwp import apply_hwp
from hardware.qwp import apply_qwp


st.set_page_config(layout="wide")
st.title("Waveplate  Simulator")


# -----------------------------------------
# LEFT SIDE — Sidebar controls
# -----------------------------------------
st.sidebar.header("Add Waveplates to Sequence")

sequence = st.session_state.get("sequence", [])

if st.sidebar.button("➕ Add HWP"):
    sequence.append(("HWP", 0))
    st.session_state.sequence = sequence

if st.sidebar.button("➕ Add QWP"):
    sequence.append(("QWP", 0))
    st.session_state.sequence = sequence

if st.sidebar.button("🗑️ Clear Sequence"):
    st.session_state.sequence = []


# -----------------------------------------
# RIGHT SIDE — Main control panel
# -----------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Polarization")
    pol = st.selectbox("Choose polarization", ["H", "V", "D", "A", "R", "L", "Custom"])
    if pol == "Custom":
        pol_str = st.text_input("Enter Jones vector (a,b)", "0.5+0.5j, 0.5-0.5j")
        E_in = get_polarization_vector(pol_str)
    else:
        E_in = get_polarization_vector(pol)

with col2:
    st.subheader("Waveplate Sequence Editor")

    if "sequence" not in st.session_state:
        st.session_state.sequence = []

    seq = st.session_state.sequence

    for i, (wtype, angle) in enumerate(seq):
        st.write(f"**{wtype} #{i+1}**")
        new_angle = st.number_input(f"Angle for {wtype} #{i+1}", 
                                    value=float(angle), key=f"ang{i}")
        seq[i] = (wtype, new_angle)

# -----------------------------------------
# APPLY WAVEPLATE SEQUENCE
# -----------------------------------------
E = E_in.copy()

for wtype, angle in seq:
    if wtype == "HWP":
        E = apply_hwp(E, angle)
    elif wtype == "QWP":
        E = apply_qwp(E, angle)

# -----------------------------------------
# DISPLAY OUTPUT
# -----------------------------------------
st.subheader("Final Output Jones Vector")
st.code(f"{E}", language="text")

st.subheader("Waveplate Chain Used")
for w, ang in seq:
    st.write(f"- {w} @ {ang}°")

