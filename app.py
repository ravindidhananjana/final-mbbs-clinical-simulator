import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types
import random

# ─────────────────────────────────────────────────────────────────────────────
# 1. PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LK Final MBBS Clinical Simulator",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. MASTER CLINICAL SYLLABUS
# ─────────────────────────────────────────────────────────────────────────────
Syllabus = {
    "Medicine Long Cases": {
        "CVS": ["CCF", "Hypertension", "Chronic valve disease", "SABE", "Cor pulmonale",
                "Young hypertension", "MI", "Angina (stable / unstable)"],
        "RS": ["Pleural effusion", "Pneumonia", "Bronchiectasis", "Bronchial asthma",
               "Lung abscess", "COPD", "CA bronchus", "Haemoptysis"],
        "GUT": ["Nephrotic syndrome", "Acute nephritic syndrome", "Chronic nephritis",
                "CRF", "ARF", "UTI"],
        "GIT": ["Cirrhosis", "Amoebiasis - liver", "Infective hepatitis", "Jaundice",
                "Changes bowel habits", "Acute gastro-enteritis", "Hepatomegaly"],
        "Nervous & MS": ["Hemiplegia", "Peripheral neuritis", "Cx spondylosis",
                         "Epilepsy/Status Epilepticus", "Motor neurone disease", "Parkinsonism",
                         "CVA", "Wasting of muscles", "Hypertensive encephalopathy",
                         "Hepatic encephalopathy", "Meningitis", "SAH"],
        "Endocrine": ["DM", "Thyrotoxicosis", "Myxoedema", "Addison's disease"],
        "Systemic": ["Rheumatoid arthritis", "SLE"],
        "Haematological": ["Leukemia", "Anemia", "Haemolytic anaemia", "Multiple myeloma"],
        "Miscellaneous": ["PUO", "Sheehans syndrome", "Purpura"],
    },
    "Medicine Short Cases": {
        "CVS": ["ASD", "Congenital heart disease", "Valvular heart disease",
                "SVC/IVC obstruction", "MS/MR/AS/AR", "Various pulses"],
        "RS": ["Pneumothorax", "TB cavity", "Empyaema", "Lobar pneumonia",
               "Pleural effusion", "Emphysema"],
        "GIT": ["Hepatosplenomegaly", "Hepatomegaly", "Splenomegaly"],
        "Infections": ["Herpes zoster"],
        "Endocrine": ["Acromegaly", "Cushings syndrome", "Myxoedema"],
        "Systemic": ["Ankylosing spondylitis", "Rheumatoid arthritis", "Scleroderma"],
        "Nervous & MS": ["Foot drop", "Wrist drop", "Parkinsonism", "Motor neuron disease",
                         "Friedreich ataxia", "Neurofibromatosis", "Myasthenia gravis", "Ptosis",
                         "Bells palsy", "Spastic paralysis", "3rd nerve palsy",
                         "Cranial nerve palsies", "Rheumatic chorea", "Nystagmus",
                         "Gait abnormalities", "Horners syndrome", "Lateral medullary syndrome",
                         "Transverse myelitis", "Syringomyelia", "Paraplegia",
                         "Myopathies", "Claw hand", "Vertigo"],
        "Miscellaneous": ["Clubbing", "Purpura", "Pempigus"],
    },
    "Surgery Long Cases": {
        "Main": ["PVD", "CA breast", "CA oesophagus", "CA stomach", "Colorectal CA",
                 "Haematemesis", "Chronic pancreatitis",
                 "RIF mass (TB/CA caecum/Appendicular mass)", "Obstructive jaundice",
                 "Biliary disease", "Thyroid (MNG/Graves/Solitary nodule)", "BPH", "CA prostate"],
        "Head & Neck": ["Thyroid MNG without complication", "Thyroid MNG with complication",
                        "Primary CA of thyroid", "CA with secondaries in skull",
                        "Solitary lump in neck"],
        "Chest & Breast": ["CA breast", "Mass in breast"],
        "Vascular": ["Bergers disease", "Varicose veins", "Intermittent claudication", "PVD"],
        "GIT": ["CA oesophagus", "CA stomach", "CA colon", "CA ano rectum",
                "CA head of pancreas", "Pyloric stenosis with CA", "Pyloric obstruction",
                "Peptic ulcer", "Pseudo cyst of pancreas", "Chronic pancreatitis",
                "Chronic cholecystitis", "Obstructive jaundice", "Mucocoele in gallbladder",
                "Appendicular mass", "Amoebic liver", "Colostomy"],
        "GUT": ["Enlarged prostate", "BPH", "Painless haematuria", "Haematuria",
                "Renal carcinoma", "CA prostate"],
    },
    "Surgery Short Cases": {
        "Head & Neck": ["Submandibular gland calculi", "Parotitis", "Lump in the neck",
                        "Parotid swelling", "External angular dermoid", "Cx Lymphadenopathy",
                        "Ca tongue", "Malignant ulcers neck", "TB glands/Secondary LN neck",
                        "Cx rib/thoracic inlet syndrome", "Leukoplakia", "Trismus",
                        "Thyroglossal cyst", "Lingual thyroid", "Apical/Dentoalveolar abscess",
                        "Torticollis", "Sternomastoid tumor", "Pre auricular sinus",
                        "Tongue tie", "Ranula", "Black eye"],
        "Paediatric Surgery": ["Club foot", "Meningo myelocoele"],
        "Malignancies": ["CA maxillary antrum", "CA squamous cell", "Basal cell carcinoma",
                         "Malignant melanoma"],
        "Orthopaedics": ["Chronic osteomyelitis", "Bone tumours (Benign)",
                         "Plasters for fractures", "Recurrent dislocation of shoulder",
                         "Fracture Colles", "Osteoma skull", "Osteochondroma",
                         "Bone tumour", "Bursae around knee"],
        "Chest & Breast": ["Fibroadenoma of breast", "Paget's disease", "Gynaecomastia"],
        "Vascular": ["Thrombophlebitis", "Angiomas", "Venous malformations",
                     "Varicose veins", "A-V fistula", "Lymphoedema"],
        "Abdomen & Genitals": ["Hernia - epigastric", "Hernia - Inguinal", "Hernia - Umbilical",
                               "Hernia - Paraumbilical", "Hernia - Incisional", "Hernia - femoral",
                               "Hydrocoele", "Scrotal swelling", "Un/Mal descended testis",
                               "Retractile testis", "Spermatocoele / varicoele",
                               "Meatal stenosis", "Phimosis/Paraphimosis", "Anal fistula",
                               "Rectal prolapse", "Prolapsed Haemorrhoids",
                               "Ano rectal fistula", "Fistulae in ano", "Pilonidal sinus"],
        "Limbs & Trunk": ["Ulcer chronic (Venous / arterial / Traumatic)", "Cellulitis",
                          "Gangrene", "Ganglion", "Keloid", "Papilloma",
                          "Volkmann contracture", "Ulcer-Diabetic foot",
                          "Dupuytrens contracture", "Lipoma", "Nerve palsy wrist / foot drop",
                          "Cystic Hygroma", "Burns contracture", "Benign melanoma", "CTS",
                          "Callosity", "Paronychia", "Dermoid cyst", "Implantation dermoid",
                          "Madura foot", "Trigger finger", "Neurofibromatosis",
                          "Ingrowing toe nail", "Infected sebaceous cyst",
                          "Nerve entrapment syndrome", "Muscle haematoma",
                          "Intra muscular abscess", "Erysipelas"],
        "Miscellaneous": ["Mx stomach", "Mx IC tube", "Mx T tube", "Mx urine catheters"],
    },
    "Paediatric Long Cases": {
        "CVS": ["Rheumatic carditis"],
        "RS": ["Bronchiectasis", "Lung abscess", "Bronchial asthma"],
        "Endocrine": ["Cretinism"],
        "Hematological": ["Haemolytic anaemia", "Haemophilia", "Lymphoma",
                          "Thalassaemia", "ITP", "ALL"],
        "GIT": ["Hepatomegaly", "Viral hepatitis", "Diarrhoea", "Neonatal hepatitis",
                "Hirschsprung disease", "Shigellosis"],
        "Systemic": ["Stills disease (JIA)", "Rheumatoid arthritis"],
        "GUT": ["Acute nephritis", "Nephrotic syndrome", "UTI"],
        "Nervous & MS": ["Myopathies", "Paraplegia", "Rheumatic arthritis", "Cerebral palsy",
                         "Epilepsy", "Cerebral ataxia", "Hydrocephalus", "TB meningitis",
                         "Meningitis", "Meningism"],
        "Infectious": ["Rheumatic fever", "Glandular fever", "Malaria", "TB",
                       "Typhoid", "Dengue"],
        "Miscellaneous": ["Lymph adenopathy", "Neonatal jaundice", "Rickets", "Jaundice",
                          "Milestone regression", "Failure to thrive", "PUO"],
    },
    "Paediatric Short Cases": {
        "CVS": ["ASD/VSD", "Fallots", "MS/MR", "Infective endocarditis",
                "PDA", "Dextrocardia", "Cardiomyopathy"],
        "RS": ["Pneumonia"],
        "GIT": ["Hepatomegaly", "Hepatosplenomegaly"],
        "CNS & MS": ["Club foot", "Achondroplasia", "Meningocoele/Meningomyelocoele",
                     "Microcephaly", "Perthes", "CDH", "Erb's palsy",
                     "Syndactyly", "Spina bifida"],
        "Skin": ["Intertrigo", "Phrynoderma"],
        "Haematological": ["Thalassaemia", "Lymphatic Leukaemia", "Splenomegaly",
                           "Haemolytic anaemia", "Haemosiderosis"],
        "Systemic": ["Down syndrome", "Bitot spot", "Gutter pigmentation",
                     "Angioneurotic oedema", "Mongolism", "Turner's syndrome",
                     "Xerophthalmia", "Risus sardonicus"],
        "Neonatal EX": ["Development assessment"],
    },
    "Gynecology Cases": {
        "General": ["Abortion", "H. mole", "Ectopic pregnancy", "DUB",
                    "Post menopausal bleeding", "Amenorrhoea - Primary/Secondary",
                    "Dysmenorrhoea", "Haematocolpos", "Endometriosis", "Subfertility",
                    "Genital prolapse", "Bartholin cyst", "Stress incontinence",
                    "Hypertrophic elongation of Cx", "Chronic cervicitis / vaginitis",
                    "PID", "Vulval dystrophy", "Turner's", "Cx polyp", "UV fistula",
                    "Vaginal septum and polyp", "Cx erosion", "CA vulva",
                    "CA uterine body", "CA cervix", "Fibroid", "Ovarian tumor"],
    },
    "Obstetrics Cases": {
        "General": ["Unknown dates", "Elderly primi", "Grand multipara", "Heart disease",
                    "DM", "IUD", "Rh incompatibility", "Twin", "Anaemia in pregnancy",
                    "PIH", "HI in pregnancy", "APH", "Hydramnios",
                    "Abnormal presentation / Breech", "Fibroid complicating pregnancy",
                    "Past section", "Pyelonephritis in pregnancy", "Hyperemesis gravidarum",
                    "Normal pregnancy", "Placenta previa", "Preterm labour", "PROM",
                    "Non engaged / High head", "Post maturity", "Prolonged labour",
                    "Trial of labour", "Trial of scar", "Retained placenta",
                    "PPH", "Puerperal pyrexia"],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. CUSTOM CSS INJECTION
# ─────────────────────────────────────────────────────────────────────────────
def local_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Keyframes */
        @keyframes pulse {
            0%   { box-shadow: 0 0 15px rgba(247,148,29,0.2); border-color: rgba(247,148,29,0.4); transform: scale(0.97); }
            100% { box-shadow: 0 0 30px rgba(247,148,29,0.6); border-color: rgba(247,148,29,0.9); transform: scale(1.03); }
        }
        @keyframes fadeSlideIn {
            from { opacity: 0; transform: translateY(10px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* Page background */
        [data-testid="stAppViewContainer"] {
            background-color: #0b0c10;
            background-image: radial-gradient(rgba(247,148,29,0.04) 1px, transparent 1px);
            background-size: 24px 24px;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0); }

        h1,h2,h3,h4,h5,h6,.stMarkdown p {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #f1f3f9;
        }

        /* Main title gradient */
        .main-title {
            background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            font-size: 3.4rem !important;
            margin-bottom: 0.2rem;
            letter-spacing: -1px;
            line-height: 1.15;
            animation: fadeSlideIn 0.6s ease;
        }
        .main-subtitle {
            color: #e2e8f0;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            letter-spacing: -0.5px;
            animation: fadeSlideIn 0.7s ease;
        }

        /* Description card */
        .desc-card {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.06);
            backdrop-filter: blur(10px);
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.25);
            animation: fadeSlideIn 0.8s ease;
        }
        .desc-text {
            color: #b2b9c9 !important;
            font-size: 1.05rem !important;
            line-height: 1.7 !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #12131a;
            border-right: 1px solid rgba(255,255,255,0.05);
        }

        /* Sidebar cards */
        .custom-card {
            background-color: #1a1b23;
            padding: 1.25rem;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,0.04);
            transition: all 0.3s ease;
        }
        .custom-card:hover {
            transform: translateY(-3px);
            border-color: rgba(247,148,29,0.25);
            box-shadow: 0 12px 32px rgba(247,148,29,0.08);
        }
        .card-header {
            color: #717789;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.4rem;
            font-weight: 700;
        }
        .card-value {
            color: #fafafa;
            font-size: 1.15rem;
            font-weight: 600;
            line-height: 1.35;
        }

        /* Buttons */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #f7941d 0%, #ffaa4d 100%);
            color: white;
            border-radius: 25px;
            border: none;
            padding: 0.6rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease-in-out;
            width: 100%;
            box-shadow: 0 4px 15px rgba(247,148,29,0.2);
        }
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #ffaa4d 0%, #ffc080 100%);
            box-shadow: 0 6px 20px rgba(247,148,29,0.4);
            transform: translateY(-1px);
        }

        /* Chat input */
        [data-testid="stChatInput"] {
            background-color: #171821 !important;
            border-radius: 30px !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            padding: 5px 15px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            /* Make space for the mic button, Grammarly, and Send button on the right */
            padding-right: 110px !important; 
        }
        [data-testid="stChatInput"] textarea { 
            color: #fafafa !important; 
            padding-right: 110px !important;
        }

        /* Chat messages */
        .stChatMessage[data-testid="stChatMessage"] {
            border-radius: 16px;
            padding: 1.1rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            animation: fadeSlideIn 0.4s ease;
        }

        /* Status badges */
        .status-badge-sim {
            background: linear-gradient(135deg, rgba(46,213,115,0.15), rgba(46,213,115,0.04));
            border: 1px solid rgba(46,213,115,0.35);
            color: #2ed573;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-align: center;
            letter-spacing: 0.5px;
            margin-bottom: 1.2rem;
        }
        .status-badge-review {
            background: linear-gradient(135deg, rgba(247,148,29,0.15), rgba(247,148,29,0.04));
            border: 1px solid rgba(247,148,29,0.35);
            color: #f7941d;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-align: center;
            letter-spacing: 0.5px;
            margin-bottom: 1.2rem;
        }

        /* Progress bar */
        .progress-bar-container {
            width: 100%;
            background-color: rgba(255,255,255,0.05);
            border-radius: 10px;
            height: 6px;
            margin-top: 0.5rem;
            overflow: hidden;
        }
        .progress-bar-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.4s ease-in-out;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


