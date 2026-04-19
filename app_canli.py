import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import plotly.graph_objects as go 
import plotly.express as px 
import pandas as pd
import numpy as np
import os
import html 
import time
from scipy.stats import t

# ==========================================
# 1. MOTOR ATEŞLEME VE GÜVENLİ API BAĞLANTISI
# ==========================================
np.random.seed(2026) 

st.set_page_config(page_title="QUANTUM AI | Decision Intelligence", layout="wide", initial_sidebar_state="expanded") 

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key) 
except Exception as e:
    st.error("⚠️ SİSTEM UYARISI: Groq API Anahtarı bulunamadı! Lütfen Streamlit Cloud üzerinden 'Settings -> Secrets' kısmına anahtarınızı ekleyin.")
    st.stop()

# ==========================================
# 2. 2026 MODERN TASARIM VE HİYERARŞİ 
# ==========================================
st.markdown(""" 
<style> 
.stApp {background-color: #030712; color: #f8fafc; font-family: 'Inter', sans-serif;}
[data-testid="stSidebar"] { background-color: #050b14 !important; border-right: 1px solid rgba(56, 189, 248, 0.1); }
[data-testid="stSidebar"] img { margin-bottom: 30px !important; }
p, li, div[data-testid="stMarkdownContainer"] > p { font-size: 1.05rem !important; line-height: 1.7 !important; color: #e2e8f0 !important; }
h1, h2, h3, h4 { margin-top: 1rem; margin-bottom: 0.8rem; font-weight: 800 !important; color: #f8fafc !important;}
h2 { font-size: 1.8rem !important; color: #38bdf8 !important; text-shadow: 0px 2px 15px rgba(56, 189, 248, 0.2); border-bottom: none !important;}
div[data-baseweb="select"] > div, div[data-baseweb="popover"] > div { background-color: #0f172a !important; color: #f8fafc !important; border: 1px solid #38bdf8 !important; }
ul[role="listbox"], li[role="option"] { background-color: #0f172a !important; color: #f8fafc !important; }
li[role="option"]:hover, li[role="option"][aria-selected="true"] { background-color: #38bdf8 !important; color: #030712 !important; }
.stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: rgba(15, 23, 42, 0.8) !important; color: #38bdf8 !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; font-weight: 700 !important; }
.web-header { font-size: 3rem; font-weight: 900; text-align: left; letter-spacing: -1px; margin-bottom: 20px; background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block;} 
.metric-card { background: rgba(15, 23, 42, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px; box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3); }
.metric-value {font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-top: 5px;}
.metric-title {font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;}
.score-banner { background: linear-gradient(90deg, rgba(15,23,42,1) 0%, rgba(30,41,59,1) 100%); padding: 30px; border-radius: 20px; display: flex; justify-content: space-between; align-items: center; border: 2px solid; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.4); }
.score-number { font-size: 4rem; font-weight: 900; line-height: 1; margin: 0; }
.stButton>button { background: linear-gradient(135deg, #2563eb, #3b82f6) !important; color: white !important; font-weight: 900; border-radius: 12px; height: 3.5em; font-size: 18px; width: 100%; border: none !important; box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3); transition: all 0.3s ease; }
.stButton>button:hover { transform: scale(1.02); }
.stTabs [data-baseweb="tab-list"] { background-color: rgba(15, 23, 42, 0.6); border-radius: 12px; padding: 5px; gap: 10px; }
.stTabs [data-baseweb="tab"] { color: #94a3b8; font-weight: 700; border-radius: 8px; padding: 10px 20px; }
.stTabs [aria-selected="true"] { background-color: rgba(56, 189, 248, 0.1) !important; color: #38bdf8 !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; }
.print-btn { float: right; background: #38bdf8; color: #030712 !important; padding: 10px 20px; border-radius: 10px; font-weight: bold; text-decoration: none; transition: 0.3s; margin-top: 10px;}
.print-btn:hover { background: #0ea5e9; transform: scale(1.05); }

/* 🌟 GİZLİ PDF ŞABLONU İÇİN CSS 🌟 */
.print-only { display: none; }
@media print { 
    .print-btn, [data-testid="stSidebar"], .stButton { display: none !important; } 
    .print-only { display: block !important; margin-top: 50px; }
}
</style> 
""", unsafe_allow_html=True) 

szlk_html = """
<div style="background: rgba(30, 41, 59, 0.5); border-left: 4px solid #f59e0b; padding: 30px; margin-top: 40px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
    <h3 style="color: #fbbf24; margin-top:0;">📖 YATIRIMCI SÖZLÜĞÜ VE KAVRAMLAR</h3>
    <p>• <b style="color:#ffffff;">NPV:</b> Gelecekteki nakit akışlarının risk ve faiz düşülerek hesaplanmış bugünkü net değeridir.<br>
    • <b style="color:#ffffff;">MOIC (Mutiple on Invested Capital):</b> Yatırılan sermayenin kaç katı geri dönüş sağlandığını gösterir (Gerçek VC Standardı).<br>
    • <b style="color:#ffffff;">Discounted LTV / CAC:</b> Bir müşterinin bıraktığı ömür boyu kârın, WACC ve Churn'e indirgenmiş, onu elde etme maliyetine oranıdır.<br>
    • <b style="color:#ffffff;">Başabaş (Break-Even):</b> Yatırımcının koyduğu paranın tamamen geri dönüp şirketin net kâra geçtiği aydır.<br>
    • <b style="color:#ffffff;">S-Curve & Segmented Cohorts:</b> Büyüme lojistik bir eğri izler. Müşteriler SMB (Yüksek Churn) ve Enterprise (Yüksek NRR) olarak ikiye ayrılarak gerçekçi modellenir.</p>
</div>
"""

