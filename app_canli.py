import streamlit as st
from groq import Groq
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os
import html
import time
from scipy.stats import skewnorm, t

# ==========================================
# 1. MOTOR ATEŞLEME VE GÜVENLİ API BAĞLANTISI
# ==========================================
np.random.seed(2026)
st.set_page_config(page_title="QUANTUM AI | Kurumsal Değerleme", layout="wide", initial_sidebar_state="expanded")

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("⚠️ SİSTEM UYARISI: Groq API Anahtarı bulunamadı! Lütfen Streamlit Cloud üzerinden 'Settings -> Secrets' kısmına anahtarınızı ekleyin.")
    st.stop()

# ==========================================
# 2. 2026 MODERN TASARIM (BEYAZ MENÜ KESİN ÇÖZÜM)
# ==========================================
st.markdown("""
<style>
.stApp {background-color: #030712; color: #f8fafc; font-family: 'Inter', sans-serif;}
/* SİDEBAR TASARIMI */
[data-testid="stSidebar"] { background-color: #050b14 !important; border-right: 1px solid rgba(56, 189, 248, 0.1); }
[data-testid="stSidebar"] img { margin-bottom: 30px !important; }
/* YAZI VE BAŞLIKLAR */
p, li, div[data-testid="stMarkdownContainer"] > p { font-size: 1.08rem !important; line-height: 1.8 !important; color: #e2e8f0 !important; }
h1, h2, h3, h4 { margin-top: 1rem; margin-bottom: 0.8rem; font-weight: 800 !important; color: #f8fafc !important;}
h2 { font-size: 1.8rem !important; color: #38bdf8 !important; text-shadow: 0px 2px 15px rgba(56, 189, 248, 0.2); border-bottom: none !important;}
h3 { font-size: 1.4rem !important; color: #7dd3fc !important; }
/* BEYAZ MENÜ SORUNUNU KÖKÜNDEN ÇÖZEN NÜKLEER CSS */
div[data-baseweb="select"] > div, div[data-baseweb="popover"] > div { background-color: #0f172a !important; color: #f8fafc !important; border: 1px solid #38bdf8 !important; }
span[data-baseweb="select"] { color: #f8fafc !important; }
ul[role="listbox"] { background-color: #0f172a !important; }
li[role="option"] { color: #f8fafc !important; background-color: #0f172a !important; font-weight: 600 !important; font-size: 1.1rem !important;}
li[role="option"]:hover, li[role="option"][aria-selected="true"] { background-color: #38bdf8 !important; color: #030712 !important; }
/* INPUT KUTULARI (GLOW EFEKTİ) */
.stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: rgba(15, 23, 42, 0.8) !important; color: #38bdf8 !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; border-radius: 10px !important; font-weight: 700 !important; }
.stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus { border: 1px solid #38bdf8 !important; box-shadow: 0 0 10px rgba(56, 189, 248, 0.5) !important; }
[data-testid="stSidebar"] label p { font-size: 1.05rem !important; font-weight: 700 !important; color: #cbd5e1 !important; }
/* ANA BAŞLIK VE METRİK KARTLARI */
.web-header { font-size: 3.2rem; font-weight: 900; text-align: center; letter-spacing: -1px; margin-bottom: 40px; background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0px 10px 30px rgba(79, 172, 254, 0.15); }
.metric-card { background: rgba(15, 23, 42, 0.6); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px; backdrop-filter: blur(12px); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); }
.metric-value {font-size: 2.6rem; font-weight: 900; color: #ffffff; margin-top: 10px;}
.metric-title {font-size: 1rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;}
/* YENİ NESİL BUTON */
.stButton>button { background: linear-gradient(135deg, #2563eb, #3b82f6) !important; color: white !important; font-weight: 900; border-radius: 14px; height: 3.8em; font-size: 20px; width: 100%; border: none !important; box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3); transition: all 0.3s ease; }
.stButton>button:hover { box-shadow: 0 15px 35px rgba(59, 130, 246, 0.5); transform: scale(1.02); }
/* RAPOR KUTULARI VE SEKMELER */
.report-section { background: rgba(15, 23, 42, 0.4); padding: 40px; border-radius: 20px; border: 1px solid rgba(59, 130, 246, 0.1); margin-bottom: 30px; }
.stTabs [data-baseweb="tab-list"] { background-color: rgba(15, 23, 42, 0.6); border-radius: 12px; padding: 5px; gap: 10px; }
.stTabs [data-baseweb="tab"] { color: #94a3b8; font-weight: 700; border-radius: 8px; padding: 10px 20px; }
.stTabs [aria-selected="true"] { background-color: rgba(56, 189, 248, 0.1) !important; color: #38bdf8 !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; }
</style>
""", unsafe_allow_html=True)

