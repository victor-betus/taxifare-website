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

# ════════════════════════════════════════════════════════════════════
#  CSS — WEB 2000 STYLE
# ════════════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Boogaloo&family=Oswald:wght@700&family=VT323&display=swap');

/* TIMES SQUARE BACKGROUND — low opacity */
.stApp {
    background-image:
        linear-gradient(rgba(255,255,255,0.87), rgba(255,255,255,0.87)),
        url('https://upload.wikimedia.org/wikipedia/commons/3/39/NYC_-_Times_Square.JPG');
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    background-color: #ffffff;
}

/* MAIN CONTAINER — classic 2000s bordered box */
.main .block-container {
    background: #fffef5;
    border: 4px ridge #B22234;
    outline: 2px solid #3C3B6E;
    outline-offset: 3px;
    padding: 18px 28px;
    max-width: 1100px;
    font-family: 'Verdana', 'Comic Sans MS', Arial, sans-serif;
}

/* TITLE */
h1 {
    font-family: 'Boogaloo', 'Impact', 'Arial Black', sans-serif !important;
    font-size: 3.8rem !important;
    color: #B22234 !important;
    text-shadow: 3px 3px 0 #3C3B6E, 6px 6px 0 #FFD700 !important;
    text-align: center !important;
    letter-spacing: 4px !important;
    margin: 10px 0 !important;
}

/* H2 */
h2 {
    font-family: 'Oswald', 'Impact', Arial Black, sans-serif !important;
    color: #3C3B6E !important;
    text-align: center !important;
    letter-spacing: 3px !important;
    border-bottom: 3px double #B22234 !important;
    padding-bottom: 6px !important;
    font-size: 1.5rem !important;
}

/* H3 */
h3 {
    font-family: 'Oswald', Arial, sans-serif !important;
    color: #B22234 !important;
    font-size: 1rem !important;
    letter-spacing: 2px !important;
}

/* LABELS / TEXT */
label, p, li, .stMarkdown p {
    color: #1a1a1a !important;
    font-family: 'Verdana', 'Comic Sans MS', Arial, sans-serif !important;
    font-size: 0.9rem !important;
}

/* INPUTS — classic inset 2000s */
input[type="number"], input[type="text"], input[type="time"], input[type="date"] {
    background: #f0f0f8 !important;
    color: #000080 !important;
    border: 2px inset #aaaacc !important;
    border-radius: 3px !important;
    font-family: 'Verdana', Arial, sans-serif !important;
    font-size: 0.95rem !important;
}
input:focus {
    border-color: #B22234 !important;
    outline: 1px dotted #B22234 !important;
}

