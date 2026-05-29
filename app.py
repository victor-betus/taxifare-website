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

/* STARFIELD BACKGROUND */
.stApp {
    background-color: #06060f;
    background-image:
        radial-gradient(1px 1px at 5% 15%, #FFD700, transparent),
        radial-gradient(1px 1px at 12% 80%, #fff, transparent),
        radial-gradient(2px 2px at 20% 35%, #FFD700, transparent),
        radial-gradient(1px 1px at 28% 60%, #fff, transparent),
        radial-gradient(2px 2px at 35% 10%, #FFD700, transparent),
        radial-gradient(1px 1px at 42% 90%, #fff, transparent),
        radial-gradient(2px 2px at 50% 45%, #FFD700, transparent),
        radial-gradient(1px 1px at 58% 20%, #fff, transparent),
        radial-gradient(2px 2px at 65% 70%, #FFD700, transparent),
        radial-gradient(1px 1px at 72% 5%, #fff, transparent),
        radial-gradient(2px 2px at 80% 55%, #FFD700, transparent),
        radial-gradient(1px 1px at 88% 30%, #fff, transparent),
        radial-gradient(2px 2px at 95% 85%, #FFD700, transparent),
        repeating-linear-gradient(0deg, transparent, transparent 80px, rgba(60,59,110,0.07) 80px, rgba(60,59,110,0.07) 81px),
        linear-gradient(180deg, #06060f 0%, #0a000f 100%);
}

/* MAIN CONTAINER */
.main .block-container {
    background: rgba(4, 4, 20, 0.93);
    border-radius: 25px;
    border: 4px solid #FFD700;
    padding: 2rem 3rem;
    max-width: 1400px;
    box-shadow:
        0 0 50px rgba(255,215,0,0.4),
        0 0 100px rgba(178,34,52,0.2),
        inset 0 0 40px rgba(255,215,0,0.03);
}

/* TITLE */
h1 {
    font-family: 'Bebas Neue', 'Impact', 'Arial Black', sans-serif !important;
    font-size: 4.2rem !important;
    background: linear-gradient(90deg, #B22234, #FFD700, #ffffff, #FFD700, #B22234) !important;
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
    color: #FF4500 !important;
    letter-spacing: 5px !important;
    text-transform: uppercase !important;
    text-shadow: 0 0 12px rgba(255,69,0,0.6) !important;
}

h3 { color: #FFD700 !important; font-size: 1.1rem !important; }

/* LABELS / TEXT */
label, p, li, .stMarkdown p {
    color: #dde !important;
    font-family: 'Oswald', 'Arial', sans-serif !important;
}

/* ALL INPUTS */
input[type="number"], input[type="text"], input[type="time"], input[type="date"] {
    background: rgba(10, 10, 50, 0.95) !important;
    color: #FFD700 !important;
    border: 2px solid rgba(60,59,110,0.9) !important;
    border-radius: 8px !important;
    font-family: 'Oswald', monospace !important;
    font-size: 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input:focus {
    border-color: #FFD700 !important;
    box-shadow: 0 0 15px rgba(255,215,0,0.5) !important;
    outline: none !important;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #B22234, #FF4500, #FFD700, #FF4500, #B22234) !important;
    background-size: 300% 300% !important;
    color: #000 !important;
    font-family: 'Bebas Neue', 'Impact', 'Arial Black', sans-serif !important;
    font-size: 2.4rem !important;
    letter-spacing: 7px !important;
    border: 3px solid #FFD700 !important;
    border-radius: 18px !important;
    padding: 22px 0 !important;
    width: 100% !important;
    box-shadow: 0 0 35px rgba(255,215,0,0.7), 0 0 70px rgba(255,69,0,0.4) !important;
    animation: btn-glow 1.8s ease infinite alternate, gradient-shift 3s ease infinite !important;
    transition: transform 0.1s !important;
    cursor: pointer !important;
}
@keyframes btn-glow {
    from { box-shadow: 0 0 20px rgba(255,215,0,0.4); }
    to   { box-shadow: 0 0 70px rgba(255,215,0,1), 0 0 110px rgba(255,69,0,0.7); }
}
.stButton > button:hover  { transform: scale(1.03) !important; }
.stButton > button:active { transform: scale(0.97) !important; }

/* METRICS */
[data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', Impact, sans-serif !important;
    font-size: 3.5rem !important;
    color: #FFD700 !important;
    text-shadow: 0 0 25px rgba(255,215,0,0.8) !important;
}
[data-testid="stMetricLabel"] {
    color: #FF4500 !important;
    font-family: 'Oswald', sans-serif !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
}

/* COLUMNS */
[data-testid="column"] {
    background: rgba(15, 15, 55, 0.6);
    border-radius: 15px;
    border: 1px solid rgba(255,215,0,0.25);
    padding: 15px !important;
}

/* SPINNER */
.stSpinner > div { border-color: #FFD700 transparent #FFD700 transparent !important; }

/* HIDE STREAMLIT CHROME */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* SCROLLBAR */
::-webkit-scrollbar       { width: 8px; }
::-webkit-scrollbar-track { background: #06060f; }
::-webkit-scrollbar-thumb { background: #FFD700; border-radius: 4px; }

/* NUMBER INPUT STEPPERS */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: rgba(60,59,110,0.8) !important;
    color: #FFD700 !important;
    border: 1px solid #FFD700 !important;
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

# ── EXPLOSION SOUND for the predict button ──────────────────────────────────
EXPLOSION_JS = """
<script>
(function() {
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
        gn.gain.setValueAtTime(0.7, ctx.currentTime);
        gn.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.55);
        src.connect(gn); gn.connect(ctx.destination);
        src.start();

        var t = ctx.currentTime + 0.55;
        var osc = ctx.createOscillator();
        var g2  = ctx.createGain();
        osc.connect(g2); g2.connect(ctx.destination);
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(900,  t);
        osc.frequency.exponentialRampToValueAtTime(450,  t + 0.3);
        osc.frequency.exponentialRampToValueAtTime(1100, t + 0.6);
        osc.frequency.exponentialRampToValueAtTime(300,  t + 0.9);
        g2.gain.setValueAtTime(0.2, t);
        g2.gain.exponentialRampToValueAtTime(0.001, t + 0.9);
        osc.start(t); osc.stop(t + 0.9);
    } catch(e) {}
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

<div style="text-align:center; color:#FFD700; font-family:'Oswald',sans-serif; font-size:1.35rem; letter-spacing:5px; margin:6px 0;">
    🇺🇸 THE GREATEST · THE BOLDEST · THE MOST POWERFUL TAXI CALC IN THE KNOWN UNIVERSE 🇺🇸
</div>

<div style="text-align:center; margin:8px 0;">
    <span class="boom-row" style="font-size:2.4rem;">💥 🚕 🗽 🚁 ✈️ 🦅 ✈️ 🚁 🗽 🚕 💥</span>
</div>

<div style="text-align:center; color:#FFD700; font-size:1.3rem; letter-spacing:3px; margin:4px 0;">
    ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★
</div>
""", unsafe_allow_html=True)

# NYC TAXI ASCII BANNER
st.markdown("""
<div style="
    text-align:center;
    background: linear-gradient(135deg, rgba(178,34,52,0.15), rgba(60,59,110,0.4));
    border: 2px solid rgba(255,215,0,0.4);
    border-radius: 15px;
    padding: 16px;
    margin: 10px 0;
    font-family: monospace;
">
<pre style="color:#FFD700; display:inline-block; text-align:left; font-size:0.95rem; line-height:1.35; margin:0;">
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
#  MAP
# ════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<h2 style="text-align:center; margin-bottom:4px;">🗺️ LIVE OPERATIONAL THEATER — NEW YORK CITY 🗺️</h2>
<div style="text-align:center; color:#aaaadd; font-family:'Oswald',sans-serif; letter-spacing:3px; font-size:0.95rem; margin-bottom:12px;">
    REAL-TIME TACTICAL OVERVIEW · CLASSIFIED ROUTE DATA
</div>
""", unsafe_allow_html=True)

mid_lat = (pickup_latitude + dropoff_latitude) / 2
mid_lon = (pickup_longitude + dropoff_longitude) / 2

route_layer = pdk.Layer(
    "LineLayer",
    data=[{"start": [pickup_longitude, pickup_latitude],
           "end":   [dropoff_longitude, dropoff_latitude]}],
    get_source_position="start",
    get_target_position="end",
    get_color=[255, 215, 0, 210],
    get_width=7,
)

pickup_layer = pdk.Layer(
    "ScatterplotLayer",
    data=[{"position": [pickup_longitude, pickup_latitude]}],
    get_position="position",
    get_color=[0, 255, 100, 230],
    get_radius=220,
    pickable=True,
)

dropoff_layer = pdk.Layer(
    "ScatterplotLayer",
    data=[{"position": [dropoff_longitude, dropoff_latitude]}],
    get_position="position",
    get_color=[255, 80, 0, 230],
    get_radius=220,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=mid_lat,
    longitude=mid_lon,
    zoom=12,
    pitch=50,
    bearing=15,
)

deck = pdk.Deck(
    layers=[route_layer, pickup_layer, dropoff_layer],
    initial_view_state=view_state,
    map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
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
    <div style="color:#FFD700; font-family:'Oswald',sans-serif; font-size:1.5rem; letter-spacing:5px; margin:6px 0;">
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

    components.html(EXPLOSION_JS, height=0)

    with st.spinner("🦅  EAGLE IS COMPUTING… FREEDOM IS LOADING… DEMOCRACY IS CRUNCHING NUMBERS… 🦅"):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                fare = data.get('fare', data.get('fare_amount', 0))

                st.balloons()

                st.markdown(f"""
                <style>
                @keyframes result-pop {{ from {{ transform:scale(0.4); opacity:0; }} to {{ transform:scale(1); opacity:1; }} }}
                @keyframes money-glow {{ from {{ text-shadow: 0 0 30px rgba(0,255,136,0.7), 4px 4px 0 #006644; }}
                                         to   {{ text-shadow: 0 0 70px rgba(0,255,136,1),   4px 4px 0 #006644; }} }}
                </style>
                <div style="
                    text-align:center;
                    background: linear-gradient(135deg, rgba(40,40,110,0.97), rgba(178,34,52,0.25));
                    border: 5px solid #FFD700;
                    border-radius: 28px;
                    padding: 44px 30px;
                    margin: 20px 0;
                    box-shadow: 0 0 70px rgba(255,215,0,0.65), 0 0 140px rgba(255,69,0,0.3);
                    animation: result-pop 0.5s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
                ">
                    <div style="font-size:3.5rem; margin-bottom:10px;">💵 🦅 💵</div>
                    <div style="
                        font-family:'Bebas Neue',Impact,sans-serif;
                        font-size:3.8rem;
                        color:#FFD700;
                        text-shadow: 0 0 30px rgba(255,215,0,0.8), 4px 4px 0 #7a1010;
                        letter-spacing:8px; line-height:1;
                    ">ESTIMATED FARE</div>
                    <div style="
                        font-family:'Bebas Neue',Impact,sans-serif;
                        font-size:8.5rem;
                        color:#00FF88;
                        letter-spacing:4px; line-height:1.1;
                        animation: money-glow 1s ease infinite alternate;
                    ">${fare:.2f}</div>
                    <div style="color:#FFD700; font-size:1.25rem; letter-spacing:5px; margin-top:18px; font-family:'Oswald',sans-serif;">
                        🇺🇸 &nbsp; GOD BLESS AMERICA AND YOUR WALLET &nbsp; 🇺🇸
                    </div>
                    <div style="font-size:2.8rem; margin-top:16px;">🎆 🗽 🎆 🦅 🎆 🗽 🎆</div>
                </div>
                """, unsafe_allow_html=True)

                lat1 = math.radians(pickup_latitude);  lon1 = math.radians(pickup_longitude)
                lat2 = math.radians(dropoff_latitude); lon2 = math.radians(dropoff_longitude)
                a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
                dist_km = 6371 * 2 * math.asin(math.sqrt(a))

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("🗺️ DISTANCE",  f"{dist_km:.2f} km")
                with c2:
                    st.metric("💰 FARE",       f"${fare:.2f}")
                with c3:
                    label = f"{passenger_count} HERO{'S' if passenger_count > 1 else ''}"
                    st.metric("👥 PASSENGERS", label)

            else:
                st.error(f"⚠️ EAGLE FAILED TO RESPOND! STATUS CODE: {response.status_code}")
        except Exception as exc:
            st.error(f"⚠️ MISSION FAILED: {exc}")

# ════════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:22px 0 10px;">
    <div style="color:#FFD700; font-family:'Oswald',sans-serif; font-size:1.4rem; letter-spacing:5px;">
        ★ MADE WITH 🦅 PATRIOTISM AND 💥 MACHINE LEARNING ★
    </div>
    <div style="color:#7777aa; font-size:0.9rem; margin-top:8px; font-family:'Oswald',sans-serif; letter-spacing:2px;">
        Powered by Le Wagon Data Science Bootcamp &nbsp;|&nbsp; NYC Taxifare Prediction API
    </div>
    <div style="font-size:2.2rem; margin-top:10px;">🇺🇸 &nbsp; 🚕 &nbsp; 🗽 &nbsp; 🚕 &nbsp; 🇺🇸</div>
</div>
""", unsafe_allow_html=True)