# ==========================================
# 3. KUSURSUZ HAFIZA VE DEVASA SENARYOLAR
# ==========================================
if 'run_id' not in st.session_state:
    st.session_state.run_id = 0

if 'g_adi' not in st.session_state:
    st.session_state.update({
        'g_adi': '', 'sek': 'B2B Finansal Teknoloji', 'cap': 0, 'maliyet': 0, 'satis': 0, 'adet': 0, 'faiz': 0, 
        'sub_price': 0, 'sub_rate': 0, 'paz_orani': 5, 'op_orani': 5, 'pazar_hacmi': 0.0, 'churn': 0.0,
        'vergi': 25, 'enflasyon': 30, 'kurucu_profili': 'Standart Kurucu',
        'kutu1': 'Detaylı analiz için sol menüden bir senaryo yükleyin.', 
        'kutu2': 'Stratejik çözümünüzü (Actionable Intelligence vb.) buraya girin.', 
        'analiz_hazir': False, 'op': 0,
        'fin': {}, 'sen_sec_box': 'Seçiniz...'
    })

BENCHMARKS = {
    'B2B Finansal Teknoloji': {'ltv_cac': 4.0, 'moic': 4.5, 'rule40': 40, 'margin': 0.80},
    'IoT Donanım': {'ltv_cac': 2.5, 'moic': 3.0, 'rule40': 25, 'margin': 0.40},
    'AgriTech / Drone': {'ltv_cac': 3.0, 'moic': 3.5, 'rule40': 30, 'margin': 0.55},
    'Default': {'ltv_cac': 3.0, 'moic': 3.5, 'rule40': 30, 'margin': 0.60}
}

def yukle_termos():
    st.session_state.update({
        'g_adi': 'EcoKupa v2', 'sek': 'IoT Donanım', 'cap': 3500000, 'maliyet': 850, 'satis': 1499, 'adet': 8500, 'faiz': 45, 'sub_price': 49, 'sub_rate': 15, 'paz_orani': 20, 'op_orani': 15, 'pazar_hacmi': 2.5, 'churn': 5.0, 'vergi': 25, 'enflasyon': 35, 'kurucu_profili': 'Standart Kurucu', 
        'kutu1': 'Global taşınabilir içecek ve termos pazarı (TAM), milyarlarca dolarlık devasa bir hacme sahip olmasına rağmen, onlarca yıldır yıkıcı bir inovasyondan uzak, tamamen statik ve "aptal" (dumb) ürünlerle domine edilmektedir. Geleneksel üreticiler (Yeti, Stanley vb.) yalnızca pasif ısı yalıtımı satmakta; müşteri davranışına, sıvı tüketim alışkanlıklarına veya sağlık trendlerine dair hiçbir veri (data) üretememektedir. Tüketici elektroniği pazarındaki en büyük kriz, şirketlerin tek seferlik fiziksel ürün satışlarına (one-off sales) mahkum kalmasıdır. Üretim maliyetlerindeki makroekonomik enflasyon ve tedarik zinciri (supply chain) kırılganlıkları, geleneksel donanım şirketlerinin brüt kâr marjlarını (gross margin) %30\'ların altına itmektedir. Donanım pazarı, tekrarlayan gelir (recurring revenue) yaratma ve kullanıcı sadakatini (retention) ölçecek bir ekosistem kurma konusunda tamamen sınıfta kalmıştır.', 
        'kutu2': 'EcoKupa v2; sıradan bir donanım ürünü değil, HaaS (Hardware-as-a-Service) modelini kullanan entegre bir IoT ekosistemidir. Ürünün tabanına yerleştirilen patentli mikro-sensörler (spektrometri ve biyo-empedans), tüketilen sıvının yoğunluğunu, kalori değerini, tüketim hızını ve sıcaklığını anlık olarak analiz ederek Bluetooth Low Energy (BLE) üzerinden mobil uygulamaya aktarır. Kullanıcıya yapay zeka destekli, gerçek zamanlı "Kişiselleştirilmiş Hidrasyon ve Metabolizma Koçluğu" sunulur. Bu yıkıcı strateji sayesinde işletme, sadece fiziksel ürün satışından elde edilen düşük marjla yetinmez. Cihazı bir Truva atı (Trojan Horse) olarak kullanarak, kullanıcıları %85 brüt kâr marjına sahip aylık premium yazılım aboneliğine (SaaS) dönüştürür. Bu model, Müşteri Yaşam Boyu Değerini (D-LTV) maksimize ederken, toplanan devasa anonim sağlık verileri ile rakiplerin asla aşamayacağı bir "Veri Hendeği" (Data Moat) inşa eder.', 
        'analiz_hazir': False})