/* BUTTON — classic 2000s 3D raised, CENTRÉ */
.stButton > button {
    background: linear-gradient(to bottom, #FF6666 0%, #B22234 45%, #880000 100%) !important;
    color: #FFD700 !important;
    font-family: 'Boogaloo', 'Impact', 'Arial Black', sans-serif !important;
    font-size: 2rem !important;
    letter-spacing: 4px !important;
    border: 4px outset #FF8888 !important;
    border-radius: 6px !important;
    padding: 18px 60px !important;
    width: 100% !important;
    text-shadow: 2px 2px 4px #000 !important;
    box-shadow: 4px 4px 8px rgba(0,0,0,0.4) !important;
    cursor: pointer !important;
    transition: all 0.1s !important;
}
.stButton > button:hover {
    background: linear-gradient(to bottom, #FF8888 0%, #CC2244 45%, #AA0000 100%) !important;
    border-style: inset !important;
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 4px rgba(0,0,0,0.4) !important;
}
.stButton > button:active {
    border-style: inset !important;
    transform: translate(3px, 3px) !important;
    box-shadow: 1px 1px 2px rgba(0,0,0,0.4) !important;
}

/* METRICS */
[data-testid="stMetricValue"] {
    font-family: 'VT323', 'Courier New', monospace !important;
    font-size: 3rem !important;
    color: #B22234 !important;
    text-shadow: 1px 1px 0 #3C3B6E !important;
}
[data-testid="stMetricLabel"] {
    color: #3C3B6E !important;
    font-family: 'Verdana', Arial, sans-serif !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}

/* COLUMNS — 2000s box style */
[data-testid="column"] {
    background: #f8f8ff;
    border: 2px groove #3C3B6E;
    padding: 12px !important;
}

/* SPINNER */
.stSpinner > div { border-color: #B22234 transparent #B22234 transparent !important; }

/* HIDE STREAMLIT CHROME */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* SCROLLBAR — classic */
::-webkit-scrollbar       { width: 16px; }
::-webkit-scrollbar-track { background: #c0c0c0; border: 1px inset #888; }
::-webkit-scrollbar-thumb { background: #3C3B6E; border: 2px outset #8888cc; }

/* NUMBER INPUT STEPPERS */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: #ddddee !important;
    color: #000080 !important;
    border: 2px outset #aaaacc !important;
    border-radius: 2px !important;
}

/* HR override */
hr { border: 2px ridge #B22234 !important; margin: 12px 0 !important; }

/* BLINKING */
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0;} }
.blink { animation: blink 1s step-start infinite; }

/* MARQUEE glow */
.marq { color: #B22234; font-family: 'Boogaloo','Impact',sans-serif;
        font-size: 1.1rem; letter-spacing: 3px; font-weight: bold; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Bouton UNMUTE visible — seul moyen fiable cross-browser ─────────────────
AUDIO_COMPONENT = """
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:transparent; display:flex; justify-content:center; align-items:center; height:60px; }
#btn {
    background: linear-gradient(to bottom, #FF6666, #B22234);
    color: #FFD700;
    font-family: 'Impact', 'Arial Black', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 3px;
    border: 3px outset #FF9999;
    border-radius: 6px;
    padding: 10px 28px;
    cursor: pointer;
    text-shadow: 1px 1px 2px #000;
    box-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    animation: pulse 1s ease-in-out infinite alternate;
}
#btn.playing {
    background: linear-gradient(to bottom, #66AA66, #228822);
    border-color: #99FF99;
    animation: none;
}
@keyframes pulse {
    from { box-shadow: 3px 3px 6px rgba(0,0,0,0.4), 0 0 8px rgba(255,100,100,0.5); }
    to   { box-shadow: 3px 3px 6px rgba(0,0,0,0.4), 0 0 20px rgba(255,100,100,0.9); }
}
</style>
</head>
<body>
<audio id="honk" loop>
  <source src="https://www.orangefreesounds.com/wp-content/uploads/2021/10/Noisy-street-car-horn-honking.mp3" type="audio/mpeg">
</audio>
<button id="btn" onclick="toggleSound()">🔇 CLICK TO UNMUTE NYC 🚕</button>
<script>
var audio = document.getElementById('honk');
var btn   = document.getElementById('btn');
var on    = false;
audio.volume = 0.4;

function toggleSound() {
    if (!on) {
        audio.play().then(function() {
            on = true;
            btn.textContent = '🔊 NYC SOUNDS ON 🚕';
            btn.classList.add('playing');
        }).catch(function(){});
    } else {
        audio.pause();
        on = false;
        btn.textContent = '🔇 CLICK TO UNMUTE NYC 🚕';
        btn.classList.remove('playing');
    }
}
</script>
</body>
</html>
"""
components.html(AUDIO_COMPONENT, height=62)

# ── NYC street ambiance (honking, traffic) while loading ────────────────────
AMBIENT_JS = """
<html><body style="margin:0;padding:0;overflow:hidden;background:transparent;">
<audio id="amb" loop>
  <source src="https://www.orangefreesounds.com/wp-content/uploads/2021/10/Noisy-street-car-horn-honking.mp3" type="audio/mpeg">
</audio>
<script>
var a = document.getElementById('amb');
a.volume = 0.45;
a.play().catch(function(){});
</script>
</body></html>
"""

# ── America Fuck Yeah on success ────────────────────────────────────────────
AMERICA_JS = """
<html><body style="margin:0;padding:0;background:transparent;">
<audio id="am">
  <source src="https://archive.org/download/AMERICAFKYEAHMUSICVIDEOTeamAmericaWorldPoliceTHEMESONG/AMERICA%20F-%23K%20YEAH%21%20MUSIC%20VIDEO%20-%20Team%20America%20World%20Police%20THEME%20SONG.mp3" type="audio/mpeg">
</audio>
<script>
var m = document.getElementById('am');
m.volume = 0.85;
m.play().catch(function(){});
</script>
</body></html>
"""

# ════════════════════════════════════════════════════════════════════
#  HEADER — WEB 2000 VIBES
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@keyframes rainbow {
  0%{color:#B22234} 16%{color:#FF8C00} 33%{color:#FFD700}
  50%{color:#228B22} 66%{color:#3C3B6E} 83%{color:#8B008B} 100%{color:#B22234}
}
.rainbow-star { animation: rainbow 2s linear infinite; display:inline-block; }
</style>

<marquee behavior="scroll" direction="left" scrollamount="5"
         style="background:#3C3B6E; color:#FFD700; font-family:'Boogaloo','Impact',sans-serif;
                font-size:1.1rem; padding:6px 0; letter-spacing:3px; border:2px outset #8888cc;">
  🦅 WELCOME TO AMERICA'S #1 NYC TAXI FARE CALCULATOR 🚕 &nbsp;&nbsp;&nbsp;
  FREEDOM · DEMOCRACY · MACHINE LEARNING · YELLOW CABS 💥 &nbsp;&nbsp;&nbsp;
  🇺🇸 THE GREATEST WEBSITE IN THE HISTORY OF THE INTERNET 🇺🇸 &nbsp;&nbsp;&nbsp;
  ⚠️ BEST VIEWED IN INTERNET EXPLORER 6.0 AT 1024×768 ⚠️ &nbsp;&nbsp;&nbsp;
</marquee>

<div style="text-align:center; margin:14px 0 4px;">
    <h1>🦅 AMERICA'S #1 NYC TAXI FARE CALCULATOR 🦅</h1>
</div>

<div style="text-align:center; margin:6px 0;">
    <span class="rainbow-star" style="font-size:1.4rem;">
    ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★
    </span>
</div>

<div style="text-align:center; font-family:'Verdana',sans-serif; font-size:0.95rem;
            color:#000080; background:#e8e8ff; border:2px groove #3C3B6E;
            padding:8px; margin:8px 0; letter-spacing:2px;">
    🇺🇸 &nbsp; THE GREATEST · THE BOLDEST · THE MOST POWERFUL TAXI CALCULATOR IN THE KNOWN UNIVERSE &nbsp; 🇺🇸
</div>
""", unsafe_allow_html=True)

# NYC TAXI GIFs — centered row
st.markdown("""
<div style="text-align:center; background:#fffff0; border:3px ridge #B22234;
            padding:14px; margin:10px 0;">
    <div style="font-family:'Boogaloo','Impact',sans-serif; color:#B22234;
                font-size:1.2rem; letter-spacing:3px; margin-bottom:10px;">
        🚕 NEW YORK CITY YELLOW CABS 🚕
    </div>
    <div style="display:flex; justify-content:center; align-items:center; gap:16px; flex-wrap:wrap;">
        <img src="https://media.giphy.com/media/93nb6Zt16rwjGk2Y8O/giphy.gif"
             height="160" style="border:4px outset #B22234;">
        <img src="https://media.giphy.com/media/Y70DOxH0fpUHBtOCiF/giphy.gif"
             height="160" style="border:4px outset #3C3B6E;">
        <img src="https://media.giphy.com/media/Z9lNKlUpafy9uWELmz/giphy.gif"
             height="160" style="border:4px outset #B22234;">
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  INPUTS — organized 2-column layout
# ════════════════════════════════════════════════════════════════════
st.markdown("<h2>🎯 ENTER YOUR RIDE DETAILS</h2>", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div style="background:#eeeeff; border:2px groove #3C3B6E; padding:10px; margin-bottom:8px;">
        <span style="font-family:'Boogaloo','Impact',sans-serif; color:#3C3B6E;
                     font-size:1.1rem; letter-spacing:2px;">📅 WHEN ARE YOU RIDING?</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**DATE**")
        pickup_date = st.date_input("Date", min_value=datetime.date(2009, 1, 1), label_visibility="collapsed")
    with c2:
        st.markdown("**TIME**")
        pickup_time = st.time_input("Time", label_visibility="collapsed")

    st.markdown("""
    <div style="background:#eeeeff; border:2px groove #3C3B6E; padding:10px; margin:8px 0;">
        <span style="font-family:'Boogaloo','Impact',sans-serif; color:#3C3B6E;
                     font-size:1.1rem; letter-spacing:2px;">👥 PASSENGERS</span>
    </div>
    """, unsafe_allow_html=True)
    passenger_count = st.slider("Passengers", min_value=1, max_value=8, value=1, label_visibility="collapsed")
    pax_icons = "🧑" * passenger_count
    st.markdown(f"<div style='text-align:center; font-size:1.6rem;'>{pax_icons}</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div style="background:#eeffee; border:2px groove #006600; padding:10px; margin-bottom:8px;">
        <span style="font-family:'Boogaloo','Impact',sans-serif; color:#006600;
                     font-size:1.1rem; letter-spacing:2px;">🟢 PICKUP LOCATION</span>
    </div>
    """, unsafe_allow_html=True)
    pickup_address = st.text_input("Pickup address", value="Central Park, New York", key="p_addr", label_visibility="collapsed")

    st.markdown("""
    <div style="background:#ffeeee; border:2px groove #880000; padding:10px; margin:8px 0;">
        <span style="font-family:'Boogaloo','Impact',sans-serif; color:#880000;
                     font-size:1.1rem; letter-spacing:2px;">🔴 DROPOFF LOCATION</span>
    </div>
    """, unsafe_allow_html=True)
    dropoff_address = st.text_input("Dropoff address", value="Times Square, New York", key="d_addr", label_visibility="collapsed")

pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)

@st.cache_data(ttl=86400)
def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1, "countrycodes": "us"}
    headers = {"User-Agent": "TaxiFareWebApp/1.0"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=5)
        if r.status_code == 200 and r.json():
            res = r.json()[0]
            return float(res['lat']), float(res['lon'])
    except Exception:
        pass
    return None, None

pickup_lat, pickup_lon   = geocode_address(pickup_address)
dropoff_lat, dropoff_lon = geocode_address(dropoff_address)

if pickup_lat is None or dropoff_lat is None:
    st.warning("⚠️ Address not found — check spelling and try again.")
    pickup_lat,  pickup_lon  = 40.783282, -73.950655
    dropoff_lat, dropoff_lon = 40.769802, -73.984365

pickup_latitude,   pickup_longitude  = pickup_lat,  pickup_lon
dropoff_latitude,  dropoff_longitude = dropoff_lat, dropoff_lon

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
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2>🗺️ LIVE MAP — NEW YORK CITY</h2>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-family:'Verdana',sans-serif; font-size:0.8rem;
            color:#000080; margin-bottom:8px; letter-spacing:1px;">
    Real-time street route · 3D buildings · Tactical overlay
</div>
""", unsafe_allow_html=True)

mid_lat = (pickup_latitude + dropoff_latitude) / 2
mid_lon = (pickup_longitude + dropoff_longitude) / 2

pad = 0.008
bmin_lat = min(pickup_latitude,  dropoff_latitude)  - pad
bmax_lat = max(pickup_latitude,  dropoff_latitude)  + pad
bmin_lon = min(pickup_longitude, dropoff_longitude) - pad
bmax_lon = max(pickup_longitude, dropoff_longitude) + pad

with st.spinner("Loading 3D buildings & street route…"):
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

dlat = abs(pickup_latitude - dropoff_latitude)
dlon = abs(pickup_longitude - dropoff_longitude)
max_diff = max(dlat, dlon)
if max_diff < 0.01:   auto_zoom = 15
elif max_diff < 0.03: auto_zoom = 14
elif max_diff < 0.07: auto_zoom = 13
elif max_diff < 0.15: auto_zoom = 12
elif max_diff < 0.4:  auto_zoom = 11
else:                 auto_zoom = 10

view_state = pdk.ViewState(
    latitude=mid_lat,
    longitude=mid_lon,
    zoom=auto_zoom,
    pitch=40,
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
st.pydeck_chart(deck, use_container_width=True, height=550)

# ════════════════════════════════════════════════════════════════════
#  PREDICT BUTTON — centered
# ════════════════════════════════════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; margin:10px 0 6px;">
    <span class="blink" style="font-size:1.5rem; color:#B22234;">▼ CLICK THE BUTTON BELOW ▼</span>
</div>
""", unsafe_allow_html=True)

url = 'https://taxifare.lewagon.ai/predict'

params = {
    'pickup_datetime':   str(pd.Timestamp(pickup_datetime)),
    'pickup_longitude':  float(pickup_longitude),
    'pickup_latitude':   float(pickup_latitude),
    'dropoff_longitude': float(dropoff_longitude),
    'dropoff_latitude':  float(dropoff_latitude),
    'passenger_count':   int(passenger_count),
}

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    clicked = st.button("🦅 CALCULATE MY FARE, AMERICA! 🦅", use_container_width=True)

if clicked:
    st.session_state['show_result'] = False
    components.html(AMERICA_JS, height=1)
    with st.spinner("🦅 EAGLE IS COMPUTING… FREEDOM IS LOADING… 🦅"):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                fare = data.get('fare', data.get('fare_amount', 0))
                st.session_state['fare']        = fare
                st.session_state['show_result'] = True
            else:
                st.error(f"⚠️ EAGLE FAILED! STATUS: {response.status_code}")
        except Exception as exc:
            st.error(f"⚠️ MISSION FAILED: {exc}")

# ════════════════════════════════════════════════════════════════════
#  RESULT
# ════════════════════════════════════════════════════════════════════
if st.session_state.get('show_result'):
    fare = st.session_state['fare']

    st.balloons()

    # Canvas fireworks animation
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:transparent; overflow:hidden; width:100%; height:340px; }
canvas { position:absolute; top:0; left:0; pointer-events:none; }
#emojis { position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; overflow:hidden; }
@keyframes rise { from{transform:translateY(0) scale(0.7);opacity:1;} to{transform:translateY(-360px) scale(1.5);opacity:0;} }
@keyframes fly  { from{transform:translateX(-80px);opacity:1;} to{transform:translateX(110vw);opacity:0.9;} }
@keyframes shake{ 0%,100%{transform:scale(1);} 50%{transform:scale(1.5) rotate(10deg);} }
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="emojis"></div>
<script>
var W=window.innerWidth||900, H=340;
var c=document.getElementById('c'); c.width=W; c.height=H;
var ctx=c.getContext('2d'); var particles=[];
var COLORS=['#FF4500','#FFD700','#B22234','#3C3B6E','#FF69B4','#00BFFF','#FF8C00'];
function boom(x,y,big){
    var n=big?80:40;
    for(var i=0;i<n;i++){
        var a=(Math.PI*2/n)*i+Math.random()*0.3;
        var s=(big?4:2)+Math.random()*(big?5:3);
        particles.push({x:x,y:y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-(big?1.5:0.5),
            life:1,decay:0.012+Math.random()*0.012,
            color:COLORS[Math.floor(Math.random()*COLORS.length)],
            size:(big?4:2)+Math.random()*3});
    }
}
function frame(){
    ctx.clearRect(0,0,W,H);
    particles=particles.filter(function(p){
        p.x+=p.vx; p.y+=p.vy; p.vy+=0.06; p.life-=p.decay;
        if(p.life<=0) return false;
        ctx.beginPath(); ctx.arc(p.x,p.y,p.size*p.life,0,Math.PI*2);
        ctx.fillStyle=p.color; ctx.globalAlpha=p.life; ctx.fill();
        ctx.globalAlpha=1; return true;
    });
    requestAnimationFrame(frame);
}
var shots=[[0,.2,.3,true],[200,.8,.25,true],[400,.5,.4,true],[700,.35,.2,false],
           [900,.1,.5,true],[1000,.9,.45,true],[1200,.5,.15,true],
           [1800,.5,.3,true],[2000,.15,.3,true],[2500,.85,.4,true]];
shots.forEach(function(s){setTimeout(function(){boom(W*s[1],H*s[2],s[3]);},s[0]);});
setInterval(function(){boom(Math.random()*W,Math.random()*H*0.7,Math.random()>0.4);},500);
frame();
var ed=document.getElementById('emojis');
['🇺🇸','🇺🇸','🦅','💥','🎆','🗽','💵','🇺🇸','💥','🦅','🎇','🇺🇸'].forEach(function(e,i){
    var el=document.createElement('div');
    el.textContent=e;
    el.style.cssText='position:absolute;font-size:2rem;bottom:-40px;left:'+(5+Math.random()*88)+'%;'
        +'animation:rise '+(1.5+Math.random()*2)+'s ease-out '+(i*0.2)+'s forwards;';
    ed.appendChild(el);
});
[8,22,38,55,70,82].forEach(function(top,i){
    var p=document.createElement('div'); p.textContent='✈️';
    p.style.cssText='position:absolute;font-size:2.2rem;top:'+top+'%;left:-70px;'
        +'animation:fly '+(1.2+Math.random()*0.8)+'s linear '+(i*0.4)+'s forwards;';
    ed.appendChild(p);
});
setTimeout(function(){
    var ex=document.createElement('div'); ex.textContent='💥';
    ex.style.cssText='position:absolute;font-size:5rem;top:28%;left:44%;animation:shake 0.3s ease-in-out 8;';
    ed.appendChild(ex);
},1500);
</script>
</body>
</html>
""", height=350)

    # Fare result card
    lat1=math.radians(pickup_latitude);  lon1=math.radians(pickup_longitude)
    lat2=math.radians(dropoff_latitude); lon2=math.radians(dropoff_longitude)
    a=math.sin((lat2-lat1)/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    dist_km=6371*2*math.asin(math.sqrt(a))

    st.markdown(f"""
    <style>
    @keyframes result-pop {{ from{{transform:scale(0.4);opacity:0;}} to{{transform:scale(1);opacity:1;}} }}
    </style>
    <div style="
        text-align:center;
        background: linear-gradient(135deg, #fffff0, #fff0f0);
        border: 5px ridge #B22234;
        outline: 2px solid #3C3B6E;
        padding: 36px 24px;
        margin: 12px 0;
        box-shadow: 6px 6px 12px rgba(0,0,0,0.3);
        animation: result-pop 0.5s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
        font-family: 'Verdana', Arial, sans-serif;
    ">
        <div style="font-size:3rem; margin-bottom:8px;">💵 🦅 💵</div>
        <div style="font-family:'Boogaloo','Impact',sans-serif; font-size:2.8rem;
                    color:#3C3B6E; letter-spacing:5px; text-shadow:2px 2px 0 #ccc;">
            ESTIMATED FARE
        </div>
        <div style="font-family:'Boogaloo','Impact',sans-serif; font-size:7rem;
                    color:#B22234; letter-spacing:3px;
                    text-shadow: 4px 4px 0 #3C3B6E, 7px 7px 0 #FFD700;">
            ${fare:.2f}
        </div>
        <div style="color:#000080; font-size:1rem; letter-spacing:4px; margin-top:14px;
                    font-family:'Verdana',sans-serif;">
            🇺🇸 &nbsp; GOD BLESS AMERICA AND YOUR WALLET &nbsp; 🇺🇸
        </div>
        <div style="font-size:2.5rem; margin-top:12px;">🎆 🗽 🎆 🦅 🎆 🗽 🎆</div>
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
#  FOOTER — classic 2000s
# ════════════════════════════════════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-family:'Verdana',Arial,sans-serif; padding:14px 0 8px;
            background:#f0f0ff; border:2px groove #3C3B6E; margin-top:8px;">
    <div style="font-family:'Boogaloo','Impact',sans-serif; color:#B22234;
                font-size:1.2rem; letter-spacing:3px;">
        ★ MADE WITH 🦅 PATRIOTISM AND 💥 MACHINE LEARNING ★
    </div>
    <div style="color:#000080; font-size:0.78rem; margin-top:6px; letter-spacing:1px;">
        Powered by Le Wagon Data Science Bootcamp &nbsp;|&nbsp; NYC Taxifare Prediction API
    </div>
    <div style="color:#666; font-size:0.7rem; margin-top:4px; font-style:italic;">
        ⚠️ Best viewed in Internet Explorer 6.0 at 1024×768 resolution &nbsp;|&nbsp;
        <span class="blink">🚧 THIS SITE IS UNDER CONSTRUCTION 🚧</span>
    </div>
    <div style="margin-top:8px; font-family:'VT323','Courier New',monospace;
                color:#3C3B6E; font-size:1.1rem; letter-spacing:2px;">
        👁️ VISITOR COUNT: 1,337,420
    </div>
    <div style="font-size:1.8rem; margin-top:8px;">🇺🇸 🚕 🗽 🚕 🇺🇸</div>
</div>
""", unsafe_allow_html=True)
