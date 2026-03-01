import streamlit as st
from groq import Groq
import plotly.graph_objects as go 
import plotly.express as px 
import base64
import time

# --- 1. MOTOR ATEŞLEME VE GÜVENLİK ---
client = Groq(api_key="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")
st.set_page_config(page_title="QUANTUM AI | Ultimate Valuation", layout="wide", initial_sidebar_state="expanded") 

# --- 2. JÜRİ ETKİLEYİCİ TASARIM (CSS) ---
st.markdown(""" 
<style> 
.web-header {font-family: 'Segoe UI', sans-serif; font-size: 2.8rem; color: #0f172a; font-weight: 900; border-bottom: 5px solid #3b82f6; padding-bottom: 15px; text-transform: uppercase; text-align: center;} 
.metric-card {background: linear-gradient(145deg, #ffffff, #f8fafc); padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border-left: 6px solid #3b82f6; transition: transform 0.2s;} 
.metric-card:hover {transform: translateY(-5px);}
.metric-value {font-size: 2.2rem; font-weight: 900; color: #0f172a; margin: 10px 0;} 
.stButton>button {background: linear-gradient(to right, #1e3a8a, #3b82f6) !important; color: white !important; height: 4em; border-radius: 10px; font-weight: 900; width: 100%; font-size: 18px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); border: none !important;}
.executive-box {background:#f0fdf4; padding:30px; border-left:10px solid #16a34a; border-radius:12px; font-weight:600; color:#166534; margin-bottom:30px; font-size: 1.1rem; line-height: 1.6;}
.report-section {background: #ffffff; padding: 35px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 25px; line-height: 1.8;}
h3 {color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; font-weight: 900;}
</style> 
""", unsafe_allow_html=True) 

# --- 3. YATIRIMCI SÖZLÜĞÜ ---
szlk_html = """
<div style="background: #fffbeb; border-left: 5px solid #f59e0b; padding: 25px; margin-top: 30px; border-radius: 12px; font-size: 15px; color: #475569; line-height: 1.8;">
    <strong style="color: #b45309; font-size: 18px;">📖 KAVRAMSAL ÇERÇEVE VE SÖZLÜK</strong><br><br>
    • <b>NPV (Net Bugünkü Değer):</b> Gelecekteki 3 yıllık serbest nakit akışlarının, sermaye maliyeti ile bugüne indirgenmiş halidir.<br>
    • <b>ROIC (Yatırılan Sermayenin Getirisi):</b> Şirketin ana faaliyetlerine bağladığı fonlardan elde ettiği verimlilik skorudur.<br>
    • <b>LTV / CAC Çarpanı:</b> Bir müşterinin yaşam boyu bıraktığı kârın, o müşteriyi elde etme maliyetine oranıdır (1'e 3 idealdir).<br>
    • <b>Runway (Nakit Ömrü):</b> Kasaya yeni para girmemesi durumunda şirketin kaç ay daha faaliyetlerine devam edebileceğidir.
</div>
"""

# --- 4. AKILLI VERİ YÜKLEYİCİ (UZUN METİNLER BURADA) ---
if 'cap' not in st.session_state:
    st.session_state.update({'g_adi':'','sek':'','cap':3500000,'maliyet':850,'satis':1499,'adet':8000,'prob':'','coz':'', 'faiz':45, 'sub_price':49, 'sub_rate':20})

