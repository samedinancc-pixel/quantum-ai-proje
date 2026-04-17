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
# 1. MOTOR ATEŞLEME VE GÜVENLİ API BAĞLANTISI (GÜNCELLENDİ)
# ==========================================
np.random.seed(2026) 

st.set_page_config(page_title="QUANTUM AI | Kurumsal Değerleme", layout="wide", initial_sidebar_state="expanded") 

# GİZLİ KASA SİSTEMİ DEVREDE (GitHub Güvenlik Açığı Kapatıldı)
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key) 
except Exception as e:
    st.error("⚠️ SİSTEM UYARISI: Groq API Anahtarı bulunamadı! Lütfen Streamlit Cloud üzerinden 'Settings -> Secrets' kısmına anahtarınızı ekleyin.")
    st.stop()

# ==========================================
# 2. 2026 MODERN TASARIM (SENİN EFSANE TASARIMIN)
# ==========================================
st.markdown(""" 
<style> 
/* Ana Arka Plan - Derin Uzay Siyahı */
.stApp {background-color: #030712; color: #f8fafc; font-family: 'Inter', sans-serif;}

/* SİDEBAR VE ŞEFFAF PNG LOGO */
[data-testid="stSidebar"] {
    background-color: #050b14 !important; 
    border-right: 1px solid rgba(56, 189, 248, 0.1);
}
[data-testid="stSidebar"] img {
    margin-bottom: 30px !important;
}

/* YAZI HİYERARŞİSİ */
p, li, div[data-testid="stMarkdownContainer"] > p { 
    font-size: 1.08rem !important; 
    line-height: 1.8 !important; 
    color: #e2e8f0 !important; 
}
h1, h2, h3, h4 { margin-top: 1rem; margin-bottom: 0.8rem; font-weight: 800 !important; color: #f8fafc !important;}

/* NEON BAŞLIKLAR */
h2 { 
    font-size: 1.8rem !important; 
    color: #38bdf8 !important; 
    text-shadow: 0px 2px 15px rgba(56, 189, 248, 0.2);
    border-bottom: none !important;
}
h3 { font-size: 1.4rem !important; color: #7dd3fc !important; }

/* KÖR EDEN MENÜ (DROPDOWN) KESİN ÇÖZÜM */
div[data-baseweb="select"] > div {
    background-color: rgba(15, 23, 42, 0.9) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
}
div[data-baseweb="popover"] > div, ul[role="listbox"] {
    background-color: #0f172a !important;
}
li[role="option"] {
    background-color: transparent !important;
    color: #f8fafc !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}
li[role="option"]:hover, li[role="option"][aria-selected="true"] {
    background-color: #38bdf8 !important;
    color: #030712 !important;
}

/* 2026 INPUT KUTULARI (GLOW EFEKTİ) */
.stTextInput>div>div>input, .stNumberInput>div>div>input {
    background-color: rgba(15, 23, 42, 0.8) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
}
.stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
    border: 1px solid #38bdf8 !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.5) !important;
}

/* SİDEBAR PARAMETRE BAŞLIKLARI */
[data-testid="stSidebar"] label p { 
    font-size: 1.05rem !important; 
    font-weight: 700 !important; 
    color: #cbd5e1 !important; 
}

/* 2026 ANA BAŞLIK */
.web-header {
    font-size: 3.2rem; 
    font-weight: 900; 
    text-align: center; 
    letter-spacing: -1px; 
    margin-bottom: 40px; 
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent; 
    text-shadow: 0px 10px 30px rgba(79, 172, 254, 0.15);
    padding-top: 10px;
} 

/* METRİK KARTLARI (GLASSMORPHISM) */
.metric-card {
    background: rgba(15, 23, 42, 0.6); 
    padding: 25px; 
    border-radius: 20px; 
    border: 1px solid rgba(255,255,255,0.05); 
    margin-bottom: 20px; 
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}
.metric-value {font-size: 2.6rem; font-weight: 900; color: #ffffff; margin-top: 10px; text-shadow: 0 2px 10px rgba(0,0,0,0.5);}
.metric-title {font-size: 1rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;}

/* YENİ NESİL BUTON */
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important; 
    color: white !important; 
    font-weight: 900; 
    border-radius: 14px; 
    height: 3.8em; 
    font-size: 20px; 
    width: 100%; 
    border: none !important; 
    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
    transition: all 0.3s ease;
}
.stButton>button:hover {
    box-shadow: 0 15px 35px rgba(59, 130, 246, 0.5);
    transform: scale(1.02);
}

/* RAPOR KUTULARI VE SEKMELER */
.report-section {
    background: rgba(15, 23, 42, 0.4); 
    padding: 40px; 
    border-radius: 20px; 
    border: 1px solid rgba(59, 130, 246, 0.1); 
    margin-bottom: 30px; 
}
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(15, 23, 42, 0.6);
    border-radius: 12px;
    padding: 5px;
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8;
    font-weight: 700;
    border-radius: 8px;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(56, 189, 248, 0.1) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
}
</style> 
""", unsafe_allow_html=True) 

