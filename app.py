import streamlit as st
import requests
import pandas as pd
import datetime
import pydeck as pdk
import streamlit.components.v1 as components
import math

st.set_page_config(
    page_title="🦅 AMERICA'S #1 NYC TAXI 🦅",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@400;700&display=swap');

/* TIMES SQUARE BACKGROUND — year 2000 vibe, low opacity */
.stApp {
    background-image:
        linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)),
        url('https://upload.wikimedia.org/wikipedia/commons/3/39/NYC_-_Times_Square.JPG');
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    background-color: #ffffff;
}

/* MAIN CONTAINER */
.main .block-container {
    background: #ffffff;
    border-radius: 25px;
    border: 5px solid #B22234;
    padding: 2rem 3rem;
    max-width: 1400px;
    box-shadow:
        0 0 0 8px #3C3B6E,
        0 8px 40px rgba(0,0,0,0.15);
}

/* TITLE */
h1 {
    font-family: 'Bebas Neue', 'Impact', 'Arial Black', sans-serif !important;
    font-size: 4.2rem !important;
    background: linear-gradient(90deg, #B22234, #3C3B6E, #B22234, #3C3B6E, #B22234) !important;
    background-size: 300% 300% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-align: center !important;
    letter-spacing: 7px !important;
    animation: gradient-shift 4s ease infinite !important;
    line-height: 1.1 !important;
}

@keyframes gradient-shift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* H2 / H3 */
h2, h3 {
    font-family: 'Oswald', 'Impact', sans-serif !important;
    color: #B22234 !important;
    letter-spacing: 5px !important;
    text-transform: uppercase !important;
}

h3 { color: #3C3B6E !important; font-size: 1.1rem !important; }

/* LABELS / TEXT */
label, p, li, .stMarkdown p {
    color: #1a1a1a !important;
    font-family: 'Oswald', 'Arial', sans-serif !important;
}

/* ALL INPUTS */
input[type="number"], input[type="text"], input[type="time"], input[type="date"] {
    background: #f8f8ff !important;
    color: #1a1a1a !important;
    border: 2px solid #3C3B6E !important;
    border-radius: 8px !important;
    font-family: 'Oswald', monospace !important;
    font-size: 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input:focus {
    border-color: #B22234 !important;
    box-shadow: 0 0 10px rgba(178,34,52,0.3) !important;
    outline: none !important;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #B22234, #3C3B6E, #B22234, #3C3B6E, #B22234) !important;
    background-size: 300% 300% !important;
    color: #fff !important;
    font-family: 'Bebas Neue', 'Impact', 'Arial Black', sans-serif !important;
    font-size: 2.4rem !important;
    letter-spacing: 7px !important;
    border: 3px solid #FFD700 !important;
    border-radius: 18px !important;
    padding: 22px 0 !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(178,34,52,0.5) !important;
    animation: btn-glow 1.8s ease infinite alternate, gradient-shift 3s ease infinite !important;
    transition: transform 0.1s !important;
    cursor: pointer !important;
}
@keyframes btn-glow {
    from { box-shadow: 0 4px 15px rgba(178,34,52,0.4); }
    to   { box-shadow: 0 4px 40px rgba(178,34,52,0.9), 0 0 60px rgba(60,59,110,0.5); }
}
.stButton > button:hover  { transform: scale(1.03) !important; }
.stButton > button:active { transform: scale(0.97) !important; }

/* METRICS */
[data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', Impact, sans-serif !important;
    font-size: 3.5rem !important;
    color: #B22234 !important;
}
[data-testid="stMetricLabel"] {
    color: #3C3B6E !important;
    font-family: 'Oswald', sans-serif !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
}

/* COLUMNS */
[data-testid="column"] {
    background: #f4f4ff;
    border-radius: 15px;
    border: 1px solid rgba(60,59,110,0.3);
    padding: 15px !important;
}

/* SPINNER */
.stSpinner > div { border-color: #B22234 transparent #B22234 transparent !important; }

/* HIDE STREAMLIT CHROME */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* SCROLLBAR */
::-webkit-scrollbar       { width: 8px; }
::-webkit-scrollbar-track { background: #f0f0f0; }
::-webkit-scrollbar-thumb { background: #B22234; border-radius: 4px; }

/* NUMBER INPUT STEPPERS */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: #f0f0ff !important;
    color: #3C3B6E !important;
    border: 1px solid #3C3B6E !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── AUDIO: Eagle screech synthesised via Web Audio API ──────────────────────
AUDIO_COMPONENT = """
<script>
(function() {
    var played = false;
    function eagleScreech() {
        if (played) return;
        played = true;
        try {
            var AC = window.AudioContext || window.webkitAudioContext;
            var ctx = new AC();
            var t = ctx.currentTime;

            var osc = ctx.createOscillator();
            var g   = ctx.createGain();
            osc.connect(g); g.connect(ctx.destination);
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(1100, t);
            osc.frequency.exponentialRampToValueAtTime(550, t + 0.35);
            osc.frequency.exponentialRampToValueAtTime(1350, t + 0.70);
            osc.frequency.exponentialRampToValueAtTime(350,  t + 1.10);
            g.gain.setValueAtTime(0.18, t);
            g.gain.exponentialRampToValueAtTime(0.001, t + 1.1);
            osc.start(t); osc.stop(t + 1.1);

            var boom = ctx.createOscillator();
            var gb   = ctx.createGain();
            boom.connect(gb); gb.connect(ctx.destination);
            boom.type = 'square';
            boom.frequency.setValueAtTime(65, t + 1.0);
            gb.gain.setValueAtTime(0.35, t + 1.0);
            gb.gain.exponentialRampToValueAtTime(0.001, t + 1.5);
            boom.start(t + 1.0); boom.stop(t + 1.5);
        } catch(e) {}
    }
    document.addEventListener('click', eagleScreech, { once: true });
    setTimeout(eagleScreech, 300);
})();
</script>
"""
components.html(AUDIO_COMPONENT, height=0)

# ── WAITING: NYC street ambiance (plays while API loads) ────────────────────
AMBIENT_JS = """
<script>
(function() {
    var a = new Audio('https://soundbible.com/grab.php?id=298&type=mp3');
    a.volume = 0.35;
    a.loop   = true;
    a.play().catch(function(){});
    window._taxiAmbient = a;

    /* Explosion boom via Web Audio API */
    try {
        var AC = window.AudioContext || window.webkitAudioContext;
        var ctx = new AC();
        var sr  = ctx.sampleRate;
        var buf  = ctx.createBuffer(1, sr * 0.55, sr);
        var data = buf.getChannelData(0);
        for (var i = 0; i < data.length; i++) {
            data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (sr * 0.12));
        }
        var src = ctx.createBufferSource();
        src.buffer = buf;
        var gn = ctx.createGain();
        gn.gain.setValueAtTime(0.6, ctx.currentTime);
        gn.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.55);
        src.connect(gn); gn.connect(ctx.destination);
        src.start();
    } catch(e) {}
})();
</script>
"""

# ── RESULT: America Fuck Yeah plays on success ──────────────────────────────
AMERICA_JS = """
<script>
(function() {
    /* Stop ambient if still running */
    if (window.parent && window.parent._taxiAmbient) {
        try { window.parent._taxiAmbient.pause(); } catch(e) {}
    }
    var music = new Audio('https://archive.org/download/AMERICAFKYEAHMUSICVIDEOTeamAmericaWorldPoliceTHEMESONG/AMERICA%20F-%23K%20YEAH%21%20MUSIC%20VIDEO%20-%20Team%20America%20World%20Police%20THEME%20SONG.mp3');
    music.volume = 0.85;
    music.play().catch(function(){});
})();
</script>
"""

# ════════════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@keyframes floatL { from { transform: translateY(0) rotate(-8deg); } to { transform: translateY(-14px) rotate(8deg); } }
@keyframes floatR { from { transform: translateY(-14px) rotate(8deg); } to { transform: translateY(0) rotate(-8deg); } }
@keyframes explode { from { transform: scale(1); } to { transform: scale(1.06); } }
.eagle-l { display:inline-block; animation: floatL 1.8s ease-in-out infinite alternate; font-size:4rem; }
.eagle-r { display:inline-block; animation: floatR 1.8s ease-in-out infinite alternate; font-size:4rem; }
.boom-row { animation: explode 0.7s ease-in-out infinite alternate; display:inline-block; }
</style>

<div style="text-align:center; padding:18px 0 6px;">
    <span class="eagle-l">🦅</span>
    <h1>AMERICA'S #1 NYC TAXI FARE CALCULATOR</h1>
    <span class="eagle-r">🦅</span>
</div>

<div style="text-align:center; color:#3C3B6E; font-family:'Oswald',sans-serif; font-size:1.35rem; letter-spacing:5px; margin:6px 0;">
    🇺🇸 THE GREATEST · THE BOLDEST · THE MOST POWERFUL TAXI CALC IN THE KNOWN UNIVERSE 🇺🇸
</div>

<div style="text-align:center; margin:8px 0;">
    <span class="boom-row" style="font-size:2.4rem;">💥 🚕 🗽 🚁 ✈️ 🦅 ✈️ 🚁 🗽 🚕 💥</span>
</div>

<div style="text-align:center; color:#B22234; font-size:1.3rem; letter-spacing:3px; margin:4px 0;">
    ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★
</div>
""", unsafe_allow_html=True)

# NYC TAXI ASCII BANNER
st.markdown("""
<div style="
    text-align:center;
    background: linear-gradient(135deg, rgba(178,34,52,0.08), rgba(60,59,110,0.1));
    border: 2px solid #B22234;
    border-radius: 15px;
    padding: 16px;
    margin: 10px 0;
    font-family: monospace;
">
<pre style="color:#B22234; display:inline-block; text-align:left; font-size:0.95rem; line-height:1.35; margin:0;">
  ╔═══════════════════════════════════════════╗
  ║   ___   _   _  _    _  ___  _   _  ___   ║
  ║  |_ _| | | | || |  | |/ _ \| | | ||_ _|  ║
  ║   | |  | |_| || |__| | (_) | |_| | | |   ║
  ║  |___|  \___/ |______|\___ / \___/ |___|  ║
  ║        NYC  🚕  TAXI  🚕  CAB            ║
  ╚═══════════════════════════════════════════╝</pre>
<div style="font-size:1.8rem; margin-top:6px;">🌆 🗽 🌉 🏙️ 🌆 🗽 🌉 🏙️ 🌆 🗽 🌉</div>
</div>
""", unsafe_allow_html=True)

# NYC TAXI GIFs
st.markdown("""
<div style="display:flex; justify-content:center; align-items:center; gap:18px; flex-wrap:wrap; margin:16px 0;">
    <img src="https://media.giphy.com/media/93nb6Zt16rwjGk2Y8O/giphy.gif"
         height="180" style="border-radius:12px; border:4px solid #B22234; box-shadow:0 4px 20px rgba(178,34,52,0.4);">
    <img src="https://media.giphy.com/media/Y70DOxH0fpUHBtOCiF/giphy.gif"
         height="180" style="border-radius:12px; border:4px solid #3C3B6E; box-shadow:0 4px 20px rgba(60,59,110,0.4);">
    <img src="https://media.giphy.com/media/Z9lNKlUpafy9uWELmz/giphy.gif"
         height="180" style="border-radius:12px; border:4px solid #B22234; box-shadow:0 4px 20px rgba(178,34,52,0.4);">
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════════
#  INPUTS
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<h2 style="text-align:center; margin-bottom:5px;">🎯 ENTER YOUR RIDE DETAILS, CHAMPION 🎯</h2>
""", unsafe_allow_html=True)

col_date, col_time, col_pax = st.columns(3)
with col_date:
    st.markdown("### 📅 DATE")
    pickup_date = st.date_input("Date", min_value=datetime.date(2009, 1, 1), label_visibility="collapsed")
with col_time:
    st.markdown("### ⏰ TIME")
    pickup_time = st.time_input("Time", label_visibility="collapsed")
with col_pax:
    st.markdown("### 👥 PASSENGERS")
    passenger_count = st.slider("Passengers", min_value=1, max_value=8, value=1, label_visibility="collapsed")
    pax_emoji = "🧑" * passenger_count
    st.markdown(f"<div style='text-align:center; font-size:1.8rem; color:#FFD700; letter-spacing:2px;'>{pax_emoji}</div>", unsafe_allow_html=True)

pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)

st.markdown("""
<div style="text-align:center; color:#B22234; font-size:1.4rem; margin:14px 0; font-family:'Oswald',sans-serif; letter-spacing:4px;">
    ▼ ▼ ▼ &nbsp; ENTER COORDINATES, SOLDIER &nbsp; ▼ ▼ ▼
</div>
""", unsafe_allow_html=True)

col_pick, col_drop = st.columns(2)

with col_pick:
    st.markdown("""
    <div style="text-align:center; background:linear-gradient(135deg,rgba(0,80,0,0.5),rgba(0,150,0,0.2));
        border-radius:14px; padding:14px; border:2px solid #00cc44; margin-bottom:10px;">
        <span style="font-size:2rem;">🟢</span>
        <h3 style="color:#00FF77 !important; margin:4px 0; font-size:1.3rem !important;">PICKUP ZONE</h3>
        <span style="color:#aaffcc; font-size:0.85rem; font-family:'Oswald',sans-serif; letter-spacing:2px;">WHERE THE MISSION BEGINS</span>
    </div>
    """, unsafe_allow_html=True)
    pickup_longitude = st.number_input("📍 Pickup Longitude", value=-73.950655, format="%.6f", key="p_lon")
    pickup_latitude  = st.number_input("📍 Pickup Latitude",  value=40.783282,  format="%.6f", key="p_lat")

with col_drop:
    st.markdown("""
    <div style="text-align:center; background:linear-gradient(135deg,rgba(120,0,0,0.5),rgba(200,0,0,0.2));
        border-radius:14px; padding:14px; border:2px solid #FF4500; margin-bottom:10px;">
        <span style="font-size:2rem;">🔴</span>
        <h3 style="color:#FF6347 !important; margin:4px 0; font-size:1.3rem !important;">DROPOFF ZONE</h3>
        <span style="color:#ffbbaa; font-size:0.85rem; font-family:'Oswald',sans-serif; letter-spacing:2px;">THE FINAL DESTINATION</span>
    </div>
    """, unsafe_allow_html=True)
    dropoff_longitude = st.number_input("🏁 Dropoff Longitude", value=-73.984365, format="%.6f", key="d_lon")
    dropoff_latitude  = st.number_input("🏁 Dropoff Latitude",  value=40.769802,  format="%.6f", key="d_lat")

# ════════════════════════════════════════════════════════════════════
#  MAP HELPERS
# ════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def get_osrm_route(p_lon, p_lat, d_lon, d_lat):
    url = (f"http://router.project-osrm.org/route/v1/driving/"
           f"{p_lon},{p_lat};{d_lon},{d_lat}?geometries=geojson&overview=full")
    try:
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            coords = r.json()['routes'][0]['geometry']['coordinates']
            return [[c[0], c[1]] for c in coords]
    except Exception:
        pass
    return [[p_lon, p_lat], [d_lon, d_lat]]

@st.cache_data(ttl=3600)
def get_buildings(min_lat, min_lon, max_lat, max_lon):
    query = (f"[out:json][timeout:15];"
             f"way[\"building\"]({min_lat},{min_lon},{max_lat},{max_lon});"
             f"out geom;")
    try:
        r = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query}, timeout=20
        )
        buildings = []
        for el in r.json().get('elements', []):
            if 'geometry' not in el:
                continue
            coords = [[n['lon'], n['lat']] for n in el['geometry']]
            if len(coords) < 3:
                continue
            tags = el.get('tags', {})
            try:
                height = float(tags.get('height', tags.get('building:levels', '3'))) * 3.5
            except Exception:
                height = 12
            buildings.append({'polygon': coords, 'height': min(float(height), 400)})
        return buildings
    except Exception:
        return []

# ════════════════════════════════════════════════════════════════════
#  MAP
# ════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<h2 style="text-align:center; margin-bottom:4px;">🗺️ LIVE OPERATIONAL THEATER — NEW YORK CITY 🗺️</h2>
<div style="text-align:center; color:#3C3B6E; font-family:'Oswald',sans-serif; letter-spacing:3px; font-size:0.95rem; margin-bottom:12px;">
    REAL-TIME TACTICAL OVERVIEW · CLASSIFIED ROUTE DATA · 3D BUILDINGS ENGAGED
</div>
""", unsafe_allow_html=True)

mid_lat = (pickup_latitude + dropoff_latitude) / 2
mid_lon = (pickup_longitude + dropoff_longitude) / 2

pad = 0.008
bmin_lat = min(pickup_latitude,  dropoff_latitude)  - pad
bmax_lat = max(pickup_latitude,  dropoff_latitude)  + pad
bmin_lon = min(pickup_longitude, dropoff_longitude) - pad
bmax_lon = max(pickup_longitude, dropoff_longitude) + pad

with st.spinner("🏙️ Loading 3D buildings & street route…"):
    route_coords = get_osrm_route(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude)
    buildings    = get_buildings(bmin_lat, bmin_lon, bmax_lat, bmax_lon)

building_layer = pdk.Layer(
    "PolygonLayer",
    data=buildings,
    get_polygon="polygon",
    get_elevation="height",
    elevation_scale=1,
    extruded=True,
    get_fill_color=[180, 185, 210, 200],
    get_line_color=[120, 120, 160, 120],
    line_width_min_pixels=1,
    pickable=False,
)

route_layer = pdk.Layer(
    "PathLayer",
    data=[{"path": route_coords}],
    get_path="path",
    get_color=[178, 34, 52, 240],
    get_width=8,
    width_min_pixels=4,
)

pickup_layer = pdk.Layer(
    "ScatterplotLayer",
    data=[{"position": [pickup_longitude, pickup_latitude]}],
    get_position="position",
    get_color=[0, 200, 80, 255],
    get_radius=120,
    stroked=True,
    line_width_min_pixels=3,
    get_line_color=[0, 255, 100, 255],
)

dropoff_layer = pdk.Layer(
    "ScatterplotLayer",
    data=[{"position": [dropoff_longitude, dropoff_latitude]}],
    get_position="position",
    get_color=[220, 30, 30, 255],
    get_radius=120,
    stroked=True,
    line_width_min_pixels=3,
    get_line_color=[255, 69, 0, 255],
)

view_state = pdk.ViewState(
    latitude=mid_lat,
    longitude=mid_lon,
    zoom=14,
    pitch=60,
    bearing=0,
)

layers = [route_layer, pickup_layer, dropoff_layer]
if buildings:
    layers = [building_layer] + layers

deck = pdk.Deck(
    layers=layers,
    initial_view_state=view_state,
    map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
)
st.pydeck_chart(deck, use_container_width=True)

# ════════════════════════════════════════════════════════════════════
#  CTA BUTTON
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@keyframes bounce { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
.arrow-down { animation: bounce 0.8s ease-in-out infinite; display:inline-block; font-size:2.5rem; }
</style>
<div style="text-align:center; margin:22px 0 10px;">
    <span class="arrow-down">👇</span>
    <div style="color:#3C3B6E; font-family:'Oswald',sans-serif; font-size:1.5rem; letter-spacing:5px; margin:6px 0;">
        PRESS THE BUTTON · UNLEASH AMERICA
    </div>
    <span class="arrow-down">👇</span>
</div>
""", unsafe_allow_html=True)

url = 'https://taxifare.lewagon.ai/predict'

params = {
    'pickup_datetime':  str(pd.Timestamp(pickup_datetime)),
    'pickup_longitude': float(pickup_longitude),
    'pickup_latitude':  float(pickup_latitude),
    'dropoff_longitude': float(dropoff_longitude),
    'dropoff_latitude':  float(dropoff_latitude),
    'passenger_count':  int(passenger_count),
}

if st.button("🦅 💥 CALCULATE MY FARE, AMERICA! 💥 🦅"):
    st.session_state['show_result'] = False
    components.html(AMBIENT_JS, height=0)

    with st.spinner("🦅  EAGLE IS COMPUTING… FREEDOM IS LOADING… DEMOCRACY IS CRUNCHING NUMBERS… 🦅"):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                fare = data.get('fare', data.get('fare_amount', 0))
                st.session_state['fare']        = fare
                st.session_state['show_result'] = True
            else:
                st.error(f"⚠️ EAGLE FAILED TO RESPOND! STATUS CODE: {response.status_code}")
        except Exception as exc:
            st.error(f"⚠️ MISSION FAILED: {exc}")

if st.session_state.get('show_result'):
    fare = st.session_state['fare']

    st.balloons()
    components.html(AMERICA_JS, height=0)

    # ── CANVAS ANIMATION: planes, flags, explosions ──────────────────
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background: transparent; overflow: hidden; width:100%; height:360px; }
canvas { position:absolute; top:0; left:0; pointer-events:none; }
#emojis { position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; overflow:hidden; }
@keyframes rise  { from { transform: translateY(0) scale(0.7) rotate(0deg); opacity:1; }
                   to   { transform: translateY(-380px) scale(1.6) rotate(20deg); opacity:0; } }
@keyframes fly   { from { transform: translateX(-80px) scaleX(1); opacity:1; }
                   to   { transform: translateX(110vw) scaleX(1); opacity:0.9; } }
@keyframes shake { 0%,100%{transform:scale(1) rotate(0deg);} 25%{transform:scale(1.4) rotate(-10deg);}
                   75%{transform:scale(1.3) rotate(10deg);} }
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="emojis"></div>
<script>
var W = window.innerWidth || 900, H = 360;
var c = document.getElementById('c');
c.width = W; c.height = H;
var ctx = c.getContext('2d');
var particles = [];

var COLORS = ['#FF4500','#FFD700','#B22234','#3C3B6E','#FF69B4','#00BFFF','#FF8C00','#ADFF2F'];

function boom(x, y, big) {
    var n = big ? 80 : 45;
    for (var i = 0; i < n; i++) {
        var angle = (Math.PI * 2 / n) * i + Math.random() * 0.3;
        var speed = (big ? 4 : 2) + Math.random() * (big ? 5 : 3);
        particles.push({
            x:x, y:y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed - (big ? 1.5 : 0.5),
            life: 1,
            decay: 0.012 + Math.random() * 0.012,
            color: COLORS[Math.floor(Math.random() * COLORS.length)],
            size: (big ? 4 : 2) + Math.random() * 3,
            trail: []
        });
    }
}

function frame() {
    ctx.clearRect(0, 0, W, H);
    particles = particles.filter(function(p) {
        p.trail.push({x:p.x, y:p.y});
        if (p.trail.length > 6) p.trail.shift();
        p.x += p.vx; p.y += p.vy; p.vy += 0.06;
        p.life -= p.decay;
        if (p.life <= 0) return false;
        // trail
        for (var t = 0; t < p.trail.length; t++) {
            ctx.beginPath();
            ctx.arc(p.trail[t].x, p.trail[t].y, p.size * p.life * (t/p.trail.length) * 0.7, 0, Math.PI*2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.life * (t/p.trail.length) * 0.4;
            ctx.fill();
        }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.life;
        ctx.fill();
        ctx.globalAlpha = 1;
        return true;
    });
    requestAnimationFrame(frame);
}

// Burst schedule
var shots = [
    [0,   W*0.2, H*0.3, true],
    [200, W*0.8, H*0.25, true],
    [400, W*0.5, H*0.4, true],
    [600, W*0.35,H*0.2, false],
    [700, W*0.65,H*0.35,false],
    [900, W*0.1, H*0.5, true],
    [1000,W*0.9, H*0.45,true],
    [1200,W*0.5, H*0.15,true],
    [1400,W*0.25,H*0.55,false],
    [1500,W*0.75,H*0.2, false],
    [1800,W*0.5, H*0.3, true],
    [2000,W*0.15,H*0.3, true],
    [2200,W*0.85,H*0.4, true],
    [2500,W*0.4, H*0.2, true],
    [2800,W*0.6, H*0.35,true],
    [3000,W*0.5, H*0.25,true]
];
shots.forEach(function(s) {
    setTimeout(function() { boom(s[1], s[2], s[3]); }, s[0]);
});
// Random after that
setInterval(function() {
    boom(Math.random()*W, Math.random()*H*0.7, Math.random()>0.4);
}, 600);
frame();

// Emoji elements
var emojiDiv = document.getElementById('emojis');

var risingItems = [
    '🇺🇸','🇺🇸','🇺🇸','🦅','🦅','💥','💥','🎆','🗽','💵','🎇','🏆','🇺🇸','💥','🦅'
];
risingItems.forEach(function(e, i) {
    var el = document.createElement('div');
    el.textContent = e;
    el.style.cssText = 'position:absolute; font-size:2rem; bottom:-40px; left:' +
        (3 + Math.random()*90) + '%; animation: rise ' +
        (1.5 + Math.random()*2) + 's ease-out ' + (i * 0.18) + 's forwards;';
    emojiDiv.appendChild(el);
});

// Planes flying across
var planeRows = [8, 20, 35, 50, 65, 78];
planeRows.forEach(function(top, i) {
    var p = document.createElement('div');
    p.textContent = '✈️';
    p.style.cssText = 'position:absolute; font-size:2.2rem; top:' + top +
        '%; left:-70px; animation: fly ' + (1.2 + Math.random()*0.8) +
        's linear ' + (i * 0.35) + 's forwards;';
    emojiDiv.appendChild(p);
    // second wave
    setTimeout(function() {
        var p2 = document.createElement('div');
        p2.textContent = '✈️';
        p2.style.cssText = 'position:absolute; font-size:2.2rem; top:' + (top+5) +
            '%; left:-70px; animation: fly ' + (1.3 + Math.random()*0.6) + 's linear 0s forwards;';
        emojiDiv.appendChild(p2);
    }, 2500);
});
// Big explosion emoji
setTimeout(function() {
    var ex = document.createElement('div');
    ex.textContent = '💥';
    ex.style.cssText = 'position:absolute; font-size:5rem; top:30%; left:45%; animation: shake 0.3s ease-in-out 6;';
    emojiDiv.appendChild(ex);
}, 1500);
</script>
</body>
</html>
""", height=370)

    # ── FARE RESULT CARD ─────────────────────────────────────────────
    lat1 = math.radians(pickup_latitude);  lon1 = math.radians(pickup_longitude)
    lat2 = math.radians(dropoff_latitude); lon2 = math.radians(dropoff_longitude)
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    dist_km = 6371 * 2 * math.asin(math.sqrt(a))

    st.markdown(f"""
    <style>
    @keyframes result-pop {{ from {{ transform:scale(0.4); opacity:0; }} to {{ transform:scale(1); opacity:1; }} }}
    </style>
    <div style="
        text-align:center;
        background: linear-gradient(135deg, #f0f0ff, #fff0f0);
        border: 5px solid #B22234;
        border-radius: 28px;
        padding: 44px 30px;
        margin: 10px 0;
        box-shadow: 0 8px 40px rgba(178,34,52,0.25);
        animation: result-pop 0.5s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
    ">
        <div style="font-size:3.5rem; margin-bottom:10px;">💵 🦅 💵</div>
        <div style="font-family:'Bebas Neue',Impact,sans-serif; font-size:3.8rem;
                    color:#3C3B6E; letter-spacing:8px; line-height:1;">ESTIMATED FARE</div>
        <div style="font-family:'Bebas Neue',Impact,sans-serif; font-size:8.5rem;
                    color:#B22234; letter-spacing:4px; line-height:1.1;">${fare:.2f}</div>
        <div style="color:#3C3B6E; font-size:1.25rem; letter-spacing:5px; margin-top:18px; font-family:'Oswald',sans-serif;">
            🇺🇸 &nbsp; GOD BLESS AMERICA AND YOUR WALLET &nbsp; 🇺🇸
        </div>
        <div style="font-size:2.8rem; margin-top:16px;">🎆 🗽 🎆 🦅 🎆 🗽 🎆</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🗺️ DISTANCE",  f"{dist_km:.2f} km")
    with c2:
        st.metric("💰 FARE",       f"${fare:.2f}")
    with c3:
        label = f"{passenger_count} HERO{'S' if passenger_count > 1 else ''}"
        st.metric("👥 PASSENGERS", label)

# ════════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:22px 0 10px;">
    <div style="color:#B22234; font-family:'Oswald',sans-serif; font-size:1.4rem; letter-spacing:5px;">
        ★ MADE WITH 🦅 PATRIOTISM AND 💥 MACHINE LEARNING ★
    </div>
    <div style="color:#3C3B6E; font-size:0.9rem; margin-top:8px; font-family:'Oswald',sans-serif; letter-spacing:2px;">
        Powered by Le Wagon Data Science Bootcamp &nbsp;|&nbsp; NYC Taxifare Prediction API
    </div>
    <div style="font-size:2.2rem; margin-top:10px;">🇺🇸 &nbsp; 🚕 &nbsp; 🗽 &nbsp; 🚕 &nbsp; 🇺🇸</div>
</div>
""", unsafe_allow_html=True)