szlk_html = """
<div style="background: rgba(30, 41, 59, 0.5); border-left: 4px solid #f59e0b; padding: 30px; margin-top: 40px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
    <h3 style="color: #fbbf24; margin-top:0;">📖 YATIRIMCI SÖZLÜĞÜ VE KAVRAMLAR</h3>
    <p>• <b style="color:#ffffff;">NPV:</b> Gelecekteki nakit akışlarının risk ve faiz düşülerek hesaplanmış bugünkü net değeridir.<br>
    • <b style="color:#ffffff;">MOIC (Mutiple on Invested Capital):</b> Yatırılan sermayenin kaç katı geri dönüş sağlandığını gösterir (Gerçek VC Standardı).<br>
    • <b style="color:#ffffff;">Discounted LTV / CAC:</b> Bir müşterinin bıraktığı ömür boyu kârın, WACC ve Churn'e indirgenmiş, onu elde etme maliyetine oranıdır.<br>
    • <b style="color:#ffffff;">Başabaş (Break-Even):</b> Yatırımcının koyduğu paranın tamamen geri dönüp şirketin net kâra geçtiği aydır.</p>
</div>
"""

def html_temizle(metin): 
    return metin.replace('**', '<b>').replace('###', '<h2>').replace('\n', '<br>')

# ==========================================
# 3. KUSURSUZ HAFIZA VE SENARYOLAR
# ==========================================
if 'g_adi' not in st.session_state:
    st.session_state.update({
        'g_adi': '', 'sek': '', 'cap': 0, 'maliyet': 0, 'satis': 0, 'adet': 0, 'faiz': 0,
        'sub_price': 0, 'sub_rate': 0, 'paz_orani': 5, 'op_orani': 5, 'pazar_hacmi': 0.0, 'churn': 0.0,
        'vergi': 25, 'enflasyon': 30, 'kurucu_profili': 'Standart Kurucu',
        'kutu1': '', 'kutu2': '', 'analiz_hazir': False, 'op': 0,
        'fin': {'radar': [0,0,0,0], 'dm': 0, 'paz': 0, 'op': 0, 'vergi': 0, 'npv': 0, 'basabas': 0, 'runway': 0, 'ltv_cac': 0, 'cf': [0,0,0], 'ciro': 0, 'moic': 0, 'karar': '', 'renk': '', 'prob_fail': 0, 'mc_npv': [], 'sens_data': {}},
        'sen_sec_box': 'Seçiniz...'
    })

def yukle_termos():
    st.session_state.update({'g_adi': 'EcoKupa v2', 'sek': 'IoT Donanım', 'cap': 3500000, 'maliyet': 850, 'satis': 1499, 'adet': 8500, 'faiz': 45, 'sub_price': 49, 'sub_rate': 15, 'paz_orani': 20, 'op_orani': 15, 'pazar_hacmi': 2.5, 'churn': 5.0, 'vergi': 25, 'enflasyon': 35, 'kurucu_profili': 'Standart Kurucu', 'kutu1': 'Global termos pazarı inovasyondan uzaklaşmış durumdadır.', 'kutu2': 'EcoKupa v2, otonom takip eden yıkıcı bir IoT ekosistemidir.', 'analiz_hazir': False})

def yukle_saas():
    st.session_state.update({'g_adi': 'QuantumAI Enterprise', 'sek': 'B2B Finansal Teknoloji', 'cap': 4500000, 'maliyet': 0, 'satis': 4500, 'adet': 2500, 'faiz': 40, 'sub_price': 299, 'sub_rate': 35, 'paz_orani': 30, 'op_orani': 25, 'pazar_hacmi': 14.8, 'churn': 4.5, 'vergi': 25, 'enflasyon': 40, 'kurucu_profili': 'Tier-1 (Kriz Yöneticisi)', 'kutu1': 'Girişimcilik ekosisteminin en acımasız gerçeği, kurulan her on yeni girişimin dokuzunun "Ölüm Vadisi" krizleri yüzünden batmasıdır.', 'kutu2': 'Quantum AI, Python mimarisi üzerine inşa edilmiş otonom bir "Finansal Zeka ve İş Modeli" motorudur.', 'analiz_hazir': False})