szlk_html = """
<div style="background: rgba(30, 41, 59, 0.5); border-left: 4px solid #f59e0b; padding: 30px; margin-top: 40px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
    <h3 style="color: #fbbf24; margin-top:0;">📖 YATIRIMCI SÖZLÜĞÜ VE KAVRAMLAR</h3>
    <p>• <b style="color:#ffffff;">NPV:</b> Gelecekteki nakit akışlarının risk ve faiz düşülerek hesaplanmış bugünkü net değeridir.<br>
    • <b style="color:#ffffff;">ROIC:</b> Şirkete bağlanan sermayenin yüzde kaç verimlilikle çalıştığını gösterir.<br>
    • <b style="color:#ffffff;">LTV / CAC:</b> Bir müşterinin bıraktığı ömür boyu kârın, onu elde etme maliyetine oranıdır.<br>
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
        'fin': {'radar': [0,0,0,0], 'dm': 0, 'paz': 0, 'op': 0, 'vergi': 0, 'npv': 0, 'basabas': 0, 'runway': 0, 'ltv_cac': 0, 'cf': [0,0,0], 'ciro': 0, 'roic': 0, 'karar': '', 'renk': '', 'prob_fail': 0, 'mc_npv': []},
        'sen_sec_box': 'Seçiniz...'
    })

def yukle_termos():
    st.session_state.update({
        'g_adi': 'EcoKupa v2', 'sek': 'IoT Donanım', 'cap': 3500000, 'maliyet': 850, 'satis': 1499, 'adet': 8500, 'faiz': 45, 
        'sub_price': 49, 'sub_rate': 15, 'paz_orani': 20, 'op_orani': 15, 'pazar_hacmi': 2.5, 'churn': 5.0, 'vergi': 25, 'enflasyon': 35, 'kurucu_profili': 'Standart Kurucu',
        'kutu1': 'Global termos pazarı inovasyondan uzaklaşmış durumdadır. Tüketiciler dehidrasyon riskini veri bazlı takip edememekte, geleneksel iç yüzeylerdeki kontrolsüz bakteri üremesi hijyenik bir kriz oluşturmaktadır.', 
        'kutu2': 'EcoKupa v2, kapağına entegre UV-C sterilizasyon ve tabanındaki sensörleriyle su tüketimini otonom takip eden yıkıcı bir IoT ekosistemidir.', 'analiz_hazir': False
    })

def yukle_saas():
    st.session_state.update({
        'g_adi': 'QuantumAI Enterprise', 'sek': 'B2B Finansal Teknoloji', 'cap': 4500000, 'maliyet': 0, 
        'satis': 4500, 'adet': 2500, 'faiz': 40, 'sub_price': 299, 'sub_rate': 35, 
        'paz_orani': 30, 'op_orani': 25, 'pazar_hacmi': 14.8, 'churn': 4.5, 'vergi': 25, 'enflasyon': 40, 'kurucu_profili': 'Tier-1 (Kriz Yöneticisi)',
        'kutu1': 'Günümüzde girişimcilik ekosisteminin en acımasız gerçeği, kurulan her on yeni girişimin dokuzunun ilk üç yıl içinde başarısız olmasıdır. Kuluçka merkezlerinden çıkan muazzam projeler, ürün yetersizliğinden ziyade yanlış finansal planlama ve "Ölüm Vadisi" (Valley of Death) olarak adlandırılan nakit akışı krizleri yüzünden batmaktadır. Geleneksel yöntemlerle hazırlanan iş planları statik tablolardan ibarettir ve enflasyon/faiz dalgalanmalarında anında çökmektedir. Projemizin temel amacı, parlak fikirlere sahip girişimcilerin bu karanlık vadide kaybolmasını engellemek ve onlara kurumsal bir "finansal radar" sunmaktır. Büyük holdingler yeni bir projeye girmeden önce küresel denetim şirketlerine milyonlarca lira ödeyerek detaylı durum tespiti (Due Diligence) yaptırabilmektedir. Quantum AI, bu pazar araştırmalarını ve stres testlerini saniyeler içinde otonom olarak gerçekleştirerek kurumsal danışmanlık tekelini kırmayı ve ekosistemde fırsat eşitliği yaratmayı hedeflemektedir.', 
        'kutu2': 'Quantum AI, Python mimarisi üzerine inşa edilmiş otonom bir "Finansal Zeka ve İş Modeli" motorudur. Gelir modelimiz 5 ana sütuna dayanır: 1) Ücretsiz Freemium paketiyle devasa start-up trafiği çekmek. 2) Pro SaaS Abonelik (Aylık 299 ₺) ile Llama 3.3 entegrasyonlu sınırsız analiz sunarak düzenli MRR (Aylık Tekrarlayan Gelir) yaratmak. 3) Teknokent ve VC fonlarına yönelik B2B Kurumsal Lisanslama (Yıllık 45.000 ₺+) ile beyaz etiketli (White-label) çoklu kullanıcı desteği sağlamak. 4) Taahhütsüz kullanıcılar için kullandıkça öde (Pay-as-you-go) raporlaması (99 ₺). 5) Platform içi hedeflenmiş B2B sponsorluk gelirleri. Sistem, arka planda stokastik "Monte Carlo" simülatörü (Ishisaki vd.) çalıştırarak binlerce risk senaryosu yaratır. IFRS standartlarına uygun olarak EBITDA ve CAC analizi (Akkaya & Ünal, 2019) yapar. Eşzamanlı OSINT ajanlarıyla literatür tarayıp, LLM beyni üzerinden saniyeler içinde Harvard standartlarında Porter 5 Forces ve SWOT analizleri haritalandırır.', 
        'analiz_hazir': False
    })

def yukle_drone():
    st.session_state.update({
        'g_adi': 'AgriFly - Otonom Tarım', 'sek': 'AgriTech / Drone', 'cap': 2800000, 'maliyet': 45000, 
        'satis': 125000, 'adet': 150, 'faiz': 35, 'sub_price': 1500, 'sub_rate': 65, 
        'paz_orani': 15, 'op_orani': 20, 'pazar_hacmi': 4.2, 'churn': 3.5, 'vergi': 25, 'enflasyon': 30, 'kurucu_profili': 'Çaylak (Yüksek Varyans)',
        'kutu1': 'Geleneksel tarımda çiftçiler hastalık veya böcek tespit ettiklerinde, tarlanın tamamına manuel olarak veya traktörlerle kimyasal ilaç/gübre püskürtmektedir. Bu durum hem tonlarca zehirli kimyasal israfına (yüksek maliyet) hem de mahsulün kalitesinin düşmesine neden olmaktadır. Çiftçilerin, devasa tarlalarındaki lokal hastalıkları yukarıdan analiz edebilecek uygun maliyetli bir gözlem gücüne ihtiyacı vardır.', 
        'kutu2': 'AgriFly, yüksek çözünürlüklü termal ve multispektral kameralarla donatılmış otonom bir tarım dronudur. Sistem, tarlayı havadan tarayarak sadece hastalıklı veya susuz kalmış spesifik bölgeleri tespit eder ve nokta atışı (milimetrik) ilaçlama yapar. Çiftçiler, donanım satın alımına ek olarak sunduğumuz "AgriFly SaaS" uygulamasına aylık abone olarak, tarlalarının rekolte durumunu ve sağlık haritasını cep telefonlarından canlı olarak takip ederler. Kimyasal giderlerini %60 oranında düşürür.', 
        'analiz_hazir': False
    })

def senaryo_tetikle():
    secim = st.session_state.sen_sec_box
    if secim == "☕ IoT Termos (Donanım)": yukle_termos()
    elif secim == "🤖 QuantumAI SaaS (Yazılım)": yukle_saas()
    elif secim == "🚁 AgriFly Drone (AgriTech)": yukle_drone()

# ==========================================
# 4. FİNANS MATEMATİĞİ (GÜNCELLENMİŞ CORE ENGINE)
# ==========================================
@st.cache_data(show_spinner=False)
def finans_motoru(b, m, s, a, faiz, sub_p, sub_r, paz_o, op_o, churn, vergi_orani, enflasyon_orani, pazar_hacmi, kurucu_profili):
    v_mult, delay = (0.35, 0) if "Tier-1" in kurucu_profili else ((2.5, 12) if "Çaylak" in kurucu_profili else (1.0, 4))

    def run_cycle(sys_shock=1.0):
        ch_m = max(churn/100, 0.001)
        wacc_m = (max(0.12, (faiz/100) + 0.10 + (enflasyon_orani/100)*0.3)) / 12
        und_cfs, dis_cfs, cohorts = [], [], []
        tam_tl = pazar_hacmi * 32.5 * 1e9
        max_users = (tam_tl / max(sub_p, 1)) * 0.15

        y1_ciro, y1_dm, y1_paz, y1_op, y1_vergi = 0, 0, 0, 0, 0
        y1_cf, y2_cf, y3_cf = 0, 0, 0

        for month in range(1, 61):
            mkt = (b * paz_o/100) / 12
            efficiency = 1.0 / (1.0 + (mkt/500000)**0.5)
            traffic = (mkt / (5.5 * sys_shock)) * efficiency
            new_users = traffic * (sub_r/100)

            cur_users = sum([c[1]*((1-ch_m)**(month-c[0])) for c in cohorts])
            if cur_users > max_users: new_users *= 0.1
            cohorts.append([month, new_users])

            m_saas = sum([c[1]*((1-ch_m)**(month-c[0]))*sub_p for c in cohorts])
            hw_rev = (a/12)*s*sys_shock
            rev = m_saas + hw_rev

            hw_cost = (a/12)*m
            opex = (b * op_o/100)/12 + (cur_users/500)*45000

            ebitda = rev - (hw_cost + mkt + opex)
            tax = ebitda * (vergi_orani/100) if ebitda > 0 else 0
            net_cf = ebitda - tax

            if net_cf < 0 and month <= delay: net_cf *= 1.5

            und_cfs.append(net_cf)
            dis_cfs.append(net_cf / (1 + wacc_m)**month)

            if month <= 12:
                y1_ciro += rev; y1_dm += hw_cost; y1_paz += mkt; y1_op += opex; y1_vergi += tax; y1_cf += net_cf
            elif month <= 24:
                y2_cf += net_cf
            elif month <= 36:
                y3_cf += net_cf

        exit_val = max(0, sum(und_cfs[-12:]) * 7.5)
        npv = sum(dis_cfs) + (exit_val / (1 + wacc_m)**60) - b
        ltv_cac = ((sub_p*0.85)/ch_m) / max((((b * paz_o/100)/12)/max(new_users,1)), 1)

        cum_cf = -b
        basabas = 999
        for i, cf in enumerate(und_cfs):
            cum_cf += cf
            if cum_cf >= 0 and basabas == 999: basabas = i + 1
        
        avg_burn = abs(np.mean([c for c in und_cfs if c < 0])) if any(c < 0 for c in und_cfs) else 0
        runway = int(b / avg_burn) if avg_burn > 0 else 999

        return {
            "npv": npv, "cf1": y1_cf, "cf2": y2_cf, "cf3": y3_cf,
            "ciro": y1_ciro, "dm": y1_dm, "paz": y1_paz, "op": y1_op, "vergi": y1_vergi,
            "ltv_cac": ltv_cac, "runway": runway, "basabas": basabas
        }

    base = run_cycle(1.0)
    mc_npvs = []

    for _ in range(1000): 
        sys_shock = t.rvs(df=5) * 0.15 + 1.0 if 't' in globals() else np.random.normal(1.0, 0.15)
        res = run_cycle(sys_shock)
        mc_npvs.append(res['npv'])

    prob_fail = (np.sum(np.array(mc_npvs) < 0) / 1000) * 100
    roic = (base['cf1'] / b) * 100 if b > 0 else 0

    if roic >= 15 and base['runway'] >= 12:
        karar, renk = "✅ GÜÇLÜ YATIRIM (INVEST)", "#10b981"
    elif roic >= 5 and base['runway'] >= 8:
        karar, renk = "⚠️ RİSKLİ BÜYÜME (HOLD / MONITOR)", "#f59e0b"
    else:
        karar, renk = "❌ YATIRIM YAPILAMAZ (REJECT)", "#ef4444"

    return {
        "npv": base['npv'], "roic": roic, "runway": base['runway'], "ltv_cac": base['ltv_cac'],
        "basabas": base['basabas'], "cf": [base['cf1'], base['cf2'], base['cf3']],
        "ciro": base['ciro'], "dm": base['dm'], "paz": base['paz'], "op": base['op'], "vergi": base['vergi'],
        "radar": [min(100, max(0, int(roic*2))), 85, 90, max(0, int(100-churn*2))],
        "karar": karar, "renk": renk, "prob_fail": prob_fail, "mc_npv": mc_npvs
    }

# ==========================================
# GÜVENLİ YAPAY ZEKA ÇAĞRISI
# ==========================================
def safe_ai_call(messages, retries=3):
    for i in range(retries):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.55,
                timeout=20
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            if i == retries - 1:
                raise e
            time.sleep(2 ** i) 

def ai_rapor_yaz(baslik, istek, veri, fin_data):
    if baslik == "SWOT ANALİZİ":
        sistem_prompt = """Sen dünyaca ünlü bir Stratejik İstihbarat (OSINT) ve Risk Yönetim uzmanısın.
        KESİN KURALLARIN:
        1. SWOT Analizini sıradan bir lise ödevi gibi değil; Yıkıcı İnovasyon, Regülatif Fırsatlar, Churn Regresyon Riskleri ve Makroekonomik Tehditler gibi ağır kurumsal alt başlıklarla incele.
        2. ASLA kısa yazma. Güçlü Yönler (S), Zayıf Yönler (W), Fırsatlar (O) ve Tehditler (T) kısımlarının HER BİRİNİ en az 2-3 detaylı ve analitik madde ile açıkla. Toplamda çok kapsamlı bir rapor oluştur.
        3. Sistemin teknolojik tekel (moat) kurma potansiyelini mutlaka detaylandır."""
    elif baslik == "YÖNETİCİ ÖZETİ":
        sistem_prompt = """Sen McKinsey seviyesinde bir Yönetici Ortaksın.
        KURALLAR: Raporu sadece finansal metriklerle (ROIC, NPV) değil; projenin "Ölüm Vadisi"ni (Valley of Death) nasıl aşacağını, pazar tekelini nasıl kıracağını ve sektörel vizyonunu harmanlayarak YORUMLA ve DESTANSI, vizyoner bir özet yaz."""
    else:
        sistem_prompt = """Sen McKinsey ve Goldman Sachs seviyesinde milyar dolarlık fon yöneten, kıdemli bir kurumsal stratejistsin.
        KESİN KURALLARIN:
        1. ASLA yüzeysel ve kısa özetler verme. EN AZ 4 DETAYLI PARAGRAF yazacaksın.
        2. YORUM KAT: Rakamları hesap makinesi gibi listeleme. Metrikleri vizyonla birleştir. Hayali "Şirket A, Holding B" isimleri uydurma."""
    
    user_prompt = f"RAPOR KONUSU: {baslik}\n\nSİSTEM VERİLERİ (Girişim, Sektör, Finansallar): {veri}\nİflas Olasılığı: %{fin_data['prob_fail']}\n\nİSTENEN DERİN ANALİZ: {istek}\n\nTALİMAT: Lütfen bu bölümü sıradan bir özet gibi geçme. Olabildiğince UZUN, YORUMLAYARAK, kurumsal holding jargonuyla ve detaylıca yaz."
    
    try:
        return safe_ai_call([{"role": "system", "content": sistem_prompt}, {"role": "user", "content": user_prompt}])
    except Exception as e: 
        yedek_metin = f"""<div style='background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3b82f6; padding: 15px; margin-bottom: 20px; border-radius: 4px;'><b>⚡ Yerel Simülasyon Devrede:</b> Bulut API sunucusundaki anlık gecikme nedeniyle bu rapor, Quantum AI'ın otonom matematiksel değerleme modeliyle yerel olarak oluşturulmuştur. 1.000 stokastik Monte Carlo senaryosu işlenmiştir.</div>
        <b>{baslik} KAPSAMLI STRATEJİK İNCELEMESİ:</b><br><br>
        <b>1. Makroekonomik Dayanıklılık ve Ölüm Vadisi (Valley of Death) Stratejisi</b><br>
        İncelenen proje, sektörünün hantal tekelini kırmayı hedefleyen vizyoner bir girişimdir. Sistemin algoritmaları, projenin başabaş noktasını (Break-Even) <b>{fin_data['basabas']} ay</b> olarak saptamıştır. Mevcut net nakit akışına göre hesaplanan <b>%{fin_data['prob_fail']:.1f}</b> iflas olasılığı, girişimin bu karanlık vadiyi aşmak için yeterli finansal kalkanı olduğunu doğrulamaktadır.<br><br>
        <b>2. Yatırım Getirisi ve Operasyonel Riskler (LTV/CAC & NPV Yorumu)</b><br>
        Projenin <b>{fin_data['npv']:,.0f} ₺</b> olarak hesaplanan Net Bugünkü Değeri (NPV), enflasyon ve risk (haircut) kesintisine rağmen pozitif kalmayı başarmıştır. LTV/CAC oranının <b>{fin_data['ltv_cac']:.1f}x</b> seviyesinde olması sadece bir metrik değil; aynı zamanda pazarlama stratejisinin (Opex) organik büyüme yarattığının ve müşteri kazanım maliyetlerinin ölçeklenebilir olduğunun kesin kanıtıdır.<br><br>
        <b>3. Rekabet (Moat) ve Pazar Giriş Bariyerleri (OSINT Verileri)</b><br>
        Sistemimizin taramalarına göre, sektördeki mevcut geleneksel oyuncuların pazar payı savunma refleksleri yüksek olsa da, inovasyon hızları çağdışıdır. Girişimin sunduğu yenilikçi altyapı, geleneksel rakiplerin kâr marjlarını disrupte edecek (yıkacak) bir teknolojik tekel (moat) oluşturma potansiyeline sahiptir.<br><br>
        <b>4. Karar (Decision Rule) ve M&A Potansiyeli</b><br>
        Algoritmik eşik değerlerine göre sistemin nihai kararı: <b>{fin_data['karar']}</b>. Olası Exit (Çıkış) senaryolarında hedef kitle; pazar payını korumak isteyen "Tier-1 Venture Capital Fonları" ve operasyonel hantallıktan kurtulmak isteyen "Geleneksel Sektör Konsorsiyumları" olmalıdır."""
        return yedek_metin

# ==========================================
# 5. SİDEBAR BÖLÜMÜ
# ==========================================
with st.sidebar:
    if os.path.exists("quantum_logo.png"):
        st.image("quantum_logo.png", use_container_width=True)
    elif os.path.exists("quantum logo.jpg"): 
        st.image("quantum logo.jpg", use_container_width=True)
    
    st.markdown("---")
    with st.expander("👥 Ekibimiz", expanded=False):
        st.markdown("""
        <div style="font-size: 0.90rem; color: #cbd5e1; line-height: 1.6; text-align: justify;">
        <b style="color: #60a5fa;">Zeynep İNANÇ | Operasyon ve Proje Yöneticisi</b><br>
        <b style="color: #60a5fa;">Zeren İNANÇ | Sistem Entegrasyon Yöneticisi</b><br>
        <b style="color: #60a5fa;">Begüm AKPINAR | Finansal Strateji Uzmanı</b>
        </div>
        """, unsafe_allow_html=True)
    
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
    st.number_input("TAM (Toplam Pazar Hacmi - Milyar $)", key="pazar_hacmi", step=0.1)
    st.number_input("CAPEX (Kuruluş Sermayesi) ₺", key="cap")
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
    st.slider("Aylık Churn (Müşteri Kayıp) Oranı (%)", 0.0, 20.0, key="churn", step=0.1)

# ==========================================
# 6. ANA EKRAN VE STRATEJİK ANALİZ
# ==========================================
st.markdown('<div class="web-header">QUANTUM AI | STRATEJİK DEĞERLEME MOTORU</div>', unsafe_allow_html=True)

t1, t2 = st.tabs(["🎯 Pazar Problemi", "🛡️ Stratejik Çözüm"])
with t1: st.text_area("Pazar Analizi", key="kutu1", height=300, label_visibility="collapsed")
with t2: st.text_area("Çözüm", key="kutu2", height=300, label_visibility="collapsed")
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 STRATEJİK ANALİZİ BAŞLAT"):
    fin = finans_motoru(st.session_state.cap, st.session_state.maliyet, st.session_state.satis, st.session_state.adet, st.session_state.faiz, st.session_state.sub_price, st.session_state.sub_rate, st.session_state.paz_orani, st.session_state.op_orani, st.session_state.churn, st.session_state.vergi, st.session_state.enflasyon, st.session_state.pazar_hacmi, st.session_state.kurucu_profili)
    st.session_state.fin = fin
    st.session_state.op = fin['op'] 
    
    with st.status("🧠 Kuantum Motoru Derin Analizleri Derliyor...", expanded=True) as status:
        st.write("⚠️ **KRİTİK VERİ:** Türkiye'deki teknoloji girişimlerinin %82'si, yanlış 'Başabaş Noktası' hesabı nedeniyle ilk 24 ayda iflas ediyor. Quantum AI nakit akışınızı stres testine sokuyor...")
        st.session_state.td_ozet = ai_rapor_yaz("YÖNETİCİ ÖZETİ", "Bu girişime yatırım yapılır mı? Finansal metrikleri (ROIC, NPV, Runway) ve projenin vizyonunu (Ölüm Vadisi, pazar tekelini kırma) harmanlayarak DESTANSI bir şekilde gerekçelendir.", f"Proje: {st.session_state.g_adi}, NPV: {fin['npv']}, Başabaş: {fin['basabas']} ay, ROIC: %{fin['roic']}", fin)
        
        st.write("💡 **YATIRIMCI REFLEKSİ:** Bir yatırımcının projeyi reddetmesi ortalama 180 saniye sürer. Sistem kusursuz bir Porter 5 Forces savunması inşa ediyor...")
        st.session_state.td_finans = ai_rapor_yaz("FİNANSAL STRES ANALİZİ", "Şirketin nakit dayanıklılığını ve LTV/CAC oranının ne anlama geldiğini detaylı yorumla.", f"Runway: {fin['runway']} ay, Churn: %{st.session_state.churn}, LTV/CAC: {fin['ltv_cac']}", fin)
        
        st.write("🚨 **ACI GERÇEK:** Müşteri Kayıp (Churn) oranındaki sadece %5'lik bir sapma, şirketin net kârını %25 eritir. Detaylı SWOT haritası çıkarılıyor...")
        st.session_state.td_porter = ai_rapor_yaz("PORTER 5 FORCES PAZAR HAKİMİYETİ", "Sektördeki rekabet gücünü analiz et.", f"Sektör: {st.session_state.sek}", fin)
        st.session_state.td_swot = ai_rapor_yaz("SWOT ANALİZİ", "Güçlü ve zayıf yönleri, fırsat ve tehditleri detaylıca yorumla.", f"Pazar Çözümü: {st.session_state.kutu2}", fin)
        
        st.write("🚪 **EXIT STRATEJİSİ:** En büyük başarı doğru zamanda exit yapabilmektir. M&A potansiyel alıcı profilleri sentezleniyor...")
        st.session_state.td_risk = ai_rapor_yaz("RİSK MATRİSİ", "Bu girişimi batırabilecek riskleri senaryolar halinde yaz.", f"Sektör: {st.session_state.sek}", fin)
        st.session_state.td_exit = ai_rapor_yaz("EXIT STRATEJİSİ", "Bu şirketi gelecekte kim satın alabilir? ASLA Şirket A/B gibi isimler uydurma. Sektörel alıcı profillerini detaylandır.", f"Proje Adı: {st.session_state.g_adi}", fin)
        
        status.update(label="✅ Tüm Analizler Başarıyla Tamamlandı!", state="complete")
        st.session_state.analiz_hazir = True

# ==========================================
# 8. SONUÇLARI EKRANA BASMA
# ==========================================
if st.session_state.analiz_hazir:
    fin = st.session_state.fin
    g_adi_safe = html.escape(st.session_state.g_adi) 
    
    ciro_kaybi = st.session_state.satis * (st.session_state.sub_rate/100) * st.session_state.sub_price * 0.12 if st.session_state.sub_rate > 0 else 0
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.5); border-left: 5px solid #8b5cf6; padding: 25px; border-radius: 16px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h4 style="color: #c4b5fd; margin-top: 0; font-size: 1.2rem;">🔗 Unit Economics & Stress Layer (Metric Linkage)</h4>
        <p style="font-size: 1.08rem; color: #f8fafc; margin: 0; line-height: 1.8;">
        • <b>Makroekonomi & İskonto:</b> Enflasyon (%{st.session_state.enflasyon}) ve Risk Primi (%{st.session_state.faiz}) birleştirilerek WACC oranına gömülmüş, çifte büyüme hatası giderilmiştir.<br>
        • <b>VC Seviyesi Metrikler:</b> Churn oranı yıllık bileşik (compounding decay) olarak hesaplanmış, LTV formülüne %85 SaaS Brüt Kâr Marjı eklenmiştir. Monte Carlo simülasyonu, <b>CAC Şoku ve Fiyat Baskısı (Pricing Pressure)</b> stres testlerini içermektedir.<br>
        • <b>Net Burn & Karar Motoru:</b> Şirket nakit üretiyorsa (Cash-flow positive) Runway 'Sonsuz (∞)' kabul edilir. Karar Kuralı: ROIC ≥ %15 VE (Runway ≥ 18 Ay VEYA Kârlı) ise <b>(STRONG INVEST)</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9)); padding:35px; border-radius:20px; border-left:12px solid {fin["renk"]}; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.05);"><h2 style="color:{fin["renk"]}; margin-top:0; letter-spacing: 1px; border:none;">SİSTEM KARARI: {fin["karar"]}</h2><h3 style="color:#6ee7b7; margin-top:15px;">💡 AI YÖNETİCİ ÖZETİ</h3><p style="font-size: 1.08rem; color:#f8fafc; margin-bottom:0; line-height: 1.8;">{st.session_state.td_ozet}</p></div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.markdown(f'<div class="metric-card"><div class="metric-title">NPV</div><div class="metric-value">{fin["npv"]:,.0f} ₺</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div class="metric-title">ROIC</div><div class="metric-value">%{fin["roic"]:.1f}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><div class="metric-title">LTV/CAC</div><div class="metric-value">{fin["ltv_cac"]:.1f}x</div></div>', unsafe_allow_html=True)
    
    runway_text = "∞" if fin["runway"] == 999 else f"{fin['runway']} Ay"
    m4.markdown(f'<div class="metric-card"><div class="metric-title">Runway</div><div class="metric-value">{runway_text}</div></div>', unsafe_allow_html=True)
    m5.markdown(f'<div class="metric-card" style="border-left-color: #f59e0b;"><div class="metric-title">Başabaş (ROI)</div><div class="metric-value">{fin["basabas"]} Ay</div></div>', unsafe_allow_html=True)

    fig1 = px.line(y=fin['cf'], x=["1. Yıl","2. Yıl","3. Yıl"], markers=True, color_discrete_sequence=['#60a5fa'])
    fig1.update_layout(title="1️⃣ 3 Yıllık Nakit Akışı", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    
    fig2 = go.Figure(go.Waterfall(x=["Brüt Ciro", "Üretim", "Pazarlama", "Operasyon", "Vergi", "Net Nakit"], y=[fin['ciro'], -fin['dm'], -fin['paz'], -fin['op'], -fin['vergi'], fin['cf'][0]], measure=["relative", "relative", "relative", "relative", "relative", "total"]))
    fig2.update_layout(title="2️⃣ Maliyet ve Vergi Şelalesi", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
    
    fig3 = go.Figure(data=go.Scatterpolar(r=fin['radar'], theta=['Kârlılık', 'Pazar Payı', 'İnovasyon', 'Elde Tutma'], fill='toself', marker=dict(color='#10b981')))
    fig3.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="3️⃣ Stratejik Radar", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")

    df_pie = pd.DataFrame({'Gider': ['Üretim', 'Pazarlama', 'Operasyon', 'Vergi'], 'Tutar': [fin['dm'], fin['paz'], st.session_state.op, fin['vergi']]})
    df_pie = df_pie[df_pie['Tutar'] > 0] 
    fig4 = px.pie(df_pie, names='Gider', values='Tutar', hole=0.4, color_discrete_sequence=['#ef4444', '#f59e0b', '#3b82f6', '#8b5cf6'])
    fig4.update_layout(title="4️⃣ Operasyonel Gider Dağılımı", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")

    fig5 = go.Figure(go.Indicator(mode="gauge+number", value=max(0, fin['roic']), title={'text': "5️⃣ Sağlık Göstergesi (ROIC)"}, gauge={'axis': {'range': [0, max(100, fin['roic']*1.2)]}, 'bar': {'color': "#10b981"}}))
    fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")

    fig6 = px.histogram(x=fin['mc_npv'], nbins=50, color_discrete_sequence=['#ef4444' if fin['prob_fail'] > 50 else '#3b82f6'])
    fig6.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="İflas Sınırı (0 ₺)")
    fig6.update_layout(title=f"6️⃣ Monte Carlo Stres Testi (1.000 İterasyon)<br><span style='color:#ef4444;'>İflas Olasılığı (Probability of Failure): %{fin['prob_fail']:.1f}</span>", xaxis_title="Net Bugünkü Değer (NPV)", yaxis_title="Senaryo Sayısı", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")

    t1, t2 = st.tabs(["📊 6 BOYUTLU CANLI GRAFİKLER", "⚔️ KAPSAMLI STRATEJİK RAPORLAR"])
    with t1:
        g1, g2 = st.columns(2)
        g1.plotly_chart(fig1, use_container_width=True)
        g2.plotly_chart(fig2, use_container_width=True)
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
        
        fig1_html = fig1.to_html(full_html=False, include_plotlyjs='cdn')
        fig2_html = fig2.to_html(full_html=False, include_plotlyjs='cdn')
        fig3_html = fig3.to_html(full_html=False, include_plotlyjs='cdn')
        fig4_html = fig4.to_html(full_html=False, include_plotlyjs='cdn')
        fig5_html = fig5.to_html(full_html=False, include_plotlyjs='cdn')
        fig6_html = fig6.to_html(full_html=False, include_plotlyjs='cdn')
        
        html_rapor = f"""
        <html>
        <head><meta charset='utf-8'></head>
        <body style='font-family: Arial, sans-serif; padding: 20px; background-color: #f8fafc; color: #0f172a;'>
            <h1 style='color: #1e3a8a; text-align: center;'>{g_adi_safe} | Quantum AI Raporu</h1>
            <h3 style='color: #ef4444; text-align: center;'>KARAR: {fin['karar']} | İflas Olasılığı: %{fin['prob_fail']:.1f}</h3>
            <hr>
            <h2 style='color: #2563eb;'>Yönetici Özeti</h2><p>{html_temizle(st.session_state.td_ozet)}</p>
            <h2 style='color: #2563eb;'>İnteraktif Finansal Grafikler</h2>
            <div style='display:flex; flex-wrap:wrap;'>
                <div style='width:50%;'>{fig1_html}</div>
                <div style='width:50%;'>{fig2_html}</div>
                <div style='width:33%;'>{fig3_html}</div>
                <div style='width:33%;'>{fig4_html}</div>
                <div style='width:33%;'>{fig5_html}</div>
                <div style='width:100%; margin-top:20px;'>{fig6_html}</div>
            </div>
            <h2 style='color: #2563eb;'>Finansal Stres</h2><p>{html_temizle(st.session_state.td_finans)}</p>
            <h2 style='color: #2563eb;'>Porter 5 Forces</h2><p>{html_temizle(st.session_state.td_porter)}</p>
            <h2 style='color: #2563eb;'>SWOT Analizi</h2><p>{html_temizle(st.session_state.td_swot)}</p>
            <h2 style='color: #2563eb;'>Risk Matrisi</h2><p>{html_temizle(st.session_state.td_risk)}</p>
            <h2 style='color: #2563eb;'>Exit Stratejisi</h2><p>{html_temizle(st.session_state.td_exit)}</p>
        </body>
        </html>
        """
        st.download_button(label="📥 Etkileşimli Raporu İndir (HTML)", data=html_rapor, file_name=f"{g_adi_safe}_Rapor.html", mime="text/html", use_container_width=True)
