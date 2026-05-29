import streamlit as st
import requests
import pandas as pd
import datetime
import pydeck as pdk
import streamlit.components.v1 as components
import math
import random

st.set_page_config(
    page_title="GRAND THEFT TAXI: San Fierro",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── SESSION STATE ────────────────────────────────────────────────────────────
for key, val in [('respect',0),('fare_count',0),('total_earned',0.0),
                 ('show_result',False),('last_fare',0.0),('wanted',0),
                 ('cheat_msg',''),('radio','Radio Los Santos')]:
    if key not in st.session_state:
        st.session_state[key] = val

# ════════════════════════════════════════════════════════════════════
#  CSS — GTA SAN ANDREAS
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Russo+One&family=Oswald:wght@700&family=VT323&family=Share+Tech+Mono&display=swap');

/* SCANLINES + dark background */
.stApp {
    background-color: #0a150a;
    background-image:
        repeating-linear-gradient(0deg, transparent, transparent 3px,
            rgba(0,0,0,0.25) 3px, rgba(0,0,0,0.25) 4px),
        radial-gradient(ellipse at 50% 0%, rgba(74,124,53,0.15) 0%, transparent 70%);
}

/* Main container */
.main .block-container {
    background: rgba(8, 18, 8, 0.97);
    border: 2px solid #4a7c35;
    border-radius: 0px;
    padding: 0px 24px 24px 24px !important;
    max-width: 1200px;
    box-shadow: 0 0 40px rgba(74,124,53,0.4), inset 0 0 80px rgba(0,0,0,0.6);
}

/* H1 */
h1 {
    font-family: 'Russo One', 'Impact', sans-serif !important;
    font-size: 3.8rem !important;
    color: #f5c518 !important;
    text-shadow:
        -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000,
        0 0 30px rgba(245,197,24,0.7) !important;
    text-align: center !important;
    letter-spacing: 5px !important;
    text-transform: uppercase !important;
    line-height: 1.1 !important;
}

/* H2 */
h2 {
    font-family: 'Russo One', Impact, sans-serif !important;
    color: #ff8c00 !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    text-shadow: 1px 1px 0 #000, -1px 1px 0 #000 !important;
    border-left: 4px solid #4a7c35 !important;
    padding-left: 12px !important;
}

/* H3 */
h3 {
    font-family: 'Oswald', Impact, sans-serif !important;
    color: #7ab648 !important;
    letter-spacing: 3px !important;
    font-size: 1rem !important;
    text-transform: uppercase !important;
}

/* Text */
label, p, li, .stMarkdown p {
    color: #b8e0a0 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.9rem !important;
}

/* Inputs */
input[type="text"], input[type="number"], input[type="date"], input[type="time"] {
    background: rgba(0,0,0,0.85) !important;
    color: #ff8c00 !important;
    border: 1px solid #4a7c35 !important;
    border-radius: 2px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
    caret-color: #ff8c00 !important;
}
input:focus {
    border-color: #f5c518 !important;
    box-shadow: 0 0 8px rgba(245,197,24,0.4) !important;
    outline: none !important;
}

/* SELECT */
.stSelectbox > div > div {
    background: rgba(0,0,0,0.85) !important;
    border-color: #4a7c35 !important;
    color: #ff8c00 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* BUTTON — centered */
.stButton {
    display: flex !important;
    justify-content: center !important;
}
.stButton > button {
    background: linear-gradient(to bottom, #ff8c00 0%, #cc5500 50%, #993300 100%) !important;
    color: #fff !important;
    font-family: 'Russo One', Impact, sans-serif !important;
    font-size: 1.8rem !important;
    letter-spacing: 6px !important;
    border: 3px solid #f5c518 !important;
    border-radius: 3px !important;
    padding: 16px 70px !important;
    width: 100% !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
    box-shadow: 0 0 25px rgba(255,140,0,0.5), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    text-transform: uppercase !important;
    animation: mission-pulse 2s ease infinite alternate !important;
    cursor: pointer !important;
}
@keyframes mission-pulse {
    from { box-shadow: 0 0 15px rgba(255,140,0,0.4); }
    to   { box-shadow: 0 0 40px rgba(255,140,0,0.9), 0 0 80px rgba(255,140,0,0.3); }
}
.stButton > button:hover { filter: brightness(1.2) !important; transform: scale(1.01) !important; }
.stButton > button:active { filter: brightness(0.9) !important; transform: scale(0.99) !important; }

/* SLIDER */
[data-baseweb="slider"] div[role="slider"] {
    background: #ff8c00 !important;
    border-color: #f5c518 !important;
}

/* METRICS */
[data-testid="stMetricValue"] {
    font-family: 'VT323', monospace !important;
    font-size: 2.8rem !important;
    color: #f5c518 !important;
    text-shadow: 0 0 10px rgba(245,197,24,0.6) !important;
}
[data-testid="stMetricLabel"] {
    color: #7ab648 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

/* COLUMNS */
[data-testid="column"] {
    background: rgba(0, 20, 0, 0.6) !important;
    border: 1px solid rgba(74,124,53,0.4) !important;
    padding: 14px !important;
}

/* SPINNER */
.stSpinner > div { border-color: #ff8c00 transparent #ff8c00 transparent !important; }

/* HIDE STREAMLIT */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* SCROLLBAR */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #0a150a; }
::-webkit-scrollbar-thumb { background: #4a7c35; }

/* STEPPERS */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: rgba(0,30,0,0.8) !important;
    color: #7ab648 !important;
    border: 1px solid #4a7c35 !important;
}

/* BLINK */
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0;} }
.blink { animation: blink 0.8s step-start infinite; }

/* WARNING/ERROR */
.stWarning { background: rgba(200,100,0,0.2) !important; border-color: #ff8c00 !important; }
.stError   { background: rgba(200,0,0,0.2) !important; border-color: #ff0000 !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  AUDIO
# ════════════════════════════════════════════════════════════════════
RADIO_URLS = {
    "Radio Los Santos": "https://archive.org/download/gtasars/Radio%20Los%20Santos.mp3",
    "K-DST":            "https://archive.org/download/gtasars/K-DST.mp3",
    "Playback FM":      "https://archive.org/download/gtasars/Playback%20FM.mp3",
    "SF-UR":            "https://archive.org/download/gtasars/SF-UR.mp3",
    "CSR 103.9":        "https://archive.org/download/gtasars/CSR%20103.9.mp3",
    "K-Rose":           "https://archive.org/download/gtasars/K-Rose.mp3",
}

DISPATCH_JS = """
<html><body style="margin:0;background:transparent;">
<script>
(function(){
    try {
        var AC = window.AudioContext || window.webkitAudioContext;
        var ctx = new AC();
        // Radio static crackle
        var sr = ctx.sampleRate;
        var buf = ctx.createBuffer(1, sr*0.4, sr);
        var d = buf.getChannelData(0);
        for(var i=0;i<d.length;i++) d[i]=(Math.random()*2-1)*Math.exp(-i/(sr*0.05));
        var s = ctx.createBufferSource(); s.buffer = buf;
        var g = ctx.createGain(); g.gain.setValueAtTime(0.5, ctx.currentTime);
        s.connect(g); g.connect(ctx.destination); s.start();
        // Dispatch beep
        var osc = ctx.createOscillator(); var g2 = ctx.createGain();
        osc.connect(g2); g2.connect(ctx.destination);
        osc.frequency.value = 1200; osc.type = 'square';
        g2.gain.setValueAtTime(0.3, ctx.currentTime+0.05);
        g2.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime+0.25);
        osc.start(ctx.currentTime+0.05); osc.stop(ctx.currentTime+0.25);
    } catch(e){}
})();
</script>
</body></html>
"""

MISSION_COMPLETE_JS = """
<html><body style="margin:0;background:transparent;">
<script>
(function(){
    try {
        var AC = window.AudioContext || window.webkitAudioContext;
        var ctx = new AC();
        // Mission complete ascending arpeggio
        var notes = [261.63, 329.63, 392.00, 523.25, 659.25, 783.99];
        notes.forEach(function(f,i){
            var o=ctx.createOscillator(); var g=ctx.createGain();
            o.connect(g); g.connect(ctx.destination);
            o.type='square'; o.frequency.value=f;
            var t=ctx.currentTime+i*0.1;
            g.gain.setValueAtTime(0.25,t);
            g.gain.exponentialRampToValueAtTime(0.001,t+0.4);
            o.start(t); o.stop(t+0.4);
        });
        // Final chord
        [523.25, 659.25, 783.99].forEach(function(f){
            var o=ctx.createOscillator(); var g=ctx.createGain();
            o.connect(g); g.connect(ctx.destination);
            o.type='square'; o.frequency.value=f;
            var t=ctx.currentTime+0.7;
            g.gain.setValueAtTime(0.2,t);
            g.gain.exponentialRampToValueAtTime(0.001,t+0.8);
            o.start(t); o.stop(t+0.8);
        });
    } catch(e){}
})();
</script>
</body></html>
"""

WASTED_JS = """
<html><body style="margin:0;background:transparent;">
<script>
(function(){
    try {
        var AC = window.AudioContext || window.webkitAudioContext;
        var ctx = new AC();
        var osc = ctx.createOscillator(); var g = ctx.createGain();
        osc.connect(g); g.connect(ctx.destination);
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(440, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(55, ctx.currentTime+2.5);
        g.gain.setValueAtTime(0.3, ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime+2.5);
        osc.start(ctx.currentTime); osc.stop(ctx.currentTime+2.5);
    } catch(e){}
})();
</script>
</body></html>
"""

# ════════════════════════════════════════════════════════════════════
#  GTA SA LOADING SCREEN (fades after 2.5s)
# ════════════════════════════════════════════════════════════════════
components.html("""
<html><body style="margin:0;padding:0;background:transparent;">
<style>
@import url('https://fonts.googleapis.com/css2?family=Russo+One&display=swap');
@keyframes fadeOut {
    0%,60% { opacity:1; max-height:300px; }
    95%,100% { opacity:0; max-height:0; overflow:hidden; padding:0; }
}
.loader {
    background: #000;
    padding: 30px;
    text-align: center;
    border: 2px solid #4a7c35;
    animation: fadeOut 3s ease-out 0.5s forwards;
}
.gta-logo {
    font-family: 'Russo One', Impact, sans-serif;
    font-size: 2.8rem;
    color: #f5c518;
    text-shadow: -2px -2px 0 #000, 2px 2px 0 #000, 0 0 20px #f5c518;
    letter-spacing: 6px;
}
.sub { color: #7ab648; font-family: 'Russo One', sans-serif; font-size:1rem; letter-spacing:8px; margin:4px 0 16px; }
.bar-bg { background:#1a1a1a; border:1px solid #4a7c35; height:18px; width:80%; margin:0 auto; border-radius:2px; }
.bar-fill {
    height:100%; background:linear-gradient(to right,#4a7c35,#7ab648);
    border-radius:2px;
    animation: load 2.5s ease-out 0.5s forwards;
    width: 0%;
}
@keyframes load { to { width: 100%; } }
.dots { color:#7ab648; font-size:0.85rem; letter-spacing:4px; margin-top:8px; font-family:monospace; }
</style>
<div class="loader">
    <div class="gta-logo">GRAND THEFT TAXI</div>
    <div class="sub">SAN FIERRO</div>
    <div class="bar-bg"><div class="bar-fill"></div></div>
    <div class="dots">LOADING TAXI MISSION...</div>
</div>
</body></html>
""", height=160)

# ════════════════════════════════════════════════════════════════════
#  GTA HUD — Health · Armor · Cash · Stars · Radio
# ════════════════════════════════════════════════════════════════════
wanted_stars = st.session_state['wanted']
star_display = "★" * wanted_stars + "☆" * (6 - wanted_stars)
cash_display  = f"${st.session_state['total_earned']:,.2f}"
respect_pct   = min(100, st.session_state['respect'])
missions_done = st.session_state['fare_count']
health_pct    = 100

components.html(f"""
<html><body style="margin:0;padding:0;background:transparent;">
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Russo+One&display=swap');
.hud {{
    background: rgba(0,0,0,0.85);
    border: 1px solid #4a7c35;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'VT323', monospace;
    flex-wrap: wrap;
    gap: 10px;
}}
.hud-section {{ display:flex; flex-direction:column; gap:4px; }}
.bar-label {{ color:#7ab648; font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; }}
.bar-wrap {{ width:140px; height:12px; background:#1a1a1a; border:1px solid #333; border-radius:2px; }}
.bar-fill-hp  {{ height:100%; background:linear-gradient(to right,#00aa00,#00ff00); border-radius:2px; width:{health_pct}%; }}
.bar-fill-res {{ height:100%; background:linear-gradient(to right,#0055ff,#00aaff); border-radius:2px; width:{respect_pct}%; }}
.cash {{ color:#f5c518; font-size:2.2rem; text-shadow:0 0 10px rgba(245,197,24,0.6); letter-spacing:2px; }}
.stars {{ color:#f5c518; font-size:1.8rem; letter-spacing:4px; text-shadow:0 0 8px rgba(245,197,24,0.5); }}
.stars .off {{ color:#333; }}
.cj-name {{ color:#7ab648; font-size:0.85rem; letter-spacing:3px; text-transform:uppercase; }}
.stat-val {{ color:#fff; font-size:1.1rem; }}
.mission-tag {{ color:#ff8c00; font-size:0.85rem; letter-spacing:2px; text-align:right; }}
</style>
<div class="hud">
    <div class="hud-section">
        <span class="cj-name">CJ</span>
        <div class="bar-label">HEALTH</div>
        <div class="bar-wrap"><div class="bar-fill-hp"></div></div>
        <div class="bar-label">RESPECT</div>
        <div class="bar-wrap"><div class="bar-fill-res"></div></div>
    </div>
    <div class="hud-section" style="text-align:center;">
        <div class="mission-tag">▶ TAXI DRIVER MISSION</div>
        <div style="color:#7ab648;font-size:0.75rem;letter-spacing:3px;">GROVE STREET FAMILIES</div>
        <div class="stat-val" style="color:#b8e0a0;font-size:0.85rem;margin-top:4px;">
            MISSIONS: {missions_done} &nbsp;|&nbsp; TERRITORY: GROVE ST
        </div>
    </div>
    <div class="hud-section" style="text-align:right;">
        <div class="cash">{cash_display}</div>
        <div class="bar-label" style="text-align:right;">WANTED LEVEL</div>
        <div class="stars">{star_display}</div>
    </div>
</div>
</body></html>
""", height=100)

# ════════════════════════════════════════════════════════════════════
#  TITLE
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@keyframes glitch {
    0%,95%,100% { text-shadow: -3px -3px 0 #000, 3px 3px 0 #000, 0 0 30px rgba(245,197,24,0.7); transform: none; }
    96% { text-shadow: -3px -3px 0 #ff0000, 3px 3px 0 #00ff00; transform: translate(-2px, 1px); }
    97% { text-shadow: 3px 3px 0 #ff0000, -3px -3px 0 #00ff00; transform: translate(2px, -1px); }
    98% { text-shadow: -3px -3px 0 #000, 3px 3px 0 #000, 0 0 30px rgba(245,197,24,0.7); transform: none; }
}
.gta-title { animation: glitch 6s infinite; display:inline-block; }
@keyframes subtitle-scan {
    0%,100% { color:#7ab648; }
    50% { color:#b8e0a0; }
}
</style>

<div style="text-align:center; padding:20px 0 8px; border-bottom:2px solid #4a7c35; margin-bottom:16px;">
    <div style="color:#7ab648; font-family:'Share Tech Mono',monospace; font-size:0.8rem;
                letter-spacing:8px; margin-bottom:8px;">ROCKSTAR GAMES PRESENTS</div>
    <h1><span class="gta-title">🚕 GRAND THEFT TAXI 🚕</span></h1>
    <div style="color:#ff8c00; font-family:'Russo One',Impact,sans-serif; font-size:1.3rem;
                letter-spacing:10px; text-shadow:1px 1px 0 #000; margin:6px 0;">
        SAN FIERRO
    </div>
    <div style="color:#7ab648; font-family:'Share Tech Mono',monospace; font-size:0.8rem;
                letter-spacing:4px; animation: subtitle-scan 3s ease infinite;">
        ◉ TAXI DRIVER MISSION ACTIVE ◉
    </div>
</div>

<div style="display:flex; justify-content:center; gap:40px; margin:10px 0;
            font-family:'Share Tech Mono',monospace; font-size:0.75rem; color:#4a7c35;
            letter-spacing:3px;">
    <span>◈ LOS SANTOS</span>
    <span>◈ SAN FIERRO</span>
    <span>◈ LAS VENTURAS</span>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  RADIO STATION SELECTOR
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:rgba(0,0,0,0.7); border:1px solid #4a7c35; padding:12px 16px; margin:12px 0;
            display:flex; align-items:center; gap:12px;">
    <div style="font-family:'VT323',monospace; color:#f5c518; font-size:1.6rem;">📻</div>
    <div>
        <div style="color:#7ab648; font-family:'Share Tech Mono',monospace;
                    font-size:0.7rem; letter-spacing:3px;">IN-CAR RADIO</div>
    </div>
</div>
""", unsafe_allow_html=True)

radio_col, vol_col = st.columns([3, 1])
with radio_col:
    station = st.selectbox(
        "Radio Station",
        list(RADIO_URLS.keys()),
        index=list(RADIO_URLS.keys()).index(st.session_state['radio']),
        label_visibility="collapsed"
    )
    st.session_state['radio'] = station
with vol_col:
    radio_vol = st.slider("Vol", 0, 100, 40, label_visibility="collapsed")

radio_url = RADIO_URLS[station]
components.html(f"""
<html><body style="margin:0;padding:0;background:transparent;">
<audio id="radio" loop>
  <source src="{radio_url}" type="audio/mpeg">
</audio>
<script>
var audio = document.getElementById('radio');
audio.volume = {radio_vol / 100};
audio.play().catch(function(){{}});
</script>
</body></html>
""", height=1)

st.markdown("""
<div style="font-family:'Share Tech Mono',monospace; color:#4a7c35; font-size:0.7rem;
            letter-spacing:2px; text-align:center; margin:-8px 0 8px;">
    ▸ NOW PLAYING — USE SELECTOR TO CHANGE STATION ▸
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #4a7c35; margin:12px 0;'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  MISSION BRIEFING — INPUTS
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:rgba(0,0,0,0.8); border:2px solid #ff8c00; padding:14px 18px; margin:8px 0;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
        <div style="width:8px;height:8px;background:#ff8c00;border-radius:50%;
                    box-shadow:0 0 8px #ff8c00;"></div>
        <span style="color:#ff8c00; font-family:'Russo One',Impact,sans-serif;
                     font-size:1rem; letter-spacing:5px;">MISSION BRIEFING</span>
        <div style="width:8px;height:8px;background:#ff8c00;border-radius:50%;
                    box-shadow:0 0 8px #ff8c00;"></div>
    </div>
    <div style="color:#7ab648; font-family:'Share Tech Mono',monospace; font-size:0.8rem;
                letter-spacing:1px; line-height:1.6;">
        <em>Sweet called. He needs a ride from Grove Street to the other side of town.
        Pick him up and don't take the scenic route — po-po got eyes everywhere.
        Estimated fare will be calculated. Watch your wanted level.</em>
    </div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div style="background:rgba(0,40,0,0.5); border:1px solid #4a7c35; padding:10px; margin-bottom:10px;">
        <span style="color:#7ab648; font-family:'Russo One',sans-serif;
                     font-size:0.85rem; letter-spacing:3px;">📅 MISSION DATE & TIME</span>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<span style='color:#4a7c35;font-family:monospace;font-size:0.75rem;'>DATE</span>", unsafe_allow_html=True)
        pickup_date = st.date_input("Date", min_value=datetime.date(2009,1,1), label_visibility="collapsed")
    with c2:
        st.markdown("<span style='color:#4a7c35;font-family:monospace;font-size:0.75rem;'>TIME</span>", unsafe_allow_html=True)
        pickup_time = st.time_input("Time", label_visibility="collapsed")

    st.markdown("""
    <div style="background:rgba(0,40,0,0.5); border:1px solid #4a7c35; padding:10px; margin:10px 0;">
        <span style="color:#7ab648; font-family:'Russo One',sans-serif;
                     font-size:0.85rem; letter-spacing:3px;">👥 HOMIES IN THE CAR</span>
    </div>
    """, unsafe_allow_html=True)
    passenger_count = st.slider("Homies", min_value=1, max_value=8, value=1, label_visibility="collapsed")
    homie_icons = "😎" * passenger_count
    st.markdown(f"<div style='text-align:center;font-size:1.6rem;'>{homie_icons}</div>", unsafe_allow_html=True)

    # BIG SMOKE EASTER EGG
    if passenger_count == 8:
        st.markdown("""
        <div style="background:rgba(100,50,0,0.6); border:2px solid #ff8c00;
                    padding:10px; margin:8px 0; font-family:'Share Tech Mono',monospace;">
            <div style="color:#f5c518; font-size:0.85rem; letter-spacing:1px;">
                🍔 <strong>BIG SMOKE:</strong><br>
                "I'll have two number 9s, a number 9 large,<br>
                a number 6 with extra dip, two number 45s,<br>
                one with cheese, and a large soda."
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div style="background:rgba(0,60,0,0.4); border:1px solid #7ab648; padding:10px; margin-bottom:8px;">
        <span style="color:#7ab648; font-family:'Russo One',sans-serif;
                     font-size:0.85rem; letter-spacing:3px;">🟢 WAYPOINT A — PICKUP</span>
    </div>
    """, unsafe_allow_html=True)
    pickup_address = st.text_input("Pickup", value="Grove Street, Los Santos, CA", key="p_addr", label_visibility="collapsed")

    st.markdown("""
    <div style="background:rgba(60,0,0,0.4); border:1px solid #cc2222; padding:10px; margin:8px 0;">
        <span style="color:#ff4444; font-family:'Russo One',sans-serif;
                     font-size:0.85rem; letter-spacing:3px;">🔴 WAYPOINT B — DROPOFF</span>
    </div>
    """, unsafe_allow_html=True)
    dropoff_address = st.text_input("Dropoff", value="Vinewood Hills, Los Santos, CA", key="d_addr", label_visibility="collapsed")

    # RANDOM CJ QUOTE
    quotes = [
        '"Grove Street. Home. At least it was before I messed everything up."',
        '"All we had to do was follow the damn train, CJ!"',
        '"You picked the wrong house, fool!"',
        '"Big Smoke! You set us up!"',
        '"This is the beginning of a new era for Grove Street."',
    ]
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.5); border-left:3px solid #4a7c35;
                padding:10px; margin-top:12px;">
        <div style="color:#7ab648; font-size:0.7rem; letter-spacing:2px;
                    font-family:'Share Tech Mono',monospace;">CJ SAYS:</div>
        <div style="color:#b8e0a0; font-size:0.8rem; font-family:'Share Tech Mono',monospace;
                    font-style:italic; margin-top:4px;">
            {random.choice(quotes)}
        </div>
    </div>
    """, unsafe_allow_html=True)

pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)

# ════════════════════════════════════════════════════════════════════
#  GEOCODING
# ════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400)
def geocode_address(address):
    headers = {"User-Agent": "GrandTheftTaxiApp/1.0"}
    params  = {"q": address, "format": "json", "limit": 1, "countrycodes": "us"}
    try:
        r = requests.get("https://nominatim.openstreetmap.org/search",
                         params=params, headers=headers, timeout=5)
        if r.status_code == 200 and r.json():
            res = r.json()[0]
            return float(res['lat']), float(res['lon'])
    except Exception:
        pass
    return None, None

pickup_lat,  pickup_lon  = geocode_address(pickup_address)
dropoff_lat, dropoff_lon = geocode_address(dropoff_address)

if pickup_lat is None:
    pickup_lat,  pickup_lon  = 40.783282, -73.950655
if dropoff_lat is None:
    dropoff_lat, dropoff_lon = 40.769802, -73.984365

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
        r = requests.post("https://overpass-api.de/api/interpreter",
                          data={"data": query}, timeout=20)
        buildings = []
        for el in r.json().get('elements', []):
            if 'geometry' not in el: continue
            coords = [[n['lon'], n['lat']] for n in el['geometry']]
            if len(coords) < 3: continue
            tags = el.get('tags', {})
            try:    height = float(tags.get('height', tags.get('building:levels','3'))) * 3.5
            except: height = 12
            buildings.append({'polygon': coords, 'height': min(float(height), 400)})
        return buildings
    except Exception:
        return []

# ════════════════════════════════════════════════════════════════════
#  MAP — GTA SA STYLE
# ════════════════════════════════════════════════════════════════════
st.markdown("<hr style='border:1px solid #4a7c35; margin:12px 0;'>", unsafe_allow_html=True)
st.markdown("<h2 style='margin-bottom:4px;'>🗺️ TACTICAL MAP — GPS ACTIVE</h2>", unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Share Tech Mono',monospace; color:#4a7c35; font-size:0.75rem;
            letter-spacing:3px; margin-bottom:10px;">
    ROUTE CALCULATION IN PROGRESS... AVOID POLICE CHECKPOINTS
</div>
""", unsafe_allow_html=True)

mid_lat = (pickup_lat + dropoff_lat) / 2
mid_lon = (pickup_lon + dropoff_lon) / 2

pad = 0.008
bmin_lat = min(pickup_lat, dropoff_lat)   - pad
bmax_lat = max(pickup_lat, dropoff_lat)   + pad
bmin_lon = min(pickup_lon, dropoff_lon)   - pad
bmax_lon = max(pickup_lon, dropoff_lon)   + pad

with st.spinner("🔫 Loading gang territories & street data..."):
    route_coords = get_osrm_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    buildings    = get_buildings(bmin_lat, bmin_lon, bmax_lat, bmax_lon)

# Auto zoom
dlat = abs(pickup_lat - dropoff_lat)
dlon = abs(pickup_lon - dropoff_lon)
max_d = max(dlat, dlon)
if   max_d < 0.01:  z = 15
elif max_d < 0.03:  z = 14
elif max_d < 0.07:  z = 13
elif max_d < 0.15:  z = 12
elif max_d < 0.4:   z = 11
else:               z = 10

# GTA SA map layers — orange route, green/red waypoints
route_layer = pdk.Layer("PathLayer",
    data=[{"path": route_coords}],
    get_path="path",
    get_color=[255, 140, 0, 240],  # GTA GPS orange
    get_width=10, width_min_pixels=4,
)
pickup_layer = pdk.Layer("ScatterplotLayer",
    data=[{"position": [pickup_lon, pickup_lat]}],
    get_position="position",
    get_color=[74, 124, 53, 255],   # Grove green
    get_radius=180, stroked=True, line_width_min_pixels=4,
    get_line_color=[122, 182, 72, 255],
)
dropoff_layer = pdk.Layer("ScatterplotLayer",
    data=[{"position": [dropoff_lon, dropoff_lat]}],
    get_position="position",
    get_color=[200, 20, 20, 255],   # Target red
    get_radius=180, stroked=True, line_width_min_pixels=4,
    get_line_color=[255, 60, 60, 255],
)
building_layer = pdk.Layer("PolygonLayer",
    data=buildings,
    get_polygon="polygon", get_elevation="height",
    elevation_scale=1, extruded=True,
    get_fill_color=[30, 50, 20, 200],   # Dark green tint (GTA SA vibe)
    get_line_color=[74, 124, 53, 80],
    line_width_min_pixels=1, pickable=False,
)

view_state = pdk.ViewState(latitude=mid_lat, longitude=mid_lon,
                           zoom=z, pitch=45, bearing=0)
layers = [route_layer, pickup_layer, dropoff_layer]
if buildings:
    layers = [building_layer] + layers

deck = pdk.Deck(
    layers=layers,
    initial_view_state=view_state,
    map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
)
st.pydeck_chart(deck, use_container_width=True, height=520)

# ── MINI RADAR (fake, stylized) ──────────────────────────────────────────────
_, radar_col, _ = st.columns([3, 1, 3])
with radar_col:
    components.html("""
<html><body style="margin:0;padding:0;background:transparent;display:flex;justify-content:center;">
<canvas id="r" width="130" height="130"></canvas>
<script>
var c=document.getElementById('r'),ctx=c.getContext('2d');
// Background
ctx.fillStyle='rgba(0,20,0,0.95)';
ctx.beginPath(); ctx.arc(65,65,63,0,Math.PI*2); ctx.fill();
// Grid rings
[20,40,60].forEach(function(r){
    ctx.strokeStyle='rgba(74,124,53,0.3)'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.arc(65,65,r,0,Math.PI*2); ctx.stroke();
});
// Cross lines
ctx.strokeStyle='rgba(74,124,53,0.25)'; ctx.lineWidth=1;
ctx.beginPath(); ctx.moveTo(65,5); ctx.lineTo(65,125); ctx.stroke();
ctx.beginPath(); ctx.moveTo(5,65); ctx.lineTo(125,65); ctx.stroke();
// Sweep animation
var angle = 0;
function sweep(){
    // Redraw bg
    ctx.fillStyle='rgba(0,20,0,0.15)';
    ctx.beginPath(); ctx.arc(65,65,63,0,Math.PI*2); ctx.fill();
    // Sweep
    var grad = ctx.createConicalGradient ? null : null;
    ctx.save();
    ctx.translate(65,65);
    ctx.rotate(angle);
    var g=ctx.createLinearGradient(0,0,60,0);
    g.addColorStop(0,'rgba(122,182,72,0.8)');
    g.addColorStop(1,'rgba(122,182,72,0)');
    ctx.fillStyle=g;
    ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0,62,-0.4,0.4); ctx.closePath(); ctx.fill();
    ctx.restore();
    // Pickup blip (green)
    ctx.fillStyle='#7ab648';
    ctx.shadowColor='#7ab648'; ctx.shadowBlur=6;
    ctx.beginPath(); ctx.arc(42,38,5,0,Math.PI*2); ctx.fill();
    // Dropoff blip (red)
    ctx.fillStyle='#ff2222';
    ctx.shadowColor='#ff2222'; ctx.shadowBlur=6;
    ctx.beginPath(); ctx.arc(88,92,5,0,Math.PI*2); ctx.fill();
    ctx.shadowBlur=0;
    // N indicator
    ctx.fillStyle='#f5c518'; ctx.font='bold 11px monospace';
    ctx.fillText('N',60,14);
    angle += 0.04;
    requestAnimationFrame(sweep);
}
sweep();
// Border
ctx.strokeStyle='#4a7c35'; ctx.lineWidth=3;
ctx.beginPath(); ctx.arc(65,65,63,0,Math.PI*2); ctx.stroke();
</script>
</body></html>
""", height=135)
    st.markdown("<div style='text-align:center;color:#4a7c35;font-family:monospace;font-size:0.65rem;letter-spacing:2px;'>RADAR</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  WANTED LEVEL PREVIEW
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:rgba(0,0,0,0.6); border:1px solid #333; padding:10px 16px; margin:10px 0;
            font-family:'Share Tech Mono',monospace; font-size:0.75rem;
            display:flex; gap:30px; flex-wrap:wrap;">
    <span style="color:#4a7c35;">◈ GREEN DOT = PICKUP</span>
    <span style="color:#ff4444;">◈ RED DOT = DROPOFF</span>
    <span style="color:#ff8c00;">◈ ORANGE LINE = GPS ROUTE</span>
    <span style="color:#7ab648;">◈ DARK BUILDINGS = GANG TERRITORY</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #4a7c35; margin:12px 0;'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  START MISSION BUTTON
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; margin:10px 0 8px;">
    <span class="blink" style="color:#ff8c00; font-family:'Share Tech Mono',monospace;
                               font-size:0.85rem; letter-spacing:4px;">
        ▼ CALCULATE TAXI FARE ▼
    </span>
</div>
""", unsafe_allow_html=True)

url = 'https://taxifare.lewagon.ai/predict'
params = {
    'pickup_datetime':   str(pd.Timestamp(pickup_datetime)),
    'pickup_longitude':  float(pickup_lon),
    'pickup_latitude':   float(pickup_lat),
    'dropoff_longitude': float(dropoff_lon),
    'dropoff_latitude':  float(dropoff_lat),
    'passenger_count':   int(passenger_count),
}

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    clicked = st.button("🚕 START MISSION — CALCULATE FARE 🚕", use_container_width=True)

if clicked:
    st.session_state['show_result'] = False
    components.html(DISPATCH_JS, height=1)
    with st.spinner("📡 Dispatch radioing fare estimate... Stay low, CJ..."):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                fare = float(data.get('fare', data.get('fare_amount', 0)))
                st.session_state['last_fare']    = fare
                st.session_state['total_earned'] += fare
                st.session_state['fare_count']   += 1
                st.session_state['respect']       = min(100, st.session_state['respect'] + 10)
                # Wanted level based on fare
                if   fare < 10:  w = 0
                elif fare < 25:  w = 1
                elif fare < 50:  w = 2
                elif fare < 100: w = 3
                elif fare < 200: w = 4
                else:            w = 5
                st.session_state['wanted']       = w
                st.session_state['show_result']  = True
            else:
                components.html(WASTED_JS, height=1)
                st.error(f"WASTED — API Status: {response.status_code}")
        except Exception as exc:
            components.html(WASTED_JS, height=1)
            st.error(f"WASTED — {exc}")

# ════════════════════════════════════════════════════════════════════
#  MISSION PASSED RESULT
# ════════════════════════════════════════════════════════════════════
if st.session_state.get('show_result'):
    fare        = st.session_state['last_fare']
    fare_count  = st.session_state['fare_count']
    total       = st.session_state['total_earned']
    wanted_lv   = st.session_state['wanted']
    stars_str   = "★" * wanted_lv + "☆" * (6 - wanted_lv)

    components.html(MISSION_COMPLETE_JS, height=1)

    # Haversine distance
    lat1,lon1 = math.radians(pickup_lat), math.radians(pickup_lon)
    lat2,lon2 = math.radians(dropoff_lat), math.radians(dropoff_lon)
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    dist_km = 6371 * 2 * math.asin(math.sqrt(a))

    # MISSION PASSED screen
    st.markdown(f"""
    <style>
    @keyframes mission-passed {{
        0%   {{ opacity:0; transform:scale(2); }}
        20%  {{ opacity:1; transform:scale(1); }}
        80%  {{ opacity:1; transform:scale(1); }}
        100% {{ opacity:1; transform:scale(1); }}
    }}
    @keyframes cash-count {{
        from {{ color:#ff8c00; }} to {{ color:#f5c518; }}
    }}
    </style>
    <div style="
        text-align:center;
        background: linear-gradient(180deg, rgba(0,20,0,0.98) 0%, rgba(0,40,0,0.95) 100%);
        border: 3px solid #7ab648;
        border-radius: 4px;
        padding: 40px 30px;
        margin: 16px 0;
        box-shadow: 0 0 60px rgba(74,124,53,0.5), inset 0 0 40px rgba(0,0,0,0.5);
        animation: mission-passed 0.6s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
        font-family: 'Russo One', Impact, sans-serif;
    ">
        <div style="color:#7ab648; font-size:0.9rem; letter-spacing:8px;
                    font-family:'Share Tech Mono',monospace; margin-bottom:8px;">
            ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓
        </div>
        <div style="color:#f5c518; font-size:3.5rem; letter-spacing:8px;
                    text-shadow: -2px -2px 0 #000, 2px 2px 0 #000, 0 0 30px #f5c518;
                    margin: 8px 0;">
            TAXI MISSION PASSED!
        </div>
        <div style="color:#7ab648; font-size:0.9rem; letter-spacing:8px;
                    font-family:'Share Tech Mono',monospace; margin-bottom:24px;">
            ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓
        </div>
        <div style="color:#f5c518; font-size:5rem; letter-spacing:4px;
                    text-shadow: -3px -3px 0 #000, 3px 3px 0 #000;
                    animation: cash-count 0.5s ease infinite alternate;">
            ${fare:.2f}
        </div>
        <div style="color:#b8e0a0; font-size:1rem; letter-spacing:6px;
                    font-family:'Share Tech Mono',monospace; margin-top:10px;">
            💰 FARE COLLECTED — RESPECT GAINED +10
        </div>
        <div style="display:flex; justify-content:center; gap:30px; margin-top:20px;
                    font-family:'Share Tech Mono',monospace; font-size:0.8rem;">
            <div style="color:#7ab648;">DISTANCE: {dist_km:.1f} km</div>
            <div style="color:#ff8c00;">PASSENGERS: {passenger_count}</div>
            <div style="color:#f5c518;">WANTED: {stars_str}</div>
        </div>
        <div style="color:#4a7c35; font-size:0.75rem; letter-spacing:3px;
                    font-family:'Share Tech Mono',monospace; margin-top:16px;">
            TOTAL MISSIONS: {fare_count} &nbsp;|&nbsp; TOTAL EARNED: ${total:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats columns
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💰 FARE",       f"${fare:.2f}")
    with c2:
        st.metric("🗺️ DISTANCE",   f"{dist_km:.1f} km")
    with c3:
        st.metric("⭐ WANTED LV",  f"{wanted_lv}/6")
    with c4:
        st.metric("💎 TOTAL",      f"${total:.2f}")

# ════════════════════════════════════════════════════════════════════
#  CRAZY TAXI GAME
# ════════════════════════════════════════════════════════════════════
if st.session_state.get('show_result'):
    st.markdown("<hr style='border:1px solid #4a7c35; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; font-family:'Russo One',Impact,sans-serif;
                color:#f5c518; font-size:1.5rem; letter-spacing:6px; margin-bottom:6px;">
        🚕 CRAZY TAXI — NEW YORK CITY 🚕
    </div>
    <div style="text-align:center; font-family:'Share Tech Mono',monospace;
                color:#7ab648; font-size:0.75rem; letter-spacing:3px; margin-bottom:8px;">
        WASD / ARROW KEYS TO DRIVE · PICK UP FARES · AVOID WALLS
    </div>
    """, unsafe_allow_html=True)
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#0a150a; display:flex; flex-direction:column; align-items:center; padding:8px; font-family:monospace; }
canvas { border:2px solid #4a7c35; display:block; box-shadow:0 0 20px rgba(74,124,53,0.4); }
#ui { color:#f5c518; font-size:13px; margin-top:6px; display:flex; gap:24px; letter-spacing:2px; flex-wrap:wrap; justify-content:center; }
#ui span { color:#7ab648; }
#msg { color:#ff8c00; font-size:0.95rem; letter-spacing:2px; min-height:22px; margin-top:4px; text-align:center; }
</style>
</head>
<body>
<canvas id="c" width="780" height="460"></canvas>
<div id="ui">
  <div><span>SPEED:</span> <b id="spd">0</b> mph</div>
  <div><span>FARE:</span> $<b id="fare">0.00</b></div>
  <div><span>DELIVERED:</span> <b id="pax">0</b></div>
  <div><span>TOTAL:</span> $<b id="score">0.00</b></div>
</div>
<div id="msg">FIND A 🙋 PASSENGER AND DELIVER THEM!</div>
<script>
const W=780, H=460, T=60;
const cv=document.getElementById('c'), ctx=cv.getContext('2d');

// 0=road  1=building  2=park
const MAP=[
  [1,1,1,0,1,1,1,0,1,1,1,0,1,1],
  [1,1,1,0,1,1,1,0,1,1,1,0,1,1],
  [1,1,1,0,1,1,1,0,2,2,2,0,1,1],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [1,1,1,0,1,1,1,0,1,1,1,0,1,1],
  [1,1,1,0,2,2,2,0,1,1,1,0,1,1],
  [1,1,1,0,1,1,1,0,1,1,1,0,1,1],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
];
const ROWS=MAP.length, COLS=MAP[0].length;
const BLDG=['#1a2e1a','#162a16','#1e321e'];

/* ---- road tile helpers ---- */
const roadSet=new Set();
MAP.forEach((row,ry)=>row.forEach((cell,rx)=>{ if(cell===0) roadSet.add(ry*100+rx); }));
function isRoad(rx,ry){ return rx>=0&&ry>=0&&rx<COLS&&ry<ROWS&&MAP[ry][rx]===0; }
function tileAt(wx,wy){ return isRoad(Math.floor(wx/T),Math.floor(wy/T))?0:1; }

const roadTiles=[];
roadSet.forEach(k=>{ const ry=Math.floor(k/100),rx=k%100; roadTiles.push({rx,ry,x:rx*T+T/2,y:ry*T+T/2}); });

function randRoadPos(excludePos){
  for(let i=0;i<200;i++){
    const t=roadTiles[Math.floor(Math.random()*roadTiles.length)];
    if(!excludePos||Math.hypot(t.x-excludePos.x,t.y-excludePos.y)>120) return {x:t.x,y:t.y};
  }
  return roadTiles[0];
}

/* ---- NPC waypoint movement (always on road) ---- */
function makeNPC(speed){
  const t=roadTiles[Math.floor(Math.random()*roadTiles.length)];
  return {x:t.x, y:t.y, angle:0, speed, wx:t.x, wy:t.y, rx:t.rx, ry:t.ry};
}

function nextWaypoint(npc){
  const dirs=[{dr:0,dc:1},{dr:0,dc:-1},{dr:1,dc:0},{dr:-1,dc:0}];
  const valid=dirs.filter(d=>isRoad(npc.rx+d.dc,npc.ry+d.dr));
  if(!valid.length) return;
  const d=valid[Math.floor(Math.random()*valid.length)];
  npc.rx+=d.dc; npc.ry+=d.dr;
  npc.wx=npc.rx*T+T/2; npc.wy=npc.ry*T+T/2;
}

function moveNPC(npc){
  const dx=npc.wx-npc.x, dy=npc.wy-npc.y;
  const dist=Math.hypot(dx,dy);
  if(dist<3){ npc.x=npc.wx; npc.y=npc.wy; nextWaypoint(npc); return; }
  npc.angle=Math.atan2(dx,dy); // angle faces movement direction (sin/cos driving)
  npc.x+=dx/dist*npc.speed;
  npc.y+=dy/dist*npc.speed;
}

/* ---- Pre-render static map to offscreen canvas ---- */
const mapCanvas=document.createElement('canvas');
mapCanvas.width=W; mapCanvas.height=H;
const mctx=mapCanvas.getContext('2d');
MAP.forEach((row,ry)=>row.forEach((cell,rx)=>{
  const x=rx*T, y=ry*T;
  if(cell===0){
    mctx.fillStyle='#2d2d2d'; mctx.fillRect(x,y,T,T);
    mctx.strokeStyle='rgba(255,255,100,0.12)'; mctx.lineWidth=2; mctx.setLineDash([10,10]);
    if(isRoad(rx,ry-1)||isRoad(rx,ry+1)){ mctx.beginPath(); mctx.moveTo(x+T/2,y); mctx.lineTo(x+T/2,y+T); mctx.stroke(); }
    if(isRoad(rx-1,ry)||isRoad(rx+1,ry)){ mctx.beginPath(); mctx.moveTo(x,y+T/2); mctx.lineTo(x+T,y+T/2); mctx.stroke(); }
    mctx.setLineDash([]);
    mctx.strokeStyle='rgba(255,255,255,0.04)'; mctx.lineWidth=1; mctx.strokeRect(x,y,T,T);
  } else if(cell===2){
    mctx.fillStyle='#1a3a0a'; mctx.fillRect(x,y,T,T);
    mctx.fillStyle='rgba(50,100,20,0.6)';
    for(let i=0;i<3;i++){ mctx.beginPath(); mctx.arc(x+14+i*18,y+T/2,9,0,Math.PI*2); mctx.fill(); }
  } else {
    mctx.fillStyle=BLDG[(rx+ry)%3]; mctx.fillRect(x,y,T,T);
    // windows (static, no random flicker)
    mctx.fillStyle='rgba(255,255,180,0.12)';
    for(let r=0;r<3;r++) for(let c=0;c<3;c++) mctx.fillRect(x+7+c*17,y+7+r*17,11,11);
    mctx.strokeStyle='rgba(74,124,53,0.15)'; mctx.lineWidth=1; mctx.strokeRect(x,y,T,T);
  }
}));

/* ---- Game state ---- */
const startTile=roadTiles[0];
const P={x:startTile.x, y:startTile.y, angle:0, speed:0, hasPax:false};
const npcs=[makeNPC(1.6), makeNPC(1.3), makeNPC(2.0), makeNPC(1.1)];
let passenger=randRoadPos(P), destination=null;
let fare=0, totalScore=0, paxCount=0;
const msg=document.getElementById('msg');

const keys={};
document.addEventListener('keydown',e=>{ keys[e.key]=true; e.preventDefault(); });
document.addEventListener('keyup',e=>{ keys[e.key]=false; });

/* ---- Draw helpers ---- */
function drawCar(x,y,angle,col,isPlayer){
  ctx.save(); ctx.translate(x,y); ctx.rotate(angle);
  ctx.fillStyle='rgba(0,0,0,0.35)'; ctx.fillRect(-9,  -15+2, 18, 30);
  ctx.fillStyle=col; ctx.fillRect(-9,-15,18,30);
  ctx.fillStyle='#7ab9e8'; ctx.fillRect(-7,-11,14,12);
  ctx.fillStyle='#111';
  [[-12,-10],[ 9,-10],[-12,8],[9,8]].forEach(([wx,wy])=>ctx.fillRect(wx,wy,5,8));
  if(isPlayer){
    ctx.fillStyle='#000'; ctx.font='bold 6px monospace'; ctx.textAlign='center';
    ctx.fillText('TAXI',0,0);
    ctx.fillStyle='rgba(255,255,180,0.9)';
    ctx.beginPath(); ctx.arc(-6,-16,4,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(6,-16,4,0,Math.PI*2); ctx.fill();
  }
  ctx.restore();
}

function drawBlip(pos, isTarget){
  ctx.save(); ctx.translate(pos.x, pos.y);
  const p=0.8+0.2*Math.sin(Date.now()*0.006);
  ctx.scale(p,p);
  ctx.font='22px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.shadowBlur=14;
  if(isTarget){ ctx.shadowColor='#ff4444'; ctx.fillText('📍',0,0); }
  else         { ctx.shadowColor='#f5c518'; ctx.fillText('🙋',0,0); }
  ctx.shadowBlur=0;
  ctx.restore();
}

/* ---- Main loop ---- */
function update(){
  const maxSpd=6, acc=0.25, fric=0.88;
  if(keys['ArrowLeft']||keys['a']||keys['A']) P.angle-=0.065;
  if(keys['ArrowRight']||keys['d']||keys['D']) P.angle+=0.065;
  if(keys['ArrowUp']||keys['w']||keys['W'])    P.speed=Math.min(P.speed+acc, maxSpd);
  if(keys['ArrowDown']||keys['s']||keys['S'])  P.speed=Math.max(P.speed-acc,-maxSpd*0.4);
  P.speed*=fric;

  const nx=P.x+Math.sin(P.angle)*P.speed;
  const ny=P.y-Math.cos(P.angle)*P.speed;
  if(tileAt(nx,ny)===0){ P.x=nx; P.y=ny; }
  else { P.speed*=-0.25; }
  P.x=Math.max(5,Math.min(W-5,P.x)); P.y=Math.max(5,Math.min(H-5,P.y));

  npcs.forEach(moveNPC);

  // Pickup
  if(!P.hasPax && Math.hypot(P.x-passenger.x, P.y-passenger.y)<28){
    P.hasPax=true; fare=0;
    destination=randRoadPos(passenger);
    msg.textContent='🔴 DELIVER TO THE RED MARKER! HURRY!';
  }
  // Dropoff
  if(P.hasPax && destination && Math.hypot(P.x-destination.x, P.y-destination.y)<30){
    P.hasPax=false;
    const earned=(fare+5).toFixed(2);
    totalScore+=parseFloat(earned); paxCount++;
    passenger=randRoadPos(null); destination=null; fare=0;
    msg.textContent='✓ FARE COMPLETE! +$'+earned+' — FIND NEXT PASSENGER!';
    document.getElementById('fare').textContent='0.00';
  }
  if(P.hasPax) fare+=Math.abs(P.speed)*0.018;

  document.getElementById('spd').textContent=Math.abs(Math.round(P.speed*15));
  document.getElementById('fare').textContent=fare.toFixed(2);
  document.getElementById('pax').textContent=paxCount;
  document.getElementById('score').textContent=totalScore.toFixed(2);
}

function draw(){
  ctx.drawImage(mapCanvas,0,0);
  if(!P.hasPax) drawBlip(passenger,false);
  if(P.hasPax&&destination) drawBlip(destination,true);
  npcs.forEach(n=>drawCar(n.x,n.y,n.angle,'#cc2222',false));
  drawCar(P.x,P.y,P.angle,'#FFD700',true);
  // Speed blur
  if(Math.abs(P.speed)>4.5){
    ctx.strokeStyle='rgba(255,255,255,0.07)'; ctx.lineWidth=1;
    for(let i=0;i<6;i++){
      const rx=Math.random()*W, ry=Math.random()*H;
      ctx.beginPath(); ctx.moveTo(rx,ry);
      ctx.lineTo(rx-Math.sin(P.angle)*18,ry+Math.cos(P.angle)*18); ctx.stroke();
    }
  }
}

function loop(){ update(); draw(); requestAnimationFrame(loop); }
loop();
</script>
</body>
</html>
""", height=540)

# ════════════════════════════════════════════════════════════════════
#  CHEAT CODES
# ════════════════════════════════════════════════════════════════════
st.markdown("<hr style='border:1px solid #4a7c35; margin:16px 0;'>", unsafe_allow_html=True)
with st.expander("💀 CHEAT CODES [CLASSIFIED]"):
    st.markdown("""
    <div style="color:#4a7c35; font-family:'Share Tech Mono',monospace;
                font-size:0.75rem; letter-spacing:2px; margin-bottom:8px;">
        ENTER CHEAT CODE — CONTROLLER: ↑↓←→ABXY
    </div>
    """, unsafe_allow_html=True)
    cheat = st.text_input("", placeholder="ENTER CHEAT CODE...", key="cheat_input",
                          label_visibility="collapsed").upper().strip()
    cheat_effects = {
        "HESOYAM":   ("💰 $250,000 ADDED — HEALTH RESTORED", 250000),
        "BXOYWYS":   ("🚗 SPAWN TAXI — MISSION READY", 0),
        "WANRLTW":   ("⭐ WANTED LEVEL CLEARED", -1),
        "ROCKETMAN": ("🚀 JETPACK ACTIVATED — FLY OVER TRAFFIC", 0),
        "CJPHONEHOME": ("🌙 MOON GRAVITY ENABLED", 0),
        "KANGAROO":  ("🦘 MEGA JUMP — AVOID THE BALLAS", 0),
        "SPEEDFREAK": ("🏎️ ALL TAXIS NOW GO 200 MPH", 0),
        "AIWPRTON":  ("🚁 SPAWN HUNTER HELICOPTER", 0),
        "FULLCLIP":  ("🔫 INFINITE AMMO — JUST IN CASE", 0),
    }
    if cheat:
        if cheat in cheat_effects:
            msg, bonus = cheat_effects[cheat]
            if bonus > 0:
                st.session_state['total_earned'] += bonus
            elif bonus == -1:
                st.session_state['wanted'] = 0
            st.success(f"✓ CHEAT ACTIVATED: {msg}")
        else:
            st.error("✗ INVALID CHEAT CODE — TRY AGAIN, FOOL")

# ════════════════════════════════════════════════════════════════════
#  CJ STATS PANEL
# ════════════════════════════════════════════════════════════════════
st.markdown("<hr style='border:1px solid #4a7c35; margin:8px 0;'>", unsafe_allow_html=True)
respect = st.session_state['respect']
components.html(f"""
<html><body style="margin:0;padding:0;background:transparent;">
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Russo+One&display=swap');
.stats {{ background:rgba(0,0,0,0.7); border:1px solid #4a7c35; padding:14px 20px;
         font-family:'Share Tech Mono',monospace; }}
.stats-title {{ color:#f5c518; font-family:'Russo One',sans-serif; font-size:1rem;
               letter-spacing:5px; margin-bottom:12px; }}
.row {{ display:flex; align-items:center; gap:12px; margin:5px 0; }}
.lbl {{ color:#7ab648; font-size:0.75rem; width:120px; letter-spacing:2px; text-transform:uppercase; }}
.bar {{ flex:1; height:10px; background:#1a1a1a; border:1px solid #333; border-radius:1px; }}
.fill {{ height:100%; border-radius:1px; }}
.val {{ color:#b8e0a0; font-size:0.75rem; width:40px; text-align:right; }}
</style>
<div class="stats">
    <div class="stats-title">📊 CJ STATS</div>
    <div class="row">
        <div class="lbl">RESPECT</div>
        <div class="bar"><div class="fill" style="width:{respect}%;background:linear-gradient(to right,#0055ff,#00aaff);"></div></div>
        <div class="val">{respect}%</div>
    </div>
    <div class="row">
        <div class="lbl">STAMINA</div>
        <div class="bar"><div class="fill" style="width:{min(100,st.session_state['fare_count']*20)}%;background:linear-gradient(to right,#ff8c00,#ffcc00);"></div></div>
        <div class="val">{min(100,st.session_state['fare_count']*20)}%</div>
    </div>
    <div class="row">
        <div class="lbl">DRIVING</div>
        <div class="bar"><div class="fill" style="width:{min(100,st.session_state['fare_count']*15)}%;background:linear-gradient(to right,#aa00aa,#ff00ff);"></div></div>
        <div class="val">{min(100,st.session_state['fare_count']*15)}%</div>
    </div>
    <div class="row">
        <div class="lbl">PROGRESS</div>
        <div class="bar"><div class="fill" style="width:{min(100,st.session_state['fare_count']*10)}%;background:linear-gradient(to right,#7ab648,#b8e040);"></div></div>
        <div class="val">{min(100,st.session_state['fare_count']*10)}%</div>
    </div>
</div>
</body></html>
""", height=130)

# ════════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding:20px 0 10px; margin-top:10px;
            border-top:2px solid #4a7c35; font-family:'Share Tech Mono',monospace;">
    <div style="color:#f5c518; font-family:'Russo One',sans-serif;
                font-size:1.1rem; letter-spacing:5px;">
        ROCKSTAR GAMES
    </div>
    <div style="color:#4a7c35; font-size:0.7rem; letter-spacing:3px; margin:4px 0;">
        GRAND THEFT TAXI: SAN FIERRO &nbsp;|&nbsp; A LE WAGON PRODUCTION
    </div>
    <div style="color:#7ab648; font-size:0.7rem; letter-spacing:2px; margin:4px 0;">
        © 2024 TAXI DRIVER ENTERPRISES INC. &nbsp;|&nbsp; ALL MISSIONS RESERVED
    </div>
    <div style="font-size:1.5rem; margin-top:8px;">🚕 🔫 🌴 🚁 ⭐ 🌴 🔫 🚕</div>
    <div style="color:#2a4a1a; font-size:0.65rem; letter-spacing:1px; margin-top:6px;">
        "YOU PICKED THE WRONG HOUSE, FOOL!" — CJ, 1992
    </div>
</div>
""", unsafe_allow_html=True)