def yukle_drone():
    st.session_state.update({'g_adi': 'AgriFly - Otonom Tarım', 'sek': 'AgriTech / Drone', 'cap': 2800000, 'maliyet': 45000, 'satis': 125000, 'adet': 150, 'faiz': 35, 'sub_price': 1500, 'sub_rate': 65, 'paz_orani': 15, 'op_orani': 20, 'pazar_hacmi': 4.2, 'churn': 3.5, 'vergi': 25, 'enflasyon': 30, 'kurucu_profili': 'Çaylak (Yüksek Varyans)', 'kutu1': 'Geleneksel tarımda çiftçiler tarlanın tamamına manuel olarak kimyasal püskürtmektedir.', 'kutu2': 'AgriFly, hastalıklı bölgeleri tespit eder ve nokta atışı ilaçlama yapar.', 'analiz_hazir': False})

def senaryo_tetikle():
    secim = st.session_state.sen_sec_box
    if secim == "☕ IoT Termos (Donanım)": yukle_termos()
    elif secim == "🤖 QuantumAI SaaS (Yazılım)": yukle_saas()
    elif secim == "🚁 AgriFly Drone (AgriTech)": yukle_drone()

# ==========================================
# 4. FİNANS MATEMATİĞİ (ULTIMATE QUANT-GRADE ENGINE)
# ==========================================
@st.cache_data(show_spinner=False)
def finans_motoru(b, m, s, a, faiz, sub_p, sub_r, paz_o, op_o, churn, vergi_orani, enflasyon_orani, pazar_hacmi, kurucu_profili):
    burn_mult, cac_penalty = (1.0, 1.0) if "Tier-1" in kurucu_profili else ((1.8, 1.5) if "Çaylak" in kurucu_profili else (1.3, 1.2))
    
    def run_cycle(macro_shock=1.0, is_mc=False, v_churn=churn, v_paz=paz_o, v_sub=sub_p):
        # 1. KORELASYON DÜZELTMESİ: Makro şok, hem talebi (satış) hem maliyeti (enflasyon/CAC) birbirine bağlı etkiler
        macro_shock = np.clip(macro_shock, 0.3, 1.4)
        demand_shock = macro_shock
        cost_shock = 1.0 + (1.0 - macro_shock) * 0.5 # Kötü senaryoda maliyet artar
        wacc_m = (max(0.15, (faiz/100) + 0.12 + (enflasyon_orani/100)*0.5)) / 12
        und_cfs, dis_cfs, cohorts, ebitdas, revs = [], [], [], [], []
        tam_tl = pazar_hacmi * 32.5 * 1e9
        max_users = (tam_tl / max(v_sub, 1)) * 0.02
        y1_ciro, y1_dm, y1_paz, y1_op, y1_vergi = 0, 0, 0, 0, 0
        y1_cf, y2_cf, y3_cf = 0, 0, 0
        base_cac = max(v_sub * 4, 150) * cac_penalty
        b2b_sales_friction = 1200
        sales_cycle_delay = 4
        revenue_delay = 1
        pending_users = [0] * 65
        base_churn = max(v_churn/100, 0.005)

        for month in range(1, 61):
            # 4. KUR RİSKİ (FX Risk): Enflasyona dayalı kur şoku (Purchasing Power Parity)
            fx_factor = (1 + (enflasyon_orani * 0.85) / 100 / 12) ** month
            inf_factor = (1 + enflasyon_orani / 100 / 12) ** month
            mkt = (b * v_paz/100) / 12
            
            # 2. RETENTION CURVE: Sabit churn yerine Power-law zamanla yavaşlayan müşteri kaybı
            cur_active_users = 0
            for c in cohorts:
                if month > c[0] + revenue_delay:
                    age = month - c[0] - revenue_delay
                    retention = (1 - base_churn) ** (age ** 0.85)
                    cur_active_users += c[1] * retention
            
            saturation = cur_active_users / max(max_users, 1)
            # CAC enflasyon ve makro maliyet şokundan korele etkilenir
            current_cac = base_cac * (1 + (saturation * 5)) * inf_factor * cost_shock
            raw_new_users = (mkt / current_cac) * (sub_r/100) * demand_shock
            
            if month + sales_cycle_delay < 65:
                pending_users[month + sales_cycle_delay] += raw_new_users
            
            active_new_users = pending_users[month]
            if active_new_users > 0:
                cohorts.append([month, active_new_users])
                
            price_decay = 1 - (saturation * 0.3)
            effective_price = v_sub * max(0.5, price_decay) * (0.8 if demand_shock < 0.9 else 1.0)
            
            # Revenue Recognition with Retention Curve
            m_saas = 0
            for c in cohorts:
                if month > c[0] + revenue_delay:
                    age = month - c[0] - revenue_delay
                    retention = (1 - base_churn) ** (age ** 0.85)
                    m_saas += c[1] * retention * effective_price
                    
            hw_rev = (a/12)*s*demand_shock if month > 6 else 0
            rev = m_saas + hw_rev
            revs.append(rev)
            
            # Giderler: Donanım kur riskine direkt maruz kalır
            hw_cost = ((a/12)*m if month > 4 else (a/12)*m*2) * fx_factor * cost_shock
            base_opex = (b * op_o/100)/12
            
            # 3. STEP-FUNCTION OPEX: Operasyon maliyetleri basamaklı (Step) artar, lineer değil!
            step_opex = np.floor(cur_active_users / 2000) * (b * 0.08) / 12 # Her 2000 kullanıcıda devasa sunucu/ekip maliyeti zıplaması
            scale_opex = (cur_active_users/100) * (effective_price * 0.05) + step_opex
            sales_cost = active_new_users * b2b_sales_friction * inf_factor
            opex = (base_opex + scale_opex + sales_cost) * burn_mult * ((fx_factor + inf_factor)/2)
            
            ebitda = rev - (hw_cost + mkt + opex)
            tax = ebitda * (vergi_orani/100) if ebitda > 0 else 0
            
            if month <= 18 and ebitda < 0:
                ebitda *= 1.4
                
            ebitdas.append(ebitda)
            net_cf = ebitda - tax
            und_cfs.append(net_cf)
            dis_cfs.append(net_cf / (1 + wacc_m)**month)
            
            if month <= 12:
                y1_ciro += rev; y1_dm += hw_cost; y1_paz += mkt; y1_op += opex; y1_vergi += tax; y1_cf += net_cf
            elif month <= 24:
                y2_cf += net_cf
            elif month <= 36:
                y3_cf += net_cf

        # 5. EXIT MULTIPLE FALLBACK (Zarar Eden Growth Start-up Kurtarması)
        exit_multiple = np.random.uniform(2.5, 5.0) if not is_mc else (np.random.uniform(1.0, 3.0) if demand_shock < 0.8 else np.random.uniform(2.0, 4.5))
        last_year_ebitda = np.mean(ebitdas[-12:]) * 12
        last_year_rev = sum(revs[-12:])
        
        if last_year_ebitda > 0:
            exit_val = last_year_ebitda * exit_multiple # Kârdaysa EBITDA çarpanı
        else:
            exit_val = last_year_rev * (exit_multiple * 0.4) # Zarardaysa Büyüme (Ciro) çarpanı
            
        npv = sum(dis_cfs) + (exit_val / (1 + wacc_m)**60) - b
        
        # VC-Grade Discounted LTV (WACC dahil edilmiş)
        avg_prices = [v_sub * max(0.5, (1 - (min(1, (i/60)) * 0.3))) for i in range(1, 61)]
        lifecycle_arpu = np.mean(avg_prices)
        gross_margin = 0.85
        monthly_margin = lifecycle_arpu * gross_margin
        ltv = monthly_margin / (base_churn + wacc_m)
        avg_cac = base_cac * 1.5 + b2b_sales_friction
        ltv_cac = ltv / avg_cac if avg_cac > 0 else 0
        
        cum_cf = -b
        basabas = 999
        for i, cf in enumerate(und_cfs):
            cum_cf += cf
            if cum_cf >= 0 and basabas == 999:
                basabas = i + 1
                
        negative_months = [c for c in und_cfs if c < 0]
        peak_burn = abs(min(negative_months)) if negative_months else 0
        runway = int(b / peak_burn) if peak_burn > 0 else 999
        
        return {
            "npv": npv, "cf1": y1_cf, "cf2": y2_cf, "cf3": y3_cf,
            "ciro": y1_ciro, "dm": y1_dm, "paz": y1_paz, "op": y1_op, "vergi": y1_vergi,
            "ltv_cac": ltv_cac, "runway": runway, "basabas": basabas, "exit_mult": exit_multiple,
            "total_return": sum(und_cfs) + exit_val
        }

    base = run_cycle(1.0, is_mc=False)
    mc_npvs = []
    
    for _ in range(1000):
        # Base shock yaratılır, run_cycle içindeki korelasyon fonksiyonuna yollanır
        base_shock = t.rvs(df=4) * 0.2 + 1.0 if 't' in globals() else np.random.normal(1.0, 0.2)
        if np.random.rand() < 0.03:
            base_shock *= 0.4
        res = run_cycle(base_shock, is_mc=True)
        mc_npvs.append(res['npv'])
        
    prob_fail = (np.sum(np.array(mc_npvs) < 0) / 1000) * 100
    moic = base['total_return'] / b if b > 0 else 0
    
    # TORNADO SENSITIVITY KISMI (Makro Duyarlılık)
    sens_churn = run_cycle(1.0, is_mc=False, v_churn=churn*1.2)['npv']
    sens_paz = run_cycle(1.0, is_mc=False, v_paz=paz_o*0.8)['npv']
    sens_sub = run_cycle(1.0, is_mc=False, v_sub=sub_p*0.8)['npv']
    
    sens_data = {
        "Churn Oranı %20 Artarsa": ((sens_churn - base['npv']) / abs(base['npv'])) * 100 if base['npv']!=0 else 0,
        "Pazarlama Bütçesi %20 Düşerse": ((sens_paz - base['npv']) / abs(base['npv'])) * 100 if base['npv']!=0 else 0,
        "Abonelik Fiyatı %20 Düşerse": ((sens_sub - base['npv']) / abs(base['npv'])) * 100 if base['npv']!=0 else 0
    }
    
    if moic >= 3.0 and base['basabas'] <= 36 and prob_fail < 45 and base['ltv_cac'] > 3.0:
        karar, renk = "✅ GÜÇLÜ YATIRIM (INVEST)", "#10b981"
    elif moic >= 1.5 and prob_fail < 65:
        karar, renk = "⚠️ RİSKLİ BÜYÜME (HOLD / MONITOR)", "#f59e0b"
    else:
        karar, renk = "❌ YATIRIM YAPILAMAZ (REJECT)", "#ef4444"
        
    return {
        "npv": base['npv'], "moic": moic, "runway": base['runway'], "ltv_cac": base['ltv_cac'],
        "basabas": base['basabas'], "cf": [base['cf1'], base['cf2'], base['cf3']],
        "ciro": base['ciro'], "dm": base['dm'], "paz": base['paz'], "op": base['op'], "vergi": base['vergi'],
        "radar": [min(100, max(0, int(moic*20))), min(100, int(base['exit_mult']*20)), 90, max(0, int(100-churn*4))],
        "karar": karar, "renk": renk, "prob_fail": prob_fail, "mc_npv": mc_npvs, "sens_data": sens_data
    }

