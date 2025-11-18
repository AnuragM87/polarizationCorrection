import streamlit as st
import numpy as np

from hardware.states import get_polarization_vector
from hardware.hwp import apply_hwp
from hardware.qwp import apply_qwp
from utils.plot_utils import polarization_ellipse_animation, polarization_ellipse_html
import streamlit.components.v1 as components


st.set_page_config(layout="wide")
st.title("Waveplate Simulator")

# -----------------------------------------------------
# Sidebar Initialization
# -----------------------------------------------------
if "sequence" not in st.session_state:
    st.session_state.sequence = []

seq = st.session_state.sequence

st.sidebar.header("Waveplate Controls")

# Add buttons
if st.sidebar.button("➕ Add HWP"):
    seq.append(("HWP", 0.0))
    st.session_state.sequence = seq

if st.sidebar.button("➕ Add QWP"):
    seq.append(("QWP", 0.0))
    st.session_state.sequence = seq

# Remove waveplate button
remove_index = st.sidebar.number_input(
    "Remove waveplate index (1-based)", 
    min_value=1, 
    max_value=len(seq) if len(seq) > 0 else 1, 
    value=1
)

if st.sidebar.button("❌ Remove Selected"):
    if len(seq) > 0:
        seq.pop(remove_index - 1)
        st.session_state.sequence = seq

# Clear all waveplates
if st.sidebar.button("🗑️ Clear All"):
    st.session_state.sequence = []


# -----------------------------------------------------
# MAIN AREA — Two Columns
# -----------------------------------------------------
col1, col2 = st.columns(2)

# -----------------------------------------------------
# LEFT COLUMN — Input Polarization
# -----------------------------------------------------
with col1:
    st.subheader("Input Polarization")
    pol = st.selectbox("Choose polarization", ["H", "V", "D", "A", "R", "L", "Custom"])

    if pol == "Custom":
        pol_str = st.text_input("Enter Jones vector (e.g. 0.5+0.5j, 0.5-0.5j)")
        E_in = get_polarization_vector(pol_str)
    else:
        E_in = get_polarization_vector(pol)

    st.write("**Initial Jones Vector:**")
    st.code(f"{E_in}")


# -----------------------------------------------------
# RIGHT COLUMN — Waveplate Editor
# -----------------------------------------------------
with col2:
    st.subheader("Waveplate Sequence Editor")

    seq = st.session_state.sequence

    for i, (wtype, angle) in enumerate(seq):
        st.write(f"### {wtype} #{i+1}")

        new_angle = st.number_input(
            f"Angle for {wtype} #{i+1}",
            value=float(angle),
            key=f"ang{i}"
        )

        seq[i] = (wtype, new_angle)

    st.session_state.sequence = seq


# -----------------------------------------------------
# APPLY SEQUENCE
# -----------------------------------------------------
E = E_in.copy()

for wtype, angle in seq:
    if wtype == "HWP":
        E = apply_hwp(E, angle)
    elif wtype == "QWP":
        E = apply_qwp(E, angle)


# -----------------------------------------------------
# OUTPUT
# -----------------------------------------------------
st.subheader("Final Output Jones Vector")
st.code(f"{E}")

st.subheader("Waveplate Chain Used")
if len(seq) == 0:
    st.write("_No waveplates added_")
else:
    for w, ang in seq:
        st.write(f"- {w} @ {ang}°")


# -----------------------------------------------------
# POLARIZATION ELLIPSE ANIMATION
# -----------------------------------------------------
st.subheader("Polarization Ellipse Animation")

# Let user choose animation mode. Default to client-side HTML canvas (fast).
anim_mode = st.selectbox("Animation type", ["HTML Canvas (fast)", "GIF (server-side)"])

try:
    if anim_mode == "HTML Canvas (fast)":
        html = polarization_ellipse_html(E, width=420, height=420)
        components.html(html, height=460)
    else:
        # fallback: generate server-side GIF (may be slow)
        ell_file = polarization_ellipse_animation(E, "ellipse.gif")
        st.image(ell_file, caption="Polarization Ellipse")
except Exception as e:
    st.error(f"Ellipse generation error: {e}")