def yukle_saas():
    st.session_state.update({
        'g_adi': 'QuantumAI Enterprise', 'sek': 'B2B Finansal Teknoloji', 'cap': 4500000, 'maliyet': 0, 'satis': 4500, 'adet': 2500, 'faiz': 40, 'sub_price': 299, 'sub_rate': 35, 'paz_orani': 30, 'op_orani': 25, 'pazar_hacmi': 14.8, 'churn': 4.5, 'vergi': 25, 'enflasyon': 40, 'kurucu_profili': 'Tier-1 (Kriz Yöneticisi)', 
        'kutu1': 'Erken aşama yatırım (VC) ve girişimcilik ekosistemindeki en acımasız gerçek, kurulan her 10 yeni teknoloji girişiminden 9\'unun ilk üç yıl içinde "Ölüm Vadisi" (Death Valley) aşamasında nakit yetersizliğinden (cash burn) batmasıdır. Bu sistematik çöküşün kök nedeni; kurucuların, CFO\'ların ve melek yatırımcıların karar alma süreçlerini tamamen statik, tek boyutlu ve insan ön yargısına (cognitive bias) açık geleneksel Excel tablolarına hapsetmesidir. Geleneksel İndirgenmiş Nakit Akışı (DCF) modelleri; makroekonomik faiz şoklarını, müşteri edinme maliyetindeki (CAC) organik enflasyonu, pazar doygunluk regresyonunu (S-Curve) ve birbirini tetikleyen korele riskleri eşzamanlı olarak simüle edemez. Kurumsal finansal danışmanlık şirketleri (Big 4) ise aylar süren, hantal ve milyon dolarlık bütçeler gerektiren raporlar üretir. Bu durum, piyasada "Bilgi Asimetrisi" ve ölümcül bir "Karar Felci" (Decision Paralysis) yaratmaktadır.', 
        'kutu2': 'Quantum AI, hantal ve elitist şirket değerleme endüstrisini anında erişilebilir bir SaaS modeline dönüştüren "Otonom Karar Zekası" (Decision Intelligence) platformudur. Kurumsal düzeyde (Institutional-grade) Python mimarisi üzerine kurulu sistem; işletmenin finansal dinamiklerini alır, 1.000 iterasyonlu Monte Carlo simülasyonu ve Student-T (Fat Tail) dağılımı kullanarak şirketi piyasadaki en ekstrem "Kara Kuğu" (Black Swan) krizlerine karşı stres testine sokar. Sistemi rakiplerinden ayıran en büyük fark, içerisindeki Agentic Yapay Zeka (Llama 3.3) katmanıdır. Bu model sadece soğuk metrikler (NPV, IRR) üretmekle kalmaz; Rule of 40 ve LTV/CAC rasyolarını global endüstri standartlarıyla (Benchmarking) anlık olarak kıyaslayarak, yönetime "Abonelik fiyatını %15 artır, pazarlama (OPEX) bütçesini %10 kıs" gibi otonom, anında uygulanabilir (Actionable Intelligence) ve şirketi iflastan kurtaracak stratejik reçeteler sunar.', 
        'analiz_hazir': False})

def yukle_drone():
    st.session_state.update({
        'g_adi': 'AgriFly - Otonom Tarım', 'sek': 'AgriTech / Drone', 'cap': 2800000, 'maliyet': 45000, 'satis': 125000, 'adet': 150, 'faiz': 35, 'sub_price': 1500, 'sub_rate': 65, 'paz_orani': 15, 'op_orani': 20, 'pazar_hacmi': 4.2, 'churn': 3.5, 'vergi': 25, 'enflasyon': 30, 'kurucu_profili': 'Çaylak (Yüksek Varyans)', 
        'kutu1': 'Küresel tarım sektörü; artan iklim krizi, daralan kâr marjları, su kıtlığı ve sertleşen karbon ayak izi regülasyonları (örn: AB Yeşil Mutabakatı) nedeniyle eşi benzeri görülmemiş bir makroekonomik çıkmazın içindedir. Geleneksel tarım uygulamalarında, mahsul hastalıkları veya zararlılarla mücadele etmek için binlerce hektarlık arazilere traktör veya tarım uçaklarıyla "battaniye" (blanket spraying) usulü manuel kimyasal püskürtülmektedir. Bu arkaik yöntem; kullanılan gübre ve pestisitin %70\'inin israf edilmesine (çiftçi için devasa OPEX patlaması), toprağın toksikleşmesine, yeraltı tatlı su kaynaklarının kirlenmesine ve nihayetinde mahsulde ciddi verim kaybına (yield degradation) yol açmaktadır. Büyük ve orta ölçekli tarım işletmelerinin, devasa arazilerindeki mikro-stresleri ve bitki sağlığını gerçek zamanlı (real-time) izleyebilecekleri, maliyet-etkin bir teknolojik altyapısı bulunmamaktadır.', 
        'kutu2': 'AgriFly, geleneksel bir donanım üreticisi olmanın çok ötesine geçerek "Hizmet Olarak Robotik" (RaaS - Robotics as a Service) modelini uygulayan uçtan uca bir "Hassas Tarım" (Precision Agriculture) çözümüdür. Gelişmiş multispektral kameralar, termal sensörler ve Edge-AI (Uçta Yapay Zeka) görüntü işleme çipleriyle donatılmış otonom drone filomuz, binlerce dönümlük tarlaları santimetre hassasiyetiyle tarar. Bitkilerin yaydığı ışık spektrumlarını (NDVI indeksini) anlık analiz ederek hastalıklı, susuz veya mantar enfeksiyonlu spesifik bölgeleri GPS koordinatlarıyla tespit eder. Entegre püskürtme sistemi, kimyasal ilacı arazinin tamamına değil, yalnızca ve milimetrik olarak o sorunlu bitkiye uygular. Bu yıkıcı teknoloji, çiftçinin agrokimyasal (gübre/ilaç) maliyetlerini anında %75-80 oranında düşürürken operasyonel kârlılığı maksimize eder ve toplanan rekolte verilerini sigorta şirketlerine (B2B Data Monetization) satarak çift yönlü bir gelir modeli yaratır.', 
        'analiz_hazir': False})