# ==========================================
# 5. GÜVENLİ YAPAY ZEKA ÇAĞRISI
# ==========================================
def safe_ai_call(messages, retries=3):
    for i in range(retries):
        try:
            completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.55, timeout=20)
            return completion.choices[0].message.content.strip()
        except Exception as e:
            if i == retries - 1: raise e
            time.sleep(2 ** i)

def ai_rapor_yaz(baslik, istek, veri, fin_data):
    if baslik == "SWOT ANALİZİ":
        sistem_prompt = "Sen dünyaca ünlü bir Stratejik İstihbarat (OSINT) ve Risk Yönetim uzmanısın. SWOT Analizini sıradan bir lise ödevi gibi değil; Yıkıcı İnovasyon, Regülatif Fırsatlar, Churn Regresyon Riskleri ve Makroekonomik Tehditler gibi ağır kurumsal alt başlıklarla incele."
    elif baslik == "YÖNETİCİ ÖZETİ":
        sistem_prompt = "Sen McKinsey seviyesinde bir Yönetici Ortaksın. Raporu sadece finansal metriklerle değil; projenin 'Ölüm Vadisi'ni nasıl aşacağını YORUMLA ve DESTANSI, vizyoner bir özet yaz."
    else:
        sistem_prompt = "Sen Goldman Sachs seviyesinde kıdemli bir kurumsal stratejistsin. ASLA yüzeysel özetler verme. Rakamları vizyonla birleştir."
        
    user_prompt = f"RAPOR KONUSU: {baslik}\nSİSTEM VERİLERİ: {veri}\nİflas Olasılığı: %{fin_data['prob_fail']}\nİSTENEN DERİN ANALİZ: {istek}"
    
    try:
        return safe_ai_call([{"role": "system", "content": sistem_prompt}, {"role": "user", "content": user_prompt}])
    except Exception as e:
        return f"<b>⚡ Simülasyon Devrede:</b> API gecikmesi nedeniyle rapor otonom oluşturuldu.<br><b>{baslik}:</b> Algoritmik Karar: <b>{fin_data['karar']}</b>. İflas Olasılığı: %{fin_data['prob_fail']:.1f}."

