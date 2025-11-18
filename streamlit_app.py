import streamlit as st
import numpy as np
import json

from hardware.states import get_polarization_vector
from hardware.hwp import apply_hwp
from hardware.qwp import apply_qwp
from utils.plot_utils import polarization_ellipse_animation, polarization_ellipse_html
import streamlit.components.v1 as components


# Helper to safely request a rerun — some Streamlit builds don't expose experimental_rerun
def safe_rerun():
  try:
    if hasattr(st, "experimental_rerun"):
      st.experimental_rerun()
      return
  except Exception:
    pass
  # Fallback: toggle a dummy session_state key so the UI can react on next interaction
  st.session_state["_rerun_toggle"] = not st.session_state.get("_rerun_toggle", False)


st.set_page_config(layout="wide")
st.title("Waveplate Simulator")

# -----------------------------------------------------
# Sidebar Initialization
# -----------------------------------------------------
if "sequence" not in st.session_state:
    st.session_state.sequence = []

seq = st.session_state.sequence


# -----------------------------------------------------
# MAIN — Input Polarization (top)
# -----------------------------------------------------
st.subheader("Input Polarization")
pol = st.selectbox("Choose polarization", ["H", "V", "D", "A", "R", "L", "Custom"])

if pol == "Custom":
    pol_str = st.text_input("Enter Jones vector (e.g. 0.5+0.5j, 0.5-0.5j)")
    try:
        E_in = get_polarization_vector(pol_str)
    except Exception as e:
        st.error(f"Invalid custom Jones vector: {e}")
        st.stop()
else:
    E_in = get_polarization_vector(pol)

st.write("**Initial Jones Vector:**")
st.code(f"{E_in}")

# Waveplate controls (moved here per request)
st.markdown("**Waveplate Controls**")
cc1, cc2, cc3, cc4 = st.columns([1,1,1,2])

with cc1:
  if st.button("➕ Add HWP"):
    seq.append(("HWP", 0.0))
    st.session_state.sequence = seq
    safe_rerun()

with cc2:
  if st.button("➕ Add QWP"):
    seq.append(("QWP", 0.0))
    st.session_state.sequence = seq
    safe_rerun()

with cc3:
  if st.button("🗑️ Clear All"):
    st.session_state.sequence = []
    safe_rerun()

with cc4:
  remove_index = st.number_input(
    "Remove waveplate index (1-based)",
    min_value=1,
    max_value=len(seq) if len(seq) > 0 else 1,
    value=1,
    step=1,
  )
  if st.button("❌ Remove Selected"):
    if len(seq) > 0 and 1 <= remove_index <= len(seq):
      seq.pop(remove_index - 1)
      st.session_state.sequence = seq
      safe_rerun()

# -----------------------------------------------------
# Canvas Drag & Drop Editor (full width, below input)
# -----------------------------------------------------
st.subheader("Waveplate Canvas Editor")

# Build initial nodes with positions (spread horizontally)
initial_nodes = []
for i, (w, a) in enumerate(st.session_state.sequence):
    initial_nodes.append({
        "id": i,
        "type": w,
        "angle": float(a),
        "x": 120 + i * 180,
        "y": 120,
    })

init_json = json.dumps(initial_nodes)