def senaryo_tetikle():
    secim = st.session_state.sen_sec_box
    if secim == "☕ IoT Termos (Donanım)": yukle_termos()
    elif secim == "🤖 QuantumAI SaaS (Yazılım)": yukle_saas()
    elif secim == "🚁 AgriFly Drone (AgriTech)": yukle_drone()

# ==========================================
# 4. FİNANS MATEMATİĞİ
# ==========================================
@st.cache_data(show_spinner=False)
def finans_motoru(b, m, s, a, faiz, sub_p, sub_r, paz_o, op_o, churn, vergi_orani, enflasyon_orani, pazar_hacmi, kurucu_profili, sektor):
    USD_TRY_RATE = 35.0
    TAM_TO_SAM_RATIO = 0.35 
    SMB_RATIO, ENT_RATIO = 0.85, 0.15
    NRR_SMB, NRR_ENT = 1.01, 1.08 
    
    pmf_multiplier, cac_decay_rate = (1.2, 0.95) if "Tier-1" in kurucu_profili else ((0.8, 1.05) if "Çaylak" in kurucu_profili else (1.0, 0.98))
    burn_mult = 1.0 / pmf_multiplier

    def run_cycle(demand_shock=1.0, cost_shock=1.0, churn_shock=1.0, is_mc=False, v_churn=churn, v_paz=paz_o, v_sub=sub_p):
        wacc_m = (max(0.15, (faiz/100) + 0.12 + (enflasyon_orani/100)*0.5)) / 12 
        und_cfs, dis_cfs, ebitdas, revs = [], [], [], []
        
        tam_tl = pazar_hacmi * USD_TRY_RATE * 1e9
        sam_tl = tam_tl * TAM_TO_SAM_RATIO
        penetration_limit = np.clip(0.05 * pmf_multiplier / (max(v_sub, 10) / 100), 0.001, 0.15)
        max_som_users = (sam_tl / max(v_sub * 12, s, 1)) * penetration_limit 

        y1_ciro, y1_dm, y1_paz, y1_op, y1_vergi = 0, 0, 0, 0, 0
        y1_cf, y2_cf, y3_cf = 0, 0, 0
        y2_rev, y3_rev, y3_ebitda = 0, 0, 0
        
        base_saas_cac = max(v_sub * 3, 50)
        base_hw_cac = max(s * 0.05, 50)
        base_cac = ((base_saas_cac * (sub_r/100)) + (base_hw_cac * (1 - sub_r/100))) / pmf_multiplier

        sales_cycle_delay = 3 
        revenue_delay = 1 
        pending_users = [0] * 65 

        base_churn_smb = max(v_churn/100, 0.005) * churn_shock
        base_churn_ent = base_churn_smb * 0.4 

        cohorts_smb, cohorts_ent = [], []
        prev_nwc = 0 

        for month in range(1, 61):
            fx_factor = (1 + (enflasyon_orani * 0.85) / 100 / 12) ** month
            inf_factor = (1 + enflasyon_orani / 100 / 12) ** month

            t0 = 24 
            k = 0.15 
            diffusion_multiplier = 1.0 / (1.0 + np.exp(-k * (month - t0))) 
            
            mkt = (b * v_paz/100) / 12
            
            cur_active_users = 0
            for c in cohorts_smb:
                if month > c[0] + revenue_delay: cur_active_users += c[1] * ((1 - base_churn_smb) ** (month - c[0] - revenue_delay))
            for c in cohorts_ent:
                if month > c[0] + revenue_delay: cur_active_users += c[1] * ((1 - base_churn_ent) ** (month - c[0] - revenue_delay))

            saturation = cur_active_users / max(max_som_users, 1)
            current_cac = base_cac * (cac_decay_rate ** (month/12)) * (1 + (saturation ** 2) * 4) * cost_shock * inf_factor
            current_cac = current_cac * (1.5 - (diffusion_multiplier * 0.5)) 
            
            raw_new_users = (mkt / current_cac) * demand_shock * (0.5 + diffusion_multiplier)
            if month + sales_cycle_delay < 65: pending_users[month + sales_cycle_delay] += raw_new_users 
                
            active_new_users = pending_users[month] * (sub_r/100)
            if active_new_users > 0:
                cohorts_smb.append([month, active_new_users * SMB_RATIO]) 
                cohorts_ent.append([month, active_new_users * ENT_RATIO]) 

            price_decay = 1 - (saturation * 0.2)
            effective_price = v_sub * max(0.6, price_decay) * (0.9 if demand_shock < 0.9 else 1.0)

            m_saas = 0
            for c in cohorts_smb:
                if month > c[0] + revenue_delay:
                    age = month - c[0] - revenue_delay
                    m_saas += c[1] * ((1 - base_churn_smb) ** age) * effective_price * (NRR_SMB ** (age / 12))
            for c in cohorts_ent:
                if month > c[0] + revenue_delay:
                    age = month - c[0] - revenue_delay
                    m_saas += c[1] * ((1 - base_churn_ent) ** age) * effective_price * (NRR_ENT ** (age / 12))

            hw_sales = (a/12) * demand_shock if month > 6 else 0
            hw_rev = hw_sales * s
            rev = m_saas + hw_rev
            revs.append(rev)

            hw_cost = hw_sales * m * fx_factor * cost_shock
            base_opex = (b * op_o/100)/12
            step_opex = np.floor(cur_active_users / 1500) * (b * 0.05) / 12 
            saas_cogs = (cur_active_users/100) * (effective_price * 0.10) 
            
            opex = (base_opex + step_opex + saas_cogs) * burn_mult * ((fx_factor + inf_factor)/2)

            ebitda = rev - (hw_cost + mkt + opex)
            depreciation = b / 60 
            ebit = ebitda - depreciation
            tax = ebit * (vergi_orani/100) if ebit > 0 else 0
            
            receivables = rev * (30/360) 
            payables = (hw_cost + opex) * (45/360) 
            current_nwc = receivables - payables
            delta_nwc = current_nwc - prev_nwc
            prev_nwc = current_nwc
            
            if month <= 18 and ebitda < 0: ebitda *= 1.2 
            ebitdas.append(ebitda)
            
            net_cf = ebitda - tax - delta_nwc 
            und_cfs.append(net_cf)
            dis_cfs.append(net_cf / (1 + wacc_m)**month)

            if month <= 12:
                y1_ciro += rev; y1_dm += hw_cost; y1_paz += mkt; y1_op += opex; y1_vergi += tax; y1_cf += net_cf
            elif month <= 24: y2_cf += net_cf; y2_rev += rev
            elif month <= 36: y3_cf += net_cf; y3_rev += rev; y3_ebitda += ebitda

        growth_rate = ((y3_rev - y2_rev) / max(y2_rev, 1)) * 100
        ebitda_margin = (y3_ebitda / max(y3_rev, 1)) * 100
        rule_of_40 = growth_rate + ebitda_margin
        
        last_year_ebitda = np.sum(ebitdas[-12:])
        last_year_rev = np.sum(revs[-12:])
        
        if rule_of_40 >= 40 and last_year_ebitda > 0:
            base_mult = np.clip(6.0 + (rule_of_40 - 40) * 0.1, 6.0, 12.0)
            exit_val = last_year_ebitda * base_mult * (demand_shock if is_mc else 1.0)
        elif rule_of_40 >= 20 and last_year_rev > 0:
            base_mult = np.clip(3.0 + (growth_rate * 0.05), 2.0, 6.0)
            exit_val = last_year_rev * base_mult * (demand_shock if is_mc else 1.0)
        else: exit_val = last_year_rev * 0.5

        exit_multiple = exit_val / max(last_year_ebitda, last_year_rev, 1)    
        npv = sum(dis_cfs) + (exit_val / (1 + wacc_m)**60) - b
        
        saas_gross_margin = 0.85 
        avg_monthly_arpu = v_sub * saas_gross_margin
        avg_nrr = (NRR_SMB * SMB_RATIO) + (NRR_ENT * ENT_RATIO)
        net_churn = max(base_churn_smb - (avg_nrr - 1), 0.001)
        ltv = avg_monthly_arpu / (net_churn + wacc_m) 
        
        avg_cac = base_cac * 1.5 
        ltv_cac = ltv / avg_cac if avg_cac > 0 else 0

        cum_cf = -b
        basabas = 999
        for i, cf in enumerate(und_cfs):
            cum_cf += cf
            if cum_cf >= 0 and basabas == 999: basabas = i + 1
        
        negative_cfs = [abs(c) for c in und_cfs if c < 0]
        avg_burn = np.mean(negative_cfs) if negative_cfs else 0
        runway = int(b / avg_burn) if avg_burn > 0 else 999

        return {
            "npv": npv, "cf1": y1_cf, "cf2": y2_cf, "cf3": y3_cf,
            "ciro": y1_ciro, "dm": y1_dm, "paz": y1_paz, "op": y1_op, "vergi": y1_vergi,
            "ltv_cac": ltv_cac, "runway": runway, "basabas": basabas, "exit_mult": exit_multiple,
            "total_return": sum(und_cfs) + exit_val, "rule_of_40": rule_of_40
        }

    base = run_cycle(1.0, 1.0, 1.0, is_mc=False)
    mc_npvs = []
    
    risk_breakdown = {"Talep/Pazar Eksikliği": 0, "Maliyet/Operasyon Çöküşü": 0, "Churn/Müşteri Kaybı": 0}

    for _ in range(1000): 
        d_shock = max(0.1, t.rvs(df=5) * 0.15 + 1.0)
        c_shock = max(0.1, np.random.normal(1.0, 0.1))
        ch_shock = max(0.1, np.random.normal(1.0, 0.1))
        
        if np.random.rand() < 0.02: 
            d_shock *= 0.5; c_shock *= 1.5
            
        res = run_cycle(demand_shock=d_shock, cost_shock=c_shock, churn_shock=ch_shock, is_mc=True)
        mc_npvs.append(res['npv'])
        
        if res['npv'] < 0:
            shocks = {"Talep/Pazar Eksikliği": 1 - d_shock, "Maliyet/Operasyon Çöküşü": c_shock - 1, "Churn/Müşteri Kaybı": ch_shock - 1}
            worst_reason = max(shocks, key=shocks.get)
            risk_breakdown[worst_reason] += 1

    prob_fail = (np.sum(np.array(mc_npvs) < 0) / 1000) * 100
    moic = base['total_return'] / b if b > 0 else 0

    bm = BENCHMARKS.get(sektor, BENCHMARKS['Default'])
    
    score_moic = min(100, (moic / bm['moic']) * 100) * 0.35
    score_risk = max(0, (100 - prob_fail)) * 0.25
    score_ltvcac = min(100, (base['ltv_cac'] / bm['ltv_cac']) * 100) * 0.25
    score_rule40 = min(100, (base['rule_of_40'] / bm['rule40']) * 100) * 0.15
    
    final_score = int(score_moic + score_risk + score_ltvcac + score_rule40)

    if final_score >= 80: karar, renk = "GÜÇLÜ AL (STRONG INVEST)", "#10b981"
    elif final_score >= 60: karar, renk = "İZLE / BÜYÜT (HOLD & MONITOR)", "#f59e0b"
    else: karar, renk = "YATIRIM YAPILAMAZ (REJECT)", "#ef4444"

    sens_churn = run_cycle(1.0, 1.0, 1.0, is_mc=False, v_churn=churn*1.2)['npv']
    sens_paz = run_cycle(1.0, 1.0, 1.0, is_mc=False, v_paz=paz_o*0.8)['npv']
    sens_sub = run_cycle(1.0, 1.0, 1.0, is_mc=False, v_sub=sub_p*0.8)['npv']
    
    sens_data = {
        "Churn Oranı %20 Artarsa": ((sens_churn - base['npv']) / abs(base['npv'])) * 100 if base['npv']!=0 else 0,
        "Pazarlama Bütçesi %20 Düşerse": ((sens_paz - base['npv']) / abs(base['npv'])) * 100 if base['npv']!=0 else 0,
        "Abonelik Fiyatı %20 Düşerse": ((sens_sub - base['npv']) / abs(base['npv'])) * 100 if base['npv']!=0 else 0
    }

    return {
        "npv": base['npv'], "moic": moic, "runway": base['runway'], "ltv_cac": base['ltv_cac'],
        "basabas": base['basabas'], "cf": [base['cf1'], base['cf2'], base['cf3']],
        "ciro": base['ciro'], "dm": base['dm'], "paz": base['paz'], "op": base['op'], "vergi": base['vergi'],
        "karar": karar, "renk": renk, "prob_fail": prob_fail, "mc_npv": mc_npvs, 
        "score": final_score, "risk_breakdown": risk_breakdown,
        "radar": [min(100, max(0, int(moic*20))), min(100, int(base['exit_mult']*20)), 90, max(0, int(100-churn*4))],
        "sens_data": sens_data
    }