# ==========================================
# 6. SİDEBAR BÖLÜMÜ
# ==========================================
with st.sidebar:
    if os.path.exists("quantum_logo.png"): st.image("quantum_logo.png", use_container_width=True)
    elif os.path.exists("quantum logo.jpg"): st.image("quantum logo.jpg", use_container_width=True)
    
    st.markdown("---")
    with st.expander("👥 Ekibimiz", expanded=False):
        st.markdown("<div style='font-size: 0.90rem; color: #cbd5e1; line-height: 1.6; text-align: justify;'><b style='color: #60a5fa;'>Zeynep İNANÇ | Operasyon ve Proje Yöneticisi</b><br><b style='color: #60a5fa;'>Zeren İNANÇ | Sistem Entegrasyon Yöneticisi</b><br><b style='color: #60a5fa;'>Begüm AKPINAR | Finansal Strateji Uzmanı</b></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.header("📚 Örnek Senaryolar")
    st.selectbox("Yüklenecek Senaryoyu Seçin:", ["Seçiniz...", "☕ IoT Termos (Donanım)", "🤖 QuantumAI SaaS (Yazılım)", "🚁 AgriFly Drone (AgriTech)"], key="sen_sec_box", label_visibility="collapsed")
    st.button("📥 Seçili Senaryoyu Yükle", on_click=senaryo_tetikle, use_container_width=True)
    
    st.markdown("---")
    st.header("🧠 Kurucu Agent (Behavioral)")
    st.selectbox("Stokastik Kurucu Profili", ["Tier-1 (Kriz Yöneticisi)", "Standart Kurucu", "Çaylak (Yüksek Varyans)"], key="kurucu_profili")
    
    st.markdown("---")
    st.header("⚙️ Temel Parametreler")
    st.text_input("Girişim Adı", key="g_adi")
    st.text_input("Sektör", key="sek")
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

# ==========================================
# 7. ANA EKRAN VE STRATEJİK ANALİZ
# ==========================================
st.markdown('<div class="web-header">QUANTUM AI | STRATEJİK DEĞERLEME MOTORU</div>', unsafe_allow_html=True)

t1, t2 = st.tabs(["🎯 Pazar Problemi", "🛡️ Stratejik Çözüm"])
with t1: st.text_area("Pazar Analizi", key="kutu1", height=200, label_visibility="collapsed")
with t2: st.text_area("Çözüm", key="kutu2", height=200, label_visibility="collapsed")
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 STRATEJİK ANALİZİ BAŞLAT"):
    fin = finans_motoru(st.session_state.cap, st.session_state.maliyet, st.session_state.satis, st.session_state.adet, st.session_state.faiz, st.session_state.sub_price, st.session_state.sub_rate, st.session_state.paz_orani, st.session_state.op_orani, st.session_state.churn, st.session_state.vergi, st.session_state.enflasyon, st.session_state.pazar_hacmi, st.session_state.kurucu_profili)
    st.session_state.fin = fin
    st.session_state.op = fin['op']
    
    with st.status("🧠 Kuantum Motoru Derin Analizleri Derliyor...", expanded=True) as status:
        st.write("⚠️ **KRİTİK VERİ:** Institutional-grade simülasyon aktif. Retention Curve, FX Kur Riski ve Step-OPEX analizleri yapılıyor...")
        st.session_state.td_ozet = ai_rapor_yaz("YÖNETİCİ ÖZETİ", "Bu girişime yatırım yapılır mı?", f"Proje: {st.session_state.g_adi}, NPV: {fin['npv']}, MOIC: {fin['moic']:.1f}x", fin)
        
        st.write("💡 **YATIRIMCI REFLEKSİ:** Tornado (Hassasiyet) motoru devreye girdi...")
        st.session_state.td_finans = ai_rapor_yaz("FİNANSAL STRES ANALİZİ", "Şirketin nakit dayanıklılığını yorumla.", f"Runway: {fin['runway']} ay, LTV/CAC: {fin['ltv_cac']}", fin)
        
        st.write("🚨 **ACI GERÇEK:** M&A Çarpanları ve Kara Kuğu riskleri sentezleniyor...")
        st.session_state.td_porter = ai_rapor_yaz("PORTER 5 FORCES", "Rekabet gücünü analiz et.", f"Sektör: {st.session_state.sek}", fin)
        st.session_state.td_swot = ai_rapor_yaz("SWOT ANALİZİ", "Güçlü/zayıf yönleri yorumla.", f"Pazar Çözümü: {st.session_state.kutu2}", fin)
        
        st.write("🚪 **EXIT STRATEJİSİ:** M&A potansiyel alıcı profilleri sentezleniyor...")
        st.session_state.td_risk = ai_rapor_yaz("RİSK MATRİSİ", "Riskleri senaryolar halinde yaz.", f"Sektör: {st.session_state.sek}", fin)
        st.session_state.td_exit = ai_rapor_yaz("EXIT STRATEJİSİ", "Kim satın alabilir?", f"Proje: {st.session_state.g_adi}", fin)
        
        status.update(label="✅ Institutional-Grade Analiz Başarıyla Tamamlandı!", state="complete")
        st.session_state.analiz_hazir = True

# ==========================================
# 8. SONUÇLARI EKRANA BASMA (TORNADO CHART EKLENDİ)
# ==========================================
if st.session_state.analiz_hazir:
    fin = st.session_state.fin
    g_adi_safe = html.escape(st.session_state.g_adi)
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.5); border-left: 5px solid #8b5cf6; padding: 25px; border-radius: 16px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h4 style="color: #c4b5fd; margin-top: 0; font-size: 1.2rem;">🔗 Ultimate Quant-Grade Stress Layer</h4>
        <p style="font-size: 1.08rem; color: #f8fafc; margin: 0; line-height: 1.8;">
        • <b>Korelasyon & FX Şoku:</b> Makroekonomik şoklar hem talebi hem maliyeti tetikler. Enflasyona dayalı Kur Riski (USD/TRY FX Risk) Donanım ve OPEX'e basamaklı (Step-Function) olarak yedirilmiştir.<br>
        • <b>Retention Curve & Fallback Exit:</b> Churn oranı sabit tutulmamış, zamanla azalan Power-Law fonksiyonuyla modellenmiştir. EBITDA'nın negatif olduğu büyüme senaryolarında değerleme Ciro Çarpanına (Revenue Fallback) geçiş yapar.<br>
        • <b>Tornado Sensitivity Engine:</b> İflas olasılığı 'Şişman Kuyruk (Fat Tail)' ile kalibre edilmiş, model karar vermek için NPV'nin hangi parametreye en çok duyarlı olduğunu anlık hesaplamaktadır.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9)); padding:35px; border-radius:20px; border-left:12px solid {fin["renk"]}; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.05);"><h2 style="color:{fin["renk"]}; margin-top:0; letter-spacing: 1px; border:none;">SİSTEM KARARI: {fin["karar"]}</h2><h3 style="color:#6ee7b7; margin-top:15px;">💡 AI YÖNETİCİ ÖZETİ</h3><p style="font-size: 1.08rem; color:#f8fafc; margin-bottom:0; line-height: 1.8;">{st.session_state.td_ozet}</p></div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.markdown(f'<div class="metric-card"><div class="metric-title">NPV</div><div class="metric-value">{fin["npv"]:,.0f} ₺</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div class="metric-title">MOIC (Girişimci Çarpanı)</div><div class="metric-value">{fin["moic"]:.1f}x</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><div class="metric-title">D-LTV / CAC</div><div class="metric-value">{fin["ltv_cac"]:.1f}x</div></div>', unsafe_allow_html=True)
    
    runway_text = "∞" if fin["runway"] == 999 else f"{fin['runway']} Ay"
    m4.markdown(f'<div class="metric-card"><div class="metric-title">Runway (Peak Burn)</div><div class="metric-value">{runway_text}</div></div>', unsafe_allow_html=True)
    m5.markdown(f'<div class="metric-card" style="border-left-color: #f59e0b;"><div class="metric-title">Başabaş (ROI)</div><div class="metric-value">{fin["basabas"]} Ay</div></div>', unsafe_allow_html=True)
    
    fig1 = px.line(y=fin['cf'], x=["1. Yıl","2. Yıl","3. Yıl"], markers=True, color_discrete_sequence=['#60a5fa'])
    fig1.update_layout(title="1️⃣ 3 Yıllık Nakit Akışı", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    
    # 7 NUMARALI SENSITIVITY TORNADO GRAFİĞİ
    df_sens = pd.DataFrame(list(fin['sens_data'].items()), columns=['Parametre', 'NPV Değişimi (%)']).sort_values('NPV Değişimi (%)')
    fig7 = px.bar(df_sens, x='NPV Değişimi (%)', y='Parametre', orientation='h', color='NPV Değişimi (%)', color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'])
    fig7.update_layout(title="7️⃣ NPV Hassasiyet (Tornado) Analizi - 'Kill Switch' Tespiti", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    
    fig3 = go.Figure(data=go.Scatterpolar(r=fin['radar'], theta=['Kârlılık', 'Exit Çarpanı', 'İnovasyon', 'Elde Tutma'], fill='toself', marker=dict(color='#10b981')))
    fig3.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="3️⃣ Stratejik Radar", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    
    df_pie = pd.DataFrame({'Gider': ['Üretim', 'Pazarlama', 'Operasyon', 'Vergi'], 'Tutar': [fin['dm'], fin['paz'], st.session_state.op, fin['vergi']]})
    df_pie = df_pie[df_pie['Tutar'] > 0]
    fig4 = px.pie(df_pie, names='Gider', values='Tutar', hole=0.4, color_discrete_sequence=['#ef4444', '#f59e0b', '#3b82f6', '#8b5cf6'])
    fig4.update_layout(title="4️⃣ Operasyonel Gider Dağılımı", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    
    fig5 = go.Figure(go.Indicator(mode="gauge+number", value=max(0, fin['moic']*10), title={'text': "5️⃣ VC Puanı (MOIC Bazlı)"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#10b981"}}))
    fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    
    fig6 = px.histogram(x=fin['mc_npv'], nbins=50, color_discrete_sequence=['#ef4444' if fin['prob_fail'] > 50 else '#3b82f6'])
    fig6.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="İflas Sınırı (0 ₺)")
    fig6.update_layout(title=f"6️⃣ Monte Carlo Stres Testi (1.000 İterasyon)<br><span style='color:#ef4444;'>İflas Olasılığı (Probability of Failure): %{fin['prob_fail']:.1f}</span>", xaxis_title="Net Bugünkü Değer (NPV)", yaxis_title="Senaryo Sayısı", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    
    t1, t2 = st.tabs(["📊 7 BOYUTLU CANLI GRAFİKLER", "⚔️ KAPSAMLI STRATEJİK RAPORLAR"])
    
    with t1:
        g1, g2 = st.columns(2)
        g1.plotly_chart(fig1, use_container_width=True)
        g2.plotly_chart(fig7, use_container_width=True) # Tornado Grafiği
        
        g3, g4, g5 = st.columns(3)
        g3.plotly_chart(fig3, use_container_width=True)
        g4.plotly_chart(fig4, use_container_width=True)
        g5.plotly_chart(fig5, use_container_width=True)
        
        st.plotly_chart(fig6, use_container_width=True)
        
    with t2:
        st.markdown(f"<div class='report-section'><h3>1. FİNANSAL STRES ANALİZİ</h3>{st.session_state.td_finans}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>2. PORTER 5 FORCES PAZAR HAKİMİYETİ</h3>{st.session_state.td_porter}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>3. SWOT ANALİZİ</h3>{st.session_state.td_swot}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>4. RİSK MATRİSİ</h3>{st.session_state.td_risk}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>5. EXIT STRATEJİSİ VE POTANSİYEL ALICILAR</h3>{st.session_state.td_exit}</div>", unsafe_allow_html=True)
        st.markdown(szlk_html, unsafe_allow_html=True)