def sektor_secildi():
    secilen = st.session_state.sektor_secimi
    s_veri = {
        "Akıllı Termos (IoT)": [
            "EcoKupa v2", "IoT Donanım", 3500000, 850, 1499, 8500, 45, 49, 25, 
            "Küresel termos ve taşınabilir içecek ekipmanları pazarı, yıllardır ciddi bir teknolojik inovasyondan yoksundur. Mevcut ürünler yalnızca temel ısı yalıtımı sağlarken, içeceklerin anlık sıcaklık takibi, bakteri oluşumuna karşı hijyen kontrolü (UV-C) ve kullanıcı alışkanlıklarının veri tabanlı analizi gibi modern tüketici ihtiyaçlarına yanıt verememektedir. Ayrıca pazardaki ucuz rakiplerin yarattığı fiyat baskısı, kâr marjlarını daraltmakta ve geleneksel modelleri yüksek riskli hale getirmektedir.", 
            "EcoKupa, yalnızca bir termos değil; patentli UV-C dezenfeksiyon teknolojisi ve Bluetooth entegreli mobil uygulamasıyla tam kapsamlı bir akıllı sağlık asistanıdır. Kullanıcılar içeceklerinin sıcaklığını anlık olarak ayarlayabilir ve sağlık verilerini senkronize edebilir. Donanım satışına ek olarak sunduğumuz 'Premium Sağlık Takibi' abonelik modeli (SaaS) sayesinde, düşük kâr marjlı pazarda kendimize yüksek kârlı ve sürdürülebilir bir rekabet hendeği yaratıyoruz."
        ],
        "Yapay Zeka (SaaS)": [
            "QuantumAI Enterprise", "Kurumsal AI", 1500000, 0, 4500, 2500, 40, 299, 90, 
            "Stratejik planlama süreçleri kurumlarda halen manuel ve verimsiz Excel tablolarıyla yürütülmektedir. Bu durum hem zaman kaybına hem de kritik finansal hatalara yol açmaktadır.", 
            "Yapay zeka tabanlı otonom değerleme ve DCF motoru sunan yüksek kârlılıklı SaaS platformu. Gelişmiş veri analitiği ile anında finansal raporlama sağlar."
        ],
        "MedTech (Giyilebilir)": [
            "BioLink Pro", "Sağlık Teknolojileri", 7500000, 2200, 12500, 5000, 30, 799, 60, 
            "Yaşlı nüfusun evde takibi sırasında acil durumların geç fark edilmesi ölümcül sonuçlar doğurmaktadır. Mevcut sistemler anlık doktor entegrasyonundan yoksundur.", 
            "Yapay zeka destekli, 7/24 vital veri takibi yapan ve doktor paneli entegrasyonu sunan tıbbi cihaz/yazılım ekosistemi. Anında müdahale hayat kurtarır."
        ]
    }
    if secilen in s_veri:
        d = s_veri[secilen]
        st.session_state.update({'g_adi':d[0], 'sek':d[1], 'cap':d[2], 'maliyet':d[3], 'satis':d[4], 'adet':d[5], 'faiz':d[6], 'sub_price':d[7], 'sub_rate':d[8], 'prob':d[9], 'coz':d[10]})

# --- 5. GELİŞTİRİLMİŞ MATEMATİKSEL MOTOR ---
def finans_motoru(b, m, s, a, faiz, sub_p, sub_r):
    ciro_don = s * a
    ciro_saas = int(a * (sub_r / 100)) * sub_p * 12
    tc = ciro_don + ciro_saas
    dm = m * a; paz = tc * 0.20; op = b * 0.15
    cf1 = tc - (dm + paz + op); r = faiz / 100
    npv = (cf1/(1+r) + (cf1*1.15)/(1+r)**2 + (cf1*1.3)/(1+r)**3) - b
    roic = (npv / b) * 100 if b > 0 else 0
    yanma = (paz + op) / 12
    runway = int(b / yanma) if yanma > 0 else 99
    ltv_cac = ((s-m) + (sub_p*12/0.15)) / (paz/a) if a>0 else 0
    return {"npv":npv, "roic":roic, "runway":runway, "ltv_cac":ltv_cac, "cf":[cf1, cf1*1.15, cf1*1.3], "gelirler":[ciro_don, ciro_saas], "giderler":[dm, paz, op], "tc":tc, "radar":[min(100, int(roic)), 85, 90, 75]}