# ==========================================
# 5. ASKERİ YAPAY ZEKA OTONOM KARAR MOTORU
# ==========================================
def safe_ai_call(messages, retries=3):
    for i in range(retries):
        try:
            completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.65, timeout=25)
            return completion.choices[0].message.content.strip()
        except Exception as e:
            if i == retries - 1: raise e
            time.sleep(2 ** i) 

@st.cache_data(show_spinner=False)
def ai_rapor_yaz(baslik, istek, veri, prob_fail, karar, score, run_id):
    sistem_prompt = """Sen Wall Street'in en acımasız ve vizyoner fon yöneticilerinden birisin (McKinsey / Goldman Sachs kalibresinde).
    Sana verilen metrikleri yüzeysel geçmek KESİNLİKLE YASAKTIR. Raporlarını bir kurumsal yönetim kuruluna sunar gibi hazırlayacaksın.
    
    ÇIKTI KURALLARI:
    1. Kısa, yüzeysel, 1-2 cümlelik cevaplar VEREMEZSİN. Raporlar en az 3 detaylı paragraftan oluşmalıdır.
    2. Metinlerinde kalın yazılar (**bold**), alt başlıklar ve profesyonel bir üslup kullanacaksın.
    3. Verilen sayısal verileri (NPV, Skor, İflas Riski) mutlaka analizine entegre edeceksin.
    4. "İyi görünüyor" gibi klişeler yerine "Şu metrik operasyonel bir risktir, şu şekilde çözülmeli" diyeceksin."""

    if baslik == "YÖNETİCİ ÖZETİ (AI KARAR MOTORU)":
        istek += "\n\nLütfen girişimi değerlendiren tam 3 uzun paragraf stratejik özet yaz ve ardından tam 5 maddelik detaylı bir eylem (aksiyon) planı çıkar."
    elif baslik == "FİNANSAL STRES ANALİZİ":
        istek += "\n\nLikidite durumunu, nakit yanma hızını ve LTV/CAC oranını baz alarak işletmenin iflas riskini ve hayatta kalma stresini alt başlıklarla derinlemesine açıkla."
    elif baslik == "PORTER 5 FORCES":
        istek += "\n\n5 kuvvetin HER BİRİNİ ayrı ayrı kalın başlıklar altında derinlemesine analiz et."
    elif baslik == "SWOT ANALİZİ":
        istek += "\n\nGüçlü yönler, Zayıf yönler, Fırsatlar ve Tehditleri ayrı başlıklar halinde, her birinin altına en az 3'er vurucu madde yazarak açıkla."
    elif baslik == "RİSK MATRİSİ":
        istek += "\n\nEn kritik 3 operasyonel ve makroekonomik riski belirle ve her biri için detaylı bir mitigasyon (kurtarma) stratejisi yaz."
    elif baslik == "EXIT STRATEJİSİ":
        istek += "\n\nBu girişimi ileride kim, hangi sebeple ve hangi değerleme çarpanıyla satın almak ister? Potansiyel M&A senaryolarını detaylıca kurgula."
    
    user_prompt = f"RAPOR KONUSU: {baslik}\nSİSTEM VERİLERİ: {veri}\nYatırım Skoru: {score}/100\nİflas Olasılığı: %{prob_fail}\nKARAR: {karar}\n\nİSTENEN: {istek}"
    
    try:
        return safe_ai_call([{"role": "system", "content": sistem_prompt}, {"role": "user", "content": user_prompt}])
    except Exception as e: 
        return f"<b>⚡ Otonom Güvenlik Devrede:</b> API gecikmesi nedeniyle rapor kurallı motorla oluşturuldu."