# HTML + JS for canvas editor. Use a placeholder __INIT_JSON__ and replace it safely below.
editor_html = """
<style>
  .canvas-wrap { display:flex; gap:12px; }
  .editor-canvas { border:1px solid #ddd; background:#fff; }
  .tools { display:flex; flex-direction:column; gap:6px; }
  .tools button { padding:6px 10px; }
  .node-info { font-family: sans-serif; font-size:13px; }
</style>


<div class="canvas-wrap">
  <canvas id="wpCanvas" class="editor-canvas" width="900" height="300"></canvas>
  <div class="tools">
    <button id="addH">➕ Add HWP</button>
    <button id="addQ">➕ Add QWP</button>
    <div class="node-info" id="nodeInfo">Select a node to edit</div>
  </div>
</div>

<div id="popupEditor" style="display:none; position:absolute; background:#fffbe8; border:1px solid #ff8c00; border-radius:8px; padding:12px; z-index:10; box-shadow:0 2px 8px #888;">
  <div style="margin-bottom:8px;">
    <label>Type:
      <select id="popupTypeSelect">
        <option value="HWP">HWP</option>
        <option value="QWP">QWP</option>
      </select>
    </label>
  </div>
  <div style="margin-bottom:8px;">
    <label>Angle: <input id="popupAngleInput" type="number" step="0.1" style="width:90px"/></label>
  </div>
  <div style="display:flex; gap:8px;">
    <button id="popupApply">Apply</button>
    <button id="popupDelete">Delete</button>
    <button id="popupClose">Close</button>
  </div>
</div>

<script>
// placeholder; Python will inject JSON here
const initial = __INIT_JSON__;
console.log('[canvas] initial', initial);


const canvas = document.getElementById('wpCanvas');
const ctx = canvas.getContext('2d');
let nodes = (Array.isArray(initial) ? initial.slice() : []);
let dragging = null;
let offset = {x:0, y:0};
let selected = null;
const radius = 40;

// Popup editor elements
const popup = document.getElementById('popupEditor');
const popupType = document.getElementById('popupTypeSelect');
const popupAngle = document.getElementById('popupAngleInput');
const popupApply = document.getElementById('popupApply');
const popupDelete = document.getElementById('popupDelete');
const popupClose = document.getElementById('popupClose');

function draw() {
  ctx.clearRect(0,0,canvas.width, canvas.height);

  // draw connectors in sequence order (left-to-right ordering assumed)
  ctx.strokeStyle = '#888'; ctx.lineWidth = 2;
  for (let i=0;i<nodes.length-1;i++){
    const a = nodes[i]; const b = nodes[i+1];
    ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
  }

  nodes.forEach(n=>{
    // background
    if (selected && selected.id===n.id) {
      ctx.fillStyle = '#fffae6'; // light highlight
      ctx.strokeStyle = '#ff8c00'; // orange border
    } else {
      ctx.fillStyle = '#fff';
      ctx.strokeStyle = '#333';
    }
    ctx.lineWidth = (selected && selected.id===n.id)?3:1;
    ctx.fillRect(n.x-radius, n.y-20, radius*2, 40);
    ctx.strokeRect(n.x-radius, n.y-20, radius*2, 40);

    // label
    ctx.fillStyle = '#111'; ctx.font = '14px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(n.type + ' ('+n.angle+'°)', n.x, n.y);
  });
}

function sendValue(){
  try{ window.parent.postMessage({isStreamlitMessage:true, type:'streamlit:setComponentValue', value: JSON.stringify(nodes)}, '*'); }catch(e){console.error(e)}
}

function hitTest(x,y){
  for(let i=nodes.length-1;i>=0;i--){
    const n=nodes[i];
    if (x >= n.x - radius && x <= n.x + radius && y >= n.y-20 && y <= n.y+20) return n;
  }
  return null;
}


canvas.addEventListener('mousedown', (ev)=>{
  const rect = canvas.getBoundingClientRect();
  const x = ev.clientX - rect.left; const y = ev.clientY - rect.top;
  const h = hitTest(x,y);
  if (h){
    dragging = h; offset.x = x - h.x; offset.y = y - h.y; selected = h; updateInfo();
    showPopupEditor(h, rect.left + h.x, rect.top + h.y);
  } else {
    selected = null; updateInfo(); hidePopupEditor();
  }
  draw();
});

window.addEventListener('mousemove', (ev)=>{
  if (!dragging) return;
  const rect = canvas.getBoundingClientRect();
  const x = ev.clientX - rect.left; const y = ev.clientY - rect.top;
  dragging.x = Math.max(40, Math.min(canvas.width-40, x - offset.x));
  dragging.y = Math.max(20, Math.min(canvas.height-20, y - offset.y));
  draw();
});

window.addEventListener('mouseup', ()=>{ if (dragging){ sendValue(); dragging = null; } });


function updateInfo(){
  const info = document.getElementById('nodeInfo');
  if (selected){
    info.textContent = selected.type + ' #' + (nodes.indexOf(selected)+1);
  } else { info.textContent = 'Select a node to edit'; }
}

function showPopupEditor(node, px, py){
  popup.style.display = 'block';
  popupType.value = node.type;
  popupAngle.value = node.angle;
  // Position popup near node, but keep inside window
  let left = px + 50;
  let top = py - 20;
  if (left + 220 > window.innerWidth) left = window.innerWidth - 220;
  if (top < 10) top = 10;
  popup.style.left = left + 'px';
  popup.style.top = top + 'px';
}

function hidePopupEditor(){
  popup.style.display = 'none';
}


document.getElementById('addH').addEventListener('click', ()=>{ const id = Date.now(); nodes.push({id:id,type:'HWP',angle:0,x:120,y:120}); sendValue(); draw(); });
document.getElementById('addQ').addEventListener('click', ()=>{ const id = Date.now(); nodes.push({id:id,type:'QWP',angle:0,x:120,y:120}); sendValue(); draw(); });

// Popup editor actions
popupApply.addEventListener('click', ()=>{
  if (!selected) return;
  selected.angle = Number(popupAngle.value);
  selected.type = popupType.value;
  sendValue(); draw(); updateInfo(); hidePopupEditor();
});
popupDelete.addEventListener('click', ()=>{
  if (!selected) return;
  nodes = nodes.filter(n=>n.id!==selected.id);
  selected = null;
  sendValue(); updateInfo(); draw(); hidePopupEditor();
});
popupClose.addEventListener('click', ()=>{ hidePopupEditor(); });

popupType.addEventListener('change', (ev) => {
  if (!selected) return; selected.type = ev.target.value; sendValue(); draw(); updateInfo();
});

// initial draw + post
draw(); sendValue();

</script>
"""

# inject initial JSON safely
editor_html = editor_html.replace("__INIT_JSON__", init_json)

# Render the editor and capture posted JSON
ret = components.html(editor_html, height=420)

# If the component returned a JSON string or a list/dict, update session state sequence
if ret is not None:
  try:
    parsed = None
    if isinstance(ret, str):
      parsed = json.loads(ret)
    elif isinstance(ret, (list, dict)):
      parsed = ret

    if parsed is not None:
      # convert to sequence order by sorting nodes left-to-right (x)
      parsed_sorted = sorted(parsed, key=lambda n: n.get('x', 0))
      st.session_state.sequence = [(n.get('type'), float(n.get('angle', 0))) for n in parsed_sorted]
  except Exception as e:
    st.warning(f"Could not parse canvas editor output: {e}")

# Ensure local seq reflects session state
seq = st.session_state.sequence

# -----------------------------------------------------
# Edit Waveplate (Streamlit-based panel)
# -----------------------------------------------------


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
    