local_css()

# ─────────────────────────────────────────────────────────────────────────────
# 4. API CLIENT
# ─────────────────────────────────────────────────────────────────────────────
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("⚠️ Gemini API Key not found. Please set GEMINI_API_KEY in `.streamlit/secrets.toml`.")
    st.stop()

# Model constants
TEXT_MODEL  = "gemini-3.1-flash-lite"

# ─────────────────────────────────────────────────────────────────────────────
# 5. CASE LOADER
# ─────────────────────────────────────────────────────────────────────────────
def load_new_case():
    exam_type      = random.choice(list(Syllabus.keys()))
    system_options = Syllabus[exam_type]
    system_station = random.choice(list(system_options.keys()))
    diagnosis      = random.choice(system_options[system_station])
    st.session_state.clinical_case = {
        "Exam Type":       exam_type,
        "System/Station":  system_station,
        "Diagnosis":       diagnosis,
        "Stage":           "PATIENT_SIM",
    }
    st.session_state.messages        = []
    st.session_state.examiner_review = None

# ─────────────────────────────────────────────────────────────────────────────
# 6. SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────────────────────────
if "clinical_case" not in st.session_state:
    load_new_case()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "examiner_review" not in st.session_state:
    st.session_state.examiner_review = None


# ─────────────────────────────────────────────────────────────────────────────
# 7. SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Animated stethoscope emblem
    st.markdown(
        """
        <div style="display:flex;justify-content:center;align-items:center;margin-top:1rem;margin-bottom:1.5rem;">
            <div style="
                background:linear-gradient(135deg,rgba(255,153,51,0.15),rgba(19,136,8,0.15));
                border:2px solid rgba(247,148,29,0.5);
                border-radius:50%;width:90px;height:90px;
                display:flex;justify-content:center;align-items:center;
                box-shadow:0 0 25px rgba(247,148,29,0.25);
                animation:pulse 2s infinite alternate;">
                <span style="font-size:2.6rem;">🩺</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stage = st.session_state.clinical_case["Stage"]
    if stage == "PATIENT_SIM":
        st.markdown('<div class="status-badge-sim">💬 PATIENT INTERVIEW ACTIVE</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge-review">🎓 EXAMINER REVIEW ACTIVE</div>',
                    unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="custom-card">
            <div class="card-header">Exam Context</div>
            <div class="card-value">{st.session_state.clinical_case['Exam Type']}</div>
        </div>
        <div class="custom-card">
            <div class="card-header">System / Station</div>
            <div class="card-value">{st.session_state.clinical_case['System/Station']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # History metrics
    q_count      = len([m for m in st.session_state.messages if m["role"] == "user"])
    progress_pct = min(100, int((q_count / 7) * 100))
    p_color      = "#2ed573" if progress_pct >= 70 else "#f7941d"
    hint_text    = ("💡 Ready to present? Type <b>'done'</b> to call the examiner."
                    if q_count >= 5
                    else "💡 Ask at least 5 questions for a comprehensive history.")

    st.markdown(
        f"""
        <div class="custom-card">
            <div class="card-header">History Metrics</div>
            <div class="card-value" style="display:flex;justify-content:space-between;align-items:center;">
                <span>Questions Asked:</span>
                <span style="color:{p_color};font-weight:700;">{q_count}</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width:{progress_pct}%;background:{p_color};"></div>
            </div>
            <div style="font-size:0.75rem;color:#888;margin-top:0.45rem;line-height:1.4;">
                {hint_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    if st.button("🔄 Next Random Case"):
        load_new_case()
        st.rerun()

    # Voice / Language legend
    if stage == "PATIENT_SIM":
        st.markdown(
            """
            <div style="margin-top:1rem;padding:0.9rem;background:#1a1b23;border-radius:10px;
                        border:1px solid rgba(255,255,255,0.04);">
                <div class="card-header" style="margin-bottom:0.6rem;">🌐 Language Support</div>
                <div style="font-size:0.8rem;color:#9aa0b2;line-height:1.8;">
                    🇱🇰 <b style="color:#f1f3f9;">Sinhala</b> script<br>
                    🔤 <b style="color:#f1f3f9;">Singlish</b> (Roman)<br>
                    🇬🇧 <b style="color:#f1f3f9;">English</b><br>
                    🎤 Click the mic icon in the chat box to dictate!
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# 8. MAIN HEADER & DESCRIPTION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">LK Final MBBS</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Clinical Case Simulator</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="desc-card">
        <div class="desc-text">
            🇱🇰 A clinical examination simulator tailored to <b>Sri Lankan state hospital ward environments</b>.
            Interview the patient to gather a comprehensive clinical history.
            Speak or type in <b>Sinhala, Singlish, or English</b> — the patient will respond in the same language.
            Once complete, type <b>'done'</b> to receive the External Examiner's structured evaluation.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 9. SHARED PROMPT CONTEXT
# ─────────────────────────────────────────────────────────────────────────────
current_diagnosis = st.session_state.clinical_case["Diagnosis"]
exam_type         = st.session_state.clinical_case["Exam Type"]
system_station    = st.session_state.clinical_case["System/Station"]

PATIENT_INSTRUCTION = (
    f"You are a Sri Lankan hospital patient admitted to a Teaching Hospital ward. "
    f"You have been diagnosed with '{current_diagnosis}' "
    f"(Exam category: '{exam_type}', System: '{system_station}').\n\n"
    f"[CRITICAL]: NEVER reveal the exact medical diagnosis name or clinical terminology to the student.\n\n"
    f"[SYMPTOMS]: Dynamically adapt your symptoms to perfectly match how a real patient with "
    f"'{current_diagnosis}' presents in a ward setting. Use layperson language only.\n\n"
    f"[LANGUAGE MIRROR — MOST IMPORTANT RULE]:\n"
    f"Detect the script/language of the student's latest message, then respond in the EXACT SAME language/script:\n"
    f"  • Sinhala script (e.g. 'මොකද අමාරුව?') → respond ONLY in colloquial Sinhala script.\n"
    f"    Use authentic ward expressions: 'බඩ රිදෙනවා', 'හුස්ම ගන්න අමාරුයි', 'කකුල් ඉදිමෙනවා',\n"
    f"    'ක්ලිනික් කාඩ් එක ගෙනාවා', 'රෝහලට ආවා', 'ප්‍රතිකාර ගන්නවා'.\n"
    f"  • Singlish / Roman script (e.g. 'mokada amaruwa?', 'bada ridenawada?') → respond in natural Singlish.\n"
    f"    Use: 'bada ridenawa', 'hama duwiliyama hariyala nehe', 'clinic eke card ekak thiyanawa'.\n"
    f"  • English → respond in simple, natural English with a realistic Sri Lankan patient persona.\n\n"
    f"[BREVITY]: Keep responses short and realistic. Reveal deeper history (family, social, medications) "
    f"only when directly asked."
)

EXAMINER_INSTRUCTION_BASE = (
    f"You are a Senior Consultant Physician and External Examiner for the University Final MBBS "
    f"Clinical Examination in Sri Lanka. The patient's actual diagnosis is '{current_diagnosis}'. "
)


# ─────────────────────────────────────────────────────────────────────────────
# 10. CHAT HISTORY DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    role   = message["role"]
    sender = message.get("sender")
    with st.chat_message(role):
        if sender == "Patient":
            st.markdown(
                "<div style='color:#a6b0c3;font-size:0.82rem;font-weight:700;"
                "margin-bottom:0.4rem;letter-spacing:0.5px;'>"
                "🩺 PATIENT</div>",
                unsafe_allow_html=True,
            )
        elif sender == "Examiner":
            st.markdown(
                "<div style='color:#f7941d;font-size:0.82rem;font-weight:700;"
                "margin-bottom:0.4rem;letter-spacing:0.5px;'>"
                "🎓 EXTERNAL EXAMINER</div>",
                unsafe_allow_html=True,
            )
        st.markdown(message["content"])


# ─────────────────────────────────────────────────────────────────────────────
# 11. INPUT HANDLING
# ─────────────────────────────────────────────────────────────────────────────
current_stage = st.session_state.clinical_case["Stage"]

def get_patient_text_response(contents: list) -> str | None:
    try:
        resp = client.models.generate_content(
            model=TEXT_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=PATIENT_INSTRUCTION,
                temperature=0.45,
            ),
        )
        return resp.text
    except Exception as e:
        if "429" in str(e):
            st.warning("⚠️ The patient is tired. API rate limit hit — please wait a moment and try again.")
        else:
            st.error(f"Patient model error: {e}")
        return None

if prompt := st.chat_input("Type here, or click mic to speak Sinhala/Singlish/English..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ── Trigger Examiner ──────────────────────────────────────────────────────
    if prompt.lower().strip() == "done" and current_stage != "EXAMINER_REVIEW":
        st.session_state.clinical_case["Stage"] = "EXAMINER_REVIEW"

        student_qs = [
            m["content"] for m in st.session_state.messages
            if m["role"] == "user" and m["content"].lower().strip() != "done"
        ]
        if not student_qs:
            st.warning("⚠️ You haven't asked the patient any questions yet! "
                       "Take a proper history before requesting an evaluation.")
            st.session_state.clinical_case["Stage"] = "PATIENT_SIM"
            st.rerun()

        with st.spinner("🎓 Examiner is reviewing your performance…"):
            history_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(student_qs)])
            examiner_full_instruction = (
                EXAMINER_INSTRUCTION_BASE
                + "The student just finished history-taking. "
                + "Below is the ONLY list of questions the student asked (patient replies are hidden). "
                + "Based solely on what the student chose to ask, evaluate their clinical performance in English. "
                + "Assess coverage of: Presenting Complaint, HPC, PMH, Drug/Allergy, Social/Family history. "
                + "Adopt the persona of an encouraging, fair Clinical Mentor. "
                + "You must STRICTLY address the user as 'you'—do NOT use titles like 'Doctor', 'Student', or 'Candidate'.\n\n"
                + "Format your evaluation EXACTLY as follows:\n\n"
                + "[A brief, natural conversational intro addressing the user directly as 'you' to start the review.]\n\n"
                + "🌟 WHAT YOU DID BRILLIANTLY:\n"
                + "(A bulleted list of history-taking aspects you handled well, using positive reinforcement.)\n\n"
                + "💡 AREAS TO REFINE & HOW TO FIX THEM:\n"
                + f"(A list of crucial history questions for '{current_diagnosis}' that you missed, along with warm, practical guidance on how to ask them and why they are important.)\n\n"
                + "📊 HISTORY-TAKING SCORE:\n"
                + "History Score: [A realistic, encouraging percentage score (e.g., 78%)]\n\n"
                + "💬 VIVA / DISCUSSION TRANSITION:\n"
                + "State clearly that the history-taking phase is now complete and we are moving to the clinical discussion. "
                + "Then, ask 1 or 2 clinical follow-up questions about this case (e.g., differentials, bedside/lab investigations, or physical signs expected) to initiate the viva."
            )
            examiner_contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(
                        text=f"Here are my history-taking questions:\n\n{history_text}\n\nPlease evaluate my performance."
                    )],
                )
            ]
            try:
                resp = client.models.generate_content(
                    model=TEXT_MODEL,
                    contents=examiner_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=examiner_full_instruction,
                        temperature=0.5,
                    ),
                )
                examiner_resp = resp.text
                st.session_state.examiner_review = examiner_resp
                st.session_state.messages.append(
                    {"role": "assistant", "content": examiner_resp, "sender": "Examiner"}
                )
            except Exception as e:
                st.error(f"Examiner generation error: {e}")
        st.rerun()

    # ── Patient Simulation (text) ─────────────────────────────────────────────
    elif current_stage == "PATIENT_SIM":
        with st.spinner("🩺 Patient is responding…"):
            formatted = [
                types.Content(
                    role="user" if m["role"] == "user" else "model",
                    parts=[types.Part.from_text(text=m["content"])],
                )
                for m in st.session_state.messages
            ]
            patient_resp = get_patient_text_response(formatted)
            if patient_resp:
                st.session_state.messages.append(
                    {"role": "assistant", "content": patient_resp, "sender": "Patient"}
                )
        st.rerun()

    # ── Examiner Viva (interactive) ───────────────────────────────────────────
    elif current_stage == "EXAMINER_REVIEW":
        with st.spinner("🎓 Examiner is responding…"):
            viva_instruction = (
                EXAMINER_INSTRUCTION_BASE
                + "You have already provided your initial critique. The student is now answering your viva questions "
                + "(differentials, expected physical signs, investigations, management). "
                + "Evaluate their reasoning using the encouraging, fair Clinical Mentor persona. "
                + "Strictly address the student as 'you' (do NOT use 'Doctor', 'Student', or 'Candidate'). "
                + "Be supportive, guide them towards the correct reasoning when they make mistakes, and ask 1-2 follow-up clinical questions to advance the viva."
            )
            formatted = [
                types.Content(
                    role="user" if m["role"] == "user" else "model",
                    parts=[types.Part.from_text(text=m["content"])],
                )
                for m in st.session_state.messages
            ]
            try:
                resp = client.models.generate_content(
                    model=TEXT_MODEL,
                    contents=formatted,
                    config=types.GenerateContentConfig(
                        system_instruction=viva_instruction,
                        temperature=0.5,
                    ),
                )
                examiner_resp = resp.text
                st.session_state.messages.append(
                    {"role": "assistant", "content": examiner_resp, "sender": "Examiner"}
                )
            except Exception as e:
                st.error(f"Examiner viva error: {e}")
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# 12. WEB SPEECH API MIC INJECTION
# ─────────────────────────────────────────────────────────────────────────────
def inject_mic_button():
    js_code = """
    <script>
    const parentDoc = window.parent.document;
    
    function getChatContainer() {
        return parentDoc.querySelector('[data-testid="stChatInput"]');
    }
    
    function initSpeechRecognition() {
        // Inject styles for the mic and enforce container padding
        if (!parentDoc.getElementById('mic-style')) {
            const style = parentDoc.createElement('style');
            style.id = 'mic-style';
            style.innerHTML = `
                @keyframes pulse-red {
                    0% { color: #717789; transform: translateY(-50%) scale(1); filter: drop-shadow(0 0 0 rgba(255,71,87,0)); }
                    50% { color: #ff4757; transform: translateY(-50%) scale(1.15); filter: drop-shadow(0 0 6px rgba(255,71,87,0.8)); }
                    100% { color: #717789; transform: translateY(-50%) scale(1); filter: drop-shadow(0 0 0 rgba(255,71,87,0)); }
                }
                .mic-recording {
                    animation: pulse-red 1.2s infinite !important;
                    color: #ff4757 !important;
                }
            `;
            parentDoc.head.appendChild(style);
        }

        let currentRecognition = null;
        let isRecording = false;
        
        // CRITICAL FIX: Streamlit reruns destroy the iframe context but leave the old button in the parent DOM.
        // We MUST remove the old button so we can bind a fresh onclick handler in this active context.
        const oldBtn = parentDoc.getElementById('custom-mic-btn');
        if (oldBtn) {
            oldBtn.remove();
        }
        
        // Create the button in memory
        const micBtn = parentDoc.createElement('button');
        micBtn.id = 'custom-mic-btn';
        micBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" x2="12" y1="19" y2="22"></line></svg>`;
        
        micBtn.style.background = 'transparent';
        micBtn.style.border = 'none';
        micBtn.style.color = '#717789';
        micBtn.style.cursor = 'pointer';
        micBtn.style.padding = '5px 10px';
        micBtn.style.position = 'absolute';
        micBtn.style.right = '55px'; // Placed directly left of the send button
        micBtn.style.top = '50%';
        micBtn.style.transform = 'translateY(-50%)';
        micBtn.style.zIndex = '999';
        micBtn.style.transition = 'all 0.3s ease';

        function stopRecording() {
            if (currentRecognition) {
                try { currentRecognition.abort(); } catch(e) {}
                currentRecognition = null;
            }
            isRecording = false;
            micBtn.classList.remove('mic-recording');
        }

        micBtn.onclick = (e) => {
            e.preventDefault();
            
            const SpeechRecognition = window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                console.log("Speech Recognition not supported in this browser.");
                return;
            }

            // If already recording, stop and return
            if (isRecording) {
                stopRecording();
                return;
            }

            // Ensure clean state before starting
            stopRecording();

            isRecording = true;
            micBtn.classList.add('mic-recording');

            // Instantiate a FRESH instance on every single click
            currentRecognition = new SpeechRecognition();
            currentRecognition.continuous = false;
            currentRecognition.interimResults = false;
            currentRecognition.lang = 'si-LK'; 

            currentRecognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                const container = getChatContainer();
                if (container) {
                    const textarea = container.querySelector('textarea');
                    if (textarea) {
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, "value").set;
                        const space = textarea.value ? " " : "";
                        nativeInputValueSetter.call(textarea, textarea.value + space + transcript);
                        
                        textarea.dispatchEvent(new parentDoc.defaultView.Event('input', { bubbles: true }));
                        
                        setTimeout(() => {
                            textarea.dispatchEvent(new parentDoc.defaultView.KeyboardEvent('keydown', {
                                bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13
                            }));
                        }, 150);
                    }
                }
                stopRecording();
            };

            currentRecognition.onend = () => { stopRecording(); };
            currentRecognition.onerror = (event) => { console.error("Mic error", event.error); stopRecording(); };

            try {
                currentRecognition.start();
            } catch(e) {
                console.error("Failed to start mic", e);
                stopRecording();
            }
        };

        // Robust interval to ensure mic button persists across Streamlit reruns
        setInterval(() => {
            const container = getChatContainer();
            if (container) {
                container.style.position = 'relative';
                if (!parentDoc.getElementById('custom-mic-btn')) {
                    container.appendChild(micBtn);
                    if (isRecording) {
                        // Reset state if Streamlit wiped the UI mid-recording
                        stopRecording();
                    }
                }
            }
        }, 500);
    }
    
    initSpeechRecognition();
    </script>
    """
    components.html(js_code, height=0, width=0)

# Inject the mic component (invisible iframe)
if current_stage == "PATIENT_SIM":
    inject_mic_button()