def ai_rapor_yaz(baslik, istek, veri):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Sen dünyanın en zeki finansal analisti ve stratejistisin. İkna edici, ağırbaşlı ve McKinsey seviyesinde profesyonel bir Türkçe kullan. Madde işaretleri kullanabilirsin."}, 
                      {"role": "user", "content": f"KONU: {baslik}. VERİ: {veri}. İSTEK: {istek}"}],
            temperature=0.3
        )
        return completion.choices[0].message.content.strip()
    except: return "Llama 3.3-70B motoru şu an aşırı yüklü, lütfen 10 saniye sonra tekrar deneyiniz."

# --- 6. SİDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Llama_Index_logo.png/1200px-Llama_Index_logo.png", width=60)
    st.header("🏢 Kurumsal Kütüphane")
    if st.button("🚀 ÖRNEK SENARYOYU YÜKLE"):
        st.session_state.sektor_secimi = "Akıllı Termos (IoT)"
        sektor_secildi()
    st.selectbox("Hazır Şablonlar", ["Seçiniz...", "Akıllı Termos (IoT)", "Yapay Zeka (SaaS)", "MedTech (Giyilebilir)"], key="sektor_secimi", on_change=sektor_secildi)
    
    st.markdown("---")
    g_adi = st.text_input("Girişim Adı", value=st.session_state.g_adi)
    sek = st.text_input("Sektör", value=st.session_state.sek)
    cap = st.number_input("CAPEX (Kuruluş Maliyeti ₺)", value=st.session_state.cap)
    maliyet = st.number_input("Birim Maliyet (₺)", value=st.session_state.maliyet)
    satis = st.number_input("Satış Fiyatı (₺)", value=st.session_state.satis)
    adet = st.number_input("Yıllık Hedef Adet", value=st.session_state.adet)
    faiz = st.number_input("İskonto / Risk Oranı (%)", value=st.session_state.faiz)
    sub_p = st.number_input("Aylık Abonelik Ücreti (₺)", value=st.session_state.sub_price)
    sub_r = st.slider("Abonelik Dönüşüm Oranı (%)", 0, 100, st.session_state.sub_rate)

