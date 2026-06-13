import streamlit as st
import streamlit.components.v1 as components
import os
import time

# Core Modules
from core.ai_agent import ai_rapor_yaz
from core.finance_engine import finans_motoru

# UI Modules
from ui.components import apply_custom_css, initialize_session_state, senaryo_tetikle, SZLK_HTML, TEAM_HTML
from ui.charts import (
    create_cf_line_chart, create_sensitivity_tornado, create_radar_chart,
    create_opex_pie_chart, create_vc_score_gauge, create_risk_pie_chart,
    create_monte_carlo_histogram
)

@st.cache_data(ttl=600)
def get_ticker_data():
    try:
        import yfinance as yf
        symbols = ["XU100.IS", "USDTRY=X", "EURTRY=X", "GC=F", "BTC-USD"]
        names = ["BIST 100", "Dolar/TL", "Euro/TL", "Ons Altın", "Bitcoin"]
        
        data = yf.download(symbols, period="5d", progress=False)
        results = []
        for sym, name in zip(symbols, names):
            try:
                closes = data['Close'][sym].dropna()
                if len(closes) >= 2:
                    prev = float(closes.iloc[-2])
                    curr = float(closes.iloc[-1])
                    pct = ((curr - prev) / prev) * 100
                    results.append((name, curr, pct))
                elif len(closes) == 1:
                    results.append((name, float(closes.iloc[-1]), 0.0))
                else:
                    results.append((name, 0.0, 0.0))
            except Exception:
                results.append((name, 0.0, 0.0))
        return results
    except Exception:
        return []