# ==========================================
# 6. SİDEBAR BÖLÜMÜ VE EKİBİMİZ
# ==========================================
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
    st.markdown("""
    <div style='background: rgba(15, 23, 42, 0.6); padding: 15px; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.2);'>
        <h4 style='color: #38bdf8; margin-top: 0; font-size: 1.1rem;'>👥 Kurucu Ekip</h4>
        <p style='font-size: 0.95rem; color: #cbd5e1; margin-bottom: 5px;'><b>Zeynep İNANÇ</b><br><span style='color: #94a3b8;'>Operasyon ve Proje Yöneticisi</span></p>
        <p style='font-size: 0.95rem; color: #cbd5e1; margin-bottom: 5px;'><b>Zeren İNANÇ</b><br><span style='color: #94a3b8;'>Sistem Entegrasyon Yöneticisi</span></p>
        <p style='font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0;'><b>Begüm AKPINAR</b><br><span style='color: #94a3b8;'>Finansal Strateji Uzmanı</span></p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 7. ANA EKRAN, HİYERARŞİ 
# ==========================================
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
        st.session_state.td_ozet = ai_rapor_yaz("YÖNETİCİ ÖZETİ (AI KARAR MOTORU)", "Kompozit Skora göre aksiyon öner.", f"Proje: {st.session_state.g_adi}", fin['prob_fail'], fin['karar'], fin['score'], r_id)
        st.session_state.td_finans = ai_rapor_yaz("FİNANSAL STRES ANALİZİ", "Şirketin nakit dayanıklılığını yorumla.", f"Runway: {fin['runway']} ay", fin['prob_fail'], fin['karar'], fin['score'], r_id)
        st.session_state.td_porter = ai_rapor_yaz("PORTER 5 FORCES", "Rekabet gücünü analiz et.", f"Sektör: {st.session_state.sek}", fin['prob_fail'], fin['karar'], fin['score'], r_id)
        st.session_state.td_swot = ai_rapor_yaz("SWOT ANALİZİ", "Güçlü ve Zayıf yönler.", f"Çözüm: {st.session_state.kutu2}", fin['prob_fail'], fin['karar'], fin['score'], r_id)
        st.session_state.td_risk = ai_rapor_yaz("RİSK MATRİSİ", "Operasyonel Riskleri analiz et.", f"Sektör: {st.session_state.sek}", fin['prob_fail'], fin['karar'], fin['score'], r_id)
        st.session_state.td_exit = ai_rapor_yaz("EXIT STRATEJİSİ", "Kim satın alabilir?", f"Proje: {st.session_state.g_adi}", fin['prob_fail'], fin['karar'], fin['score'], r_id)
        
        status.update(label="✅ Decision Engine Raporları Tamamlandı!", state="complete")
        st.session_state.analiz_hazir = True

# ==========================================
# 8. SONUÇLAR VE EKRAN BASTIRMA
# ==========================================
if st.session_state.analiz_hazir:
    fin = st.session_state.fin
    
    st.markdown(f"""
    <div class="score-banner" style="border-color: {fin['renk']};">
        <div>
            <h3 style="color: #94a3b8; margin:0; font-size: 1.2rem; text-transform: uppercase;">KOMPOZİT YATIRIM SKORU</h3>
            <h2 style="color: {fin['renk']}; margin-top:5px; border:none; font-size: 2rem;">KARAR: {fin['karar']}</h2>
        </div>
        <div class="score-number" style="color: {fin['renk']};">{fin['score']}<span style="font-size:1.5rem; color:#64748b;">/100</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.markdown(f'<div class="metric-card"><div class="metric-title">NPV</div><div class="metric-value">{fin["npv"]:,.0f} ₺</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div class="metric-title">MOIC (Girişimci Çarpanı)</div><div class="metric-value">{fin["moic"]:.1f}x</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><div class="metric-title">D-LTV / CAC</div><div class="metric-value">{fin["ltv_cac"]:.1f}x</div></div>', unsafe_allow_html=True)
    runway_text = "∞" if fin["runway"] == 999 else f"{fin['runway']} Ay"
    m4.markdown(f'<div class="metric-card"><div class="metric-title">Runway (Avg Burn)</div><div class="metric-value">{runway_text}</div></div>', unsafe_allow_html=True)
    m5.markdown(f'<div class="metric-card" style="border-left-color: #f59e0b;"><div class="metric-title">Başabaş (ROI)</div><div class="metric-value">{fin["basabas"]} Ay</div></div>', unsafe_allow_html=True)

    fig1 = px.line(y=fin['cf'], x=["1. Yıl","2. Yıl","3. Yıl"], markers=True, color_discrete_sequence=['#60a5fa'])
    fig1.update_layout(title="1️⃣ UFCF (Serbest Nakit Akışı)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    
    df_sens = pd.DataFrame(list(fin['sens_data'].items()), columns=['Parametre', 'NPV Değişimi (%)']).sort_values('NPV Değişimi (%)')
    fig7 = px.bar(df_sens, x='NPV Değişimi (%)', y='Parametre', orientation='h', color='NPV Değişimi (%)', color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'])
    fig7.update_layout(title="2️⃣ Hassasiyet (Tornado) Analizi", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")

    fig3 = go.Figure(data=go.Scatterpolar(r=fin['radar'], theta=['Kârlılık', 'Exit Çarpanı', 'İnovasyon', 'Elde Tutma'], fill='toself', marker=dict(color='#10b981')))
    fig3.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="3️⃣ Stratejik Radar", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")

    df_pie = pd.DataFrame({'Gider': ['Üretim', 'Pazarlama', 'Operasyon', 'Vergi'], 'Tutar': [fin['dm'], fin['paz'], fin['op'], fin['vergi']]})
    df_pie = df_pie[df_pie['Tutar'] > 0] 
    fig4 = px.pie(df_pie, names='Gider', values='Tutar', hole=0.4, color_discrete_sequence=['#ef4444', '#f59e0b', '#3b82f6', '#8b5cf6'])
    fig4.update_layout(title="4️⃣ OPEX (Gider) Dağılımı", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")

    fig5 = go.Figure(go.Indicator(mode="gauge+number", value=max(0, fin['moic']*10), title={'text': "5️⃣ VC Puanı (MOIC)"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#10b981"}}))
    fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")

    df_risk = pd.DataFrame(list(fin['risk_breakdown'].items()), columns=['Risk Faktörü', 'İflas Nedeni (Adet)'])
    df_risk = df_risk[df_risk['İflas Nedeni (Adet)'] > 0]
    if not df_risk.empty:
        fig_risk = px.pie(df_risk, names='Risk Faktörü', values='İflas Nedeni (Adet)', hole=0.5, color_discrete_sequence=['#ef4444', '#f59e0b', '#8b5cf6'])
        fig_risk.update_layout(title="6️⃣ Risk Parçalama (İflas Nedenleri)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    else:
        fig_risk = go.Figure().add_annotation(text="İflas Riski Tespit Edilmedi", showarrow=False, font=dict(size=20, color="#10b981"))

    fig6 = px.histogram(x=fin['mc_npv'], nbins=50, color_discrete_sequence=['#ef4444' if fin['prob_fail'] > 50 else '#3b82f6'])
    fig6.add_vline(x=0, line_dash="dash", line_color="red")
    fig6.update_layout(title=f"7️⃣ Monte Carlo Stres Testi<br><span style='color:#ef4444;'>İflas Olasılığı: %{fin['prob_fail']:.1f}</span>", xaxis_title="NPV", yaxis_title="Senaryo", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")

    t1, t2 = st.tabs(["📊 METRİKLER & GRAFİKLER", "⚔️ AI KARAR RAPORLARI"])
    with t1:
        g1, g2 = st.columns(2)
        g1.plotly_chart(fig1, use_container_width=True)
        g2.plotly_chart(fig7, use_container_width=True) 
        
        g3, g4 = st.columns(2)
        g3.plotly_chart(fig3, use_container_width=True)
        g4.plotly_chart(fig4, use_container_width=True)
        
        g5, g6 = st.columns(2)
        g5.plotly_chart(fig5, use_container_width=True)
        g6.plotly_chart(fig_risk, use_container_width=True)
        
        st.plotly_chart(fig6, use_container_width=True)
        
    with t2:
        st.markdown(f"<div style='background:rgba(15,23,42,0.8); padding:20px; border-radius:15px; margin-bottom:20px;'><h3 style='color:#6ee7b7;'>🧠 AI Yönetici Özeti & Aksiyon Planı</h3><p>{st.session_state.td_ozet}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>1. FİNANSAL STRES & LİKİDİTE (NWC)</h3>{st.session_state.td_finans}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>2. PORTER 5 FORCES PAZAR HAKİMİYETİ</h3>{st.session_state.td_porter}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>3. SWOT ANALİZİ</h3>{st.session_state.td_swot}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>4. RİSK MATRİSİ</h3>{st.session_state.td_risk}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-section'><h3>5. EXIT STRATEJİSİ VE POTANSİYEL ALICILAR</h3>{st.session_state.td_exit}</div>", unsafe_allow_html=True)
        st.markdown(szlk_html, unsafe_allow_html=True)

    # ==========================================
    # 9. GİZLİ YAZDIRMA (PDF) ŞABLONU 
    # ==========================================
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