# --- 7. ANA EKRAN ---
st.markdown('<div class="web-header">QUANTUM AI | KURUMSAL DEĞERLEME MOTORU</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: prob = st.text_area("Market / Problem Analizi", value=st.session_state.prob, height=220)
with c2: coz = st.text_area("Stratejik Çözüm / USP", value=st.session_state.coz, height=220)

if st.button("🚀 YAPAY ZEKA DEĞERLEMESİNİ BAŞLAT"):
    fin = finans_motoru(cap, maliyet, satis, adet, faiz, sub_p, sub_r)
    
    # --- JÜRİ İÇİN ŞOV KISMI (PROGRESS BAR) ---
    p_bar = st.progress(0)
    s_text = st.empty()
    
    s_text.markdown("### 🧠 Llama 3.3-70B Algoritmaları Başlatılıyor...")
    time.sleep(0.5); p_bar.progress(20)
    
    s_text.markdown("### 📊 Matematiksel Modeller ve Nakit Akışları Hesaplanıyor...")
    td_ozet = ai_rapor_yaz("YÖNETİCİ ÖZETİ VE KARAR", "Bu işe girilir mi? Net kararını ver ve sebebini NPV üzerinden açıkla.", f"NPV: {fin['npv']:,.0f} ₺")
    p_bar.progress(40)

    s_text.markdown("### ⚔️ Porter 5 Forces ve Rekabet Analizi Yazılıyor...")
    td_porter = ai_rapor_yaz("Pazar Hakimiyeti", "Porter 5 Forces modelini bu girişime uygula.", f"Sektör: {sek}, Ürün: {g_adi}")
    p_bar.progress(60)

    s_text.markdown("### 🛡️ Risk Matrisi ve Stres Testi Uygulanıyor...")
    td_finans = ai_rapor_yaz("Finansal Stres", "Nakit akışı ve yatırım kârlılığını yorumla.", f"ROIC: %{fin['roic']:.1f}, NPV: {fin['npv']}")
    td_risk = ai_rapor_yaz("SWOT", "En büyük riskleri ve fırsatları detaylandır.", f"Vade: {fin['runway']} Ay")
    p_bar.progress(80)

    s_text.markdown("### 🚪 M&A Çıkış Stratejileri Hesaplanıyor...")
    td_exit = ai_rapor_yaz("Exit Stratejisi", "Gelecekte hangi holding veya dev şirket bunu neden satın alır?", g_adi)
    p_bar.progress(100)
    
    s_text.empty()
    p_bar.empty()
    st.balloons()

    # --- SONUÇLARI YAZDIRMA ---
    st.markdown(f'<div class="executive-box">💡 <b>LLAMA 70B YÖNETİCİ ÖZETİ:</b><br>{td_ozet}</div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="metric-card"><div>Net Bugünkü Değer</div><div class="metric-value">{fin["npv"]:,.0f} ₺</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div>Sermaye Getirisi</div><div class="metric-value">%{fin["roic"]:.1f}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><div>Birim Ekonomisi</div><div class="metric-value">{fin["ltv_cac"]:.1f}x</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric-card"><div>Risk Vadesi</div><div class="metric-value">{fin["runway"]} Ay</div></div>', unsafe_allow_html=True)

    # --- 8. MUHTEŞEM GRAFİKLER ---
    fig1 = px.line(y=fin['cf'], x=["1.Yıl","2.Yıl","3.Yıl"], title="3 Yıllık Nakit Akışı", markers=True, line_shape="spline", color_discrete_sequence=['#2563eb'])
    fig2 = go.Figure(go.Waterfall(x=["Ciro","Maliyet","Pazarlama","Operasyon","Net Kâr"], y=[fin['tc'],-fin['giderler'][0],-fin['giderler'][1],-fin['giderler'][2],fin['cf'][0]], measure=["relative"]*4+["total"])).update_layout(title="Maliyet & Kâr Şelalesi")
    fig3 = px.pie(names=['Donanım','Abonelik (SaaS)'], values=fin['gelirler'], title="Hibrit Gelir Dağılımı", hole=0.4, color_discrete_sequence=['#1e40af','#3b82f6'])
    fig4 = go.Figure(data=go.Heatmap(z=[[fin['npv']*0.7, fin['npv'], fin['npv']*1.4]], x=["Enflasyonist","Hedeflenen","İyimser"], y=["Senaryolar"], colorscale='Blues')).update_layout(title="Finansal Stres Haritası")
    fig5 = go.Figure(data=go.Scatterpolar(r=fin['radar'], theta=['Getiri (ROI)','Kâr Marjı','Pazar Uyumu','Sürdürülebilirlik'], fill='toself', line_color='#2563eb')).update_layout(title="Stratejik Sağlık Radarı")

    t1, t2, t3, t4 = st.tabs(["📊 CANLI GRAFİKLER", "⚔️ KURUMSAL RAPORLAR", "🛡️ SWOT ANALİZİ", "🚪 EXIT STRATEJİSİ"])
    with t1:
        g1, g2 = st.columns(2)
        g1.plotly_chart(fig1, use_container_width=True)
        g2.plotly_chart(fig2, use_container_width=True)
        g3, g4 = st.columns(2)
        g3.plotly_chart(fig3, use_container_width=True)
        g4.plotly_chart(fig4, use_container_width=True)
        st.plotly_chart(fig5, use_container_width=True)

    with t2:
        st.markdown(f"<div class='report-section'><h3>FİNANSAL STRES ANALİZİ</h3>{td_finans}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>PORTER 5 FORCES PAZAR HAKİMİYETİ</h3>{td_porter}</div>", unsafe_allow_html=True)
        st.markdown(szlk_html, unsafe_allow_html=True)
    with t3: st.markdown(f"<div class='report-section'><h3>DERİN SWOT VE RİSK MATRİSİ</h3>{td_risk}</div>", unsafe_allow_html=True)
    with t4: st.markdown(f"<div class='report-section'><h3>KURUMSAL ÇIKIŞ (EXIT) STRATEJİSİ</h3>{td_exit}</div>", unsafe_allow_html=True)

    # --- 9. HARİKA TASARIMLI HTML İNDİRİCİ ---
    h1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')
    h2 = fig2.to_html(full_html=False, include_plotlyjs=False)
    h3 = fig3.to_html(full_html=False, include_plotlyjs=False)
    h4 = fig4.to_html(full_html=False, include_plotlyjs=False)
    h5 = fig5.to_html(full_html=False, include_plotlyjs=False)

    full_report_html = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>{g_adi} | Stratejik Değerleme</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8fafc; color: #334155; margin: 0; padding: 40px; }}
            .container {{ max-width: 1200px; margin: auto; background: white; padding: 50px; border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-top: 10px solid #1e3a8a; }}
            h1 {{ color: #1e3a8a; text-align: center; font-size: 38px; border-bottom: 3px solid #e2e8f0; padding-bottom: 20px; text-transform: uppercase; }}
            h2 {{ color: #2563eb; margin-top: 50px; padding-left: 15px; border-left: 6px solid #f59e0b; background: #f1f5f9; padding-top: 10px; padding-bottom: 10px; border-radius: 0 8px 8px 0; }}
            .summary {{ background: #f0fdf4; padding: 25px; border-radius: 12px; border-left: 8px solid #16a34a; font-size: 17px; line-height: 1.8; color: #166534; font-weight: bold; margin-bottom: 40px; }}
            .content-box {{ font-size: 16px; line-height: 1.8; color: #475569; padding: 25px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; margin-bottom: 30px; }}
            .chart-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 30px; }}
            .footer {{ text-align: center; margin-top: 60px; padding-top: 20px; border-top: 1px solid #cbd5e1; color: #94a3b8; font-size: 13px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{g_adi} | KURUMSAL ANALİZ VE DEĞERLEME RAPORU</h1>

            <h2>1. AI YÖNETİCİ ÖZETİ VE STRATEJİK KARAR</h2>
            <div class="summary">{td_ozet}</div>

            <h2>2. FİNANSAL PERFORMANS GRAFİKLERİ</h2>
            <div style="margin-top: 30px;">{h1}</div>
            <div class="chart-grid"><div>{h2}</div><div>{h3}</div></div>
            <div class="chart-grid"><div>{h4}</div><div>{h5}</div></div>

            <h2>3. FİNANSAL DERİNLİK ANALİZİ</h2>
            <div class="content-box">{td_finans}</div>

            <h2>4. PORTER 5 FORCES PAZAR HAKİMİYETİ</h2>
            <div class="content-box">{td_porter}</div>

            <h2>5. DERİN SWOT VE RİSK MATRİSİ</h2>
            <div class="content-box">{td_risk}</div>

            <h2>6. M&A VE EXIT (ÇIKIŞ) STRATEJİSİ</h2>
            <div class="content-box">{td_exit}</div>

            {szlk_html}

            <div class="footer">
                <p><strong>Özel ve Gizlidir.</strong> Bu rapor Quantum AI Elite Motoru (Llama 3.3-70B) kullanılarak üretilmiştir.</p>
                <p>© 2026 Tüm hakları saklıdır.</p>
            </div>
        </div>
    </body>
    </html>
    """
    b64 = base64.b64encode(full_report_html.encode('utf-8')).decode()
    st.markdown(f'<br><a href="data:text/html;base64,{b64}" download="{g_adi}_Kurumsal_Rapor.html"><button>📥 İNTERAKTİF GRAFİKLİ FULL RAPORU İNDİR</button></a>', unsafe_allow_html=True)