def render_ticker():
    tickers = get_ticker_data()
    if not tickers:
        return
    
    html_content = """
    <style>
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: #020617; 
        padding: 12px 0;
        border-bottom: 1px solid rgba(0, 229, 255, 0.3);
        border-radius: 8px;
        margin-top: -15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.1);
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        animation: ticker-anim 25s linear infinite;
    }
    .ticker:hover {
        animation-play-state: paused;
    }
    @keyframes ticker-anim {
        0% { transform: translateX(100vw); }
        100% { transform: translateX(-100%); }
    }
    .ticker-item {
        display: inline-block;
        padding: 0 35px;
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .t-name { color: #00E5FF; margin-right: 8px; text-shadow: 0 0 5px rgba(0,229,255,0.4); }
    .t-val { margin-right: 8px; }
    .t-pos { color: #00E676; text-shadow: 0 0 5px rgba(0,230,118,0.4); }
    .t-neg { color: #ff3366; text-shadow: 0 0 5px rgba(255,51,102,0.4); }
    </style>
    <div class="ticker-wrap">
        <div class="ticker">
    """
    
    for name, val, pct in tickers:
        color_class = "t-pos" if pct >= 0 else "t-neg"
        sign = "+" if pct >= 0 else ""
        formatted_val = f"{val:,.2f}" if val > 100 else f"{val:.4f}"
        html_content += f'<div class="ticker-item"><span class="t-name">{name}</span><span class="t-val">{formatted_val}</span><span class="{color_class}">({sign}{pct:.2f}%)</span></div>'
        
    html_content += """
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

# 1. INIT
st.set_page_config(page_title="QUANTUM AI | Decision Intelligence", layout="wide", initial_sidebar_state="expanded") 
render_ticker()
apply_custom_css()
initialize_session_state()

# 2. SIDEBAR
with st.sidebar:
    if os.path.exists("quantum_logo.png"): st.image("quantum_logo.png", use_container_width=True)
    elif os.path.exists("quantum logo.jpg"): st.image("quantum logo.jpg", use_container_width=True)
    
    st.markdown("---")
    st.header("📚 Örnek Senaryolar")
    st.selectbox("Senaryo Yükle:", ["Seçiniz...", "☕ IoT Termos (Donanım)", "🤖 QuantumAI SaaS (Yazılım)", "🚁 AgriFly Drone (AgriTech)"], key="sen_sec_box", label_visibility="collapsed")
    st.button("📥 Senaryoyu Yükle", on_click=senaryo_tetikle, use_container_width=True)
    
    st.markdown("---")
    st.header("🧠 Kurucu Agent (Behavioral)")
    st.selectbox("Stokastik Kurucu Profili", ["Tier-1 (Kriz Yöneticisi)", "Standart Kurucu", "Çaylak (Yüksek Varyans)"], key="kurucu_profili")

    st.markdown("---")
    st.header("⚙️ Temel Parametreler")
    st.text_input("Girişim Adı", key="g_adi")
    st.selectbox("Sektör (Benchmark için kritik)", ["B2B Finansal Teknoloji", "IoT Donanım", "AgriTech / Drone", "Diğer"], key="sek")
    st.number_input("TAM (Pazar Hacmi - Milyar $)", key="pazar_hacmi", step=0.1)
    st.number_input("CAPEX (Sermaye) ₺", key="cap")
    st.number_input("Birim Maliyet ₺", key="maliyet")
    st.number_input("Satış Fiyatı ₺", key="satis")
    st.number_input("Hedeflenen Satış Adedi", key="adet")
    st.number_input("Risk / İskonto Oranı (%)", key="faiz")

    st.markdown("---")
    st.header("⚖️ Makroekonomi & Vergi")
    st.slider("Kurumlar Vergisi Oranı (%)", 0, 40, key="vergi")
    st.slider("Yıllık Enflasyon Beklentisi (%)", 0, 100, key="enflasyon")

    st.markdown("---")
    st.header("📈 Gider & Abonelik Oranları")
    st.slider("Pazarlama Bütçesi (% Ciro)", 5, 50, key="paz_orani")
    st.slider("Operasyon Gideri (% CAPEX)", 5, 50, key="op_orani")
    st.number_input("Aylık Abonelik Ücreti ₺", key="sub_price")
    st.slider("Aboneliğe Dönüşüm Oranı (%)", 0, 100, key="sub_rate")
    st.slider("Aylık Churn (Kayıp) Oranı (%)", 0.0, 20.0, key="churn", step=0.1)

    st.markdown("---")
    st.markdown(TEAM_HTML, unsafe_allow_html=True)

# 3. MAIN UI
col_title, col_btn = st.columns([4, 1])
with col_title:
    st.markdown('<div class="web-header">QUANTUM AI | DECISION INTELLIGENCE</div>', unsafe_allow_html=True)
with col_btn:
    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    if st.button("🖨️ Raporu PDF Kaydet", use_container_width=True):
        components.html("<script>window.parent.print();</script>", height=0)

t1, t2 = st.tabs(["🎯 Pazar Problemi", "🛡️ Stratejik Çözüm"])
with t1: st.text_area("Pazar Analizi", key="kutu1", height=250, label_visibility="collapsed")
with t2: st.text_area("Çözüm", key="kutu2", height=250, label_visibility="collapsed")
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 STRATEJİK ANALİZİ BAŞLAT", use_container_width=True):
    if st.session_state.cap <= 0 or (st.session_state.satis <= 0 and st.session_state.sub_price <= 0):
        st.error("⚠️ SİSTEM UYARISI: Lütfen sol menüden 0'dan büyük mantıklı bir CAPEX ve Satış Fiyatı/Abonelik ücreti girin.")
        st.stop()
        
    fin = finans_motoru(st.session_state.cap, st.session_state.maliyet, st.session_state.satis, st.session_state.adet, st.session_state.faiz, st.session_state.sub_price, st.session_state.sub_rate, st.session_state.paz_orani, st.session_state.op_orani, st.session_state.churn, st.session_state.vergi, st.session_state.enflasyon, st.session_state.pazar_hacmi, st.session_state.kurucu_profili, st.session_state.sek)
    st.session_state.fin = fin
    st.session_state.run_id = time.time()
    
    with st.status("🧠 Decision Engine Raporları Üretiyor...", expanded=True) as status:
        r_id = st.session_state.run_id
        st.write("⚠️ **COMPOSITE KPI:** Sektörel Benchmarklar ve Risk Parçalama devrede...")
        st.session_state.td_ozet = ai_rapor_yaz("YÖNETİCİ ÖZETİ (AI KARAR MOTORU)", "Kompozit Skora göre aksiyon öner.", st.session_state.g_adi, st.session_state.sek, fin, r_id)
        st.session_state.td_finans = ai_rapor_yaz("FİNANSAL STRES ANALİZİ", "Şirketin nakit dayanıklılığını yorumla.", st.session_state.g_adi, st.session_state.sek, fin, r_id)
        st.session_state.td_porter = ai_rapor_yaz("PORTER 5 FORCES", "Rekabet gücünü analiz et.", st.session_state.g_adi, st.session_state.sek, fin, r_id)
        st.session_state.td_swot = ai_rapor_yaz("SWOT ANALİZİ", f"Güçlü ve Zayıf yönler. Çözüm: {st.session_state.kutu2}", st.session_state.g_adi, st.session_state.sek, fin, r_id)
        st.session_state.td_risk = ai_rapor_yaz("RİSK MATRİSİ", "Operasyonel Riskleri analiz et.", st.session_state.g_adi, st.session_state.sek, fin, r_id)
        st.session_state.td_exit = ai_rapor_yaz("EXIT STRATEJİSİ", "Kim satın alabilir?", st.session_state.g_adi, st.session_state.sek, fin, r_id)
        
        status.update(label="✅ Decision Engine Raporları Tamamlandı!", state="complete")
        st.session_state.analiz_hazir = True

# 4. DASHBOARD RENDER
if st.session_state.analiz_hazir:
    fin = st.session_state.fin
    
    st.markdown(f"""
    <div class="glass-card" style="display: flex; justify-content: space-between; align-items: center; border-left: 4px solid {fin['renk']} !important; padding: 30px !important;">
        <div>
            <h3 style="color: #94a3b8 !important; margin:0; font-size: 1.2rem; text-transform: uppercase; border-bottom: none !important;">KOMPOZİT YATIRIM SKORU</h3>
            <h2 style="color: {fin['renk']} !important; margin-top:5px; font-size: 2rem; border-bottom: none !important;">KARAR: {fin['karar']}</h2>
        </div>
        <div style="font-size: 4rem; font-weight: 900; line-height: 1; margin: 0; color: {fin['renk']};">{fin['score']}<span style="font-size:1.5rem; color:#64748b;">/100</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.markdown(f'<div class="metric-card"><div class="metric-title">NPV</div><div class="metric-value" style="color: #00E676;">{fin["npv"]:,.0f} ₺</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div class="metric-title">MOIC (Girişimci Çarpanı)</div><div class="metric-value" style="color: #00E5FF;">{fin["moic"]:.1f}x</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><div class="metric-title">D-LTV / CAC</div><div class="metric-value" style="color: #00E5FF;">{fin["ltv_cac"]:.1f}x</div></div>', unsafe_allow_html=True)
    
    runway_text = "∞" if fin["runway"] == 999 else f"{fin['runway']} Ay"
    runway_color = "#FFD600" if fin["runway"] != 999 and fin["runway"] <= 12 else "#00E676"
    m4.markdown(f'<div class="metric-card" style="border-left: 2px solid {runway_color};"><div class="metric-title">Runway (Avg Burn)</div><div class="metric-value" style="color: {runway_color};">{runway_text}</div></div>', unsafe_allow_html=True)
    
    m5.markdown(f'<div class="metric-card"><div class="metric-title">Başabaş (ROI)</div><div class="metric-value" style="color: #00E5FF;">{fin["basabas"]} Ay</div></div>', unsafe_allow_html=True)

    t1, t2 = st.tabs(["📊 METRİKLER & GRAFİKLER", "⚔️ AI KARAR RAPORLARI"])
    with t1:
        g1, g2 = st.columns(2)
        g1.plotly_chart(create_cf_line_chart(fin), use_container_width=True)
        g2.plotly_chart(create_sensitivity_tornado(fin), use_container_width=True) 
        
        g3, g4 = st.columns(2)
        g3.plotly_chart(create_radar_chart(fin), use_container_width=True)
        g4.plotly_chart(create_opex_pie_chart(fin), use_container_width=True)
        
        g5, g6 = st.columns(2)
        g5.plotly_chart(create_vc_score_gauge(fin), use_container_width=True)
        g6.plotly_chart(create_risk_pie_chart(fin), use_container_width=True)
        
        st.plotly_chart(create_monte_carlo_histogram(fin), use_container_width=True)
        
    with t2:
        st.markdown(f"""<div class='glass-card'>

### 🧠 AI Yönetici Özeti & Aksiyon Planı

{st.session_state.td_ozet}

</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class='glass-card'>

### 1. FİNANSAL STRES & LİKİDİTE (NWC)

{st.session_state.td_finans}

</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class='glass-card'>

### 2. PORTER 5 FORCES PAZAR HAKİMİYETİ

{st.session_state.td_porter}

</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class='glass-card'>

### 3. SWOT ANALİZİ

{st.session_state.td_swot}

</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class='glass-card'>

### 4. RİSK MATRİSİ

{st.session_state.td_risk}

</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class='glass-card'>

### 5. EXIT STRATEJİSİ VE POTANSİYEL ALICILAR

{st.session_state.td_exit}

</div>""", unsafe_allow_html=True)
        
        st.markdown(SZLK_HTML, unsafe_allow_html=True)

    # 5. GİZLİ YAZDIRMA (PDF) ŞABLONU 
    st.markdown(f"""
    <div class="print-only">
    <hr>
    ## 🧠 YAPAY ZEKA DEĞERLEME RAPORLARI
    ### 1. AI Yönetici Özeti & Aksiyon Planı
    {st.session_state.td_ozet}
    ### 2. Finansal Stres & Likidite (NWC)
    {st.session_state.td_finans}
    ### 3. Porter 5 Forces Pazar Hakimiyeti
    {st.session_state.td_porter}
    ### 4. SWOT Analizi
    {st.session_state.td_swot}
    ### 5. Risk Matrisi
    {st.session_state.td_risk}
    ### 6. Exit Stratejisi ve Potansiyel Alıcılar
    {st.session_state.td_exit}
    </div>
    """, unsafe_allow_html=True)
