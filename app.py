import streamlit as st
from google import genai
from google.genai import types
import random

# --- 1. SET PAGE CONFIG (Must be the very first Streamlit command) ---
st.set_page_config(
    page_title="LK Final MBBS Clinical Simulator",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. THE MASTER SYLLABUS DIRECTORY ---
Syllabus = {
    "Medicine Long Cases": {
        "CVS": ["CCF", "Hypertension", "Chronic valve disease", "SABE", "Cor pulmonale", "Young hypertension", "MI", "Angina (stable / unstable)"],
        "RS": ["Pleural effusion", "Pneumonia", "Bronchiectasis", "Bronchial asthma", "Lung abscess", "COPD", "CA bronchus", "Haemoptysis"],
        "GUT": ["Nephrotic syndrome", "Acute nephritic syndrome", "Chronic nephritis", "CRF", "ARF", "UTI"],
        "GIT": ["Cirrhosis", "Amoebiasis - liver", "Infective hepatitis", "Jaundice", "Changes bowel habits", "Acute gastro-enteritis", "Hepatomegaly"],
        "Nervous & MS": ["Hemiplegia", "Peripheral neuritis", "Cx spondylosis", "Epilepsy/Status Epilepticus", "Motor neurone disease", "Parkinsonism", "CVA", "Wasting of muscles", "Hypertensive encephalopathy", "Hepatic encephalopathy", "Meningitis", "SAH"],
        "Endocrine": ["DM", "Thyrotoxicosis", "Myxoedema", "Addison's disease"],
        "Systemic": ["Rheumatoid arthritis", "SLE"],
        "Haematological": ["Leukemia", "Anemia", "Haemolytic anaemia", "Multiple myeloma"],
        "Miscellaneous": ["PUO", "Sheehans syndrome", "Purpura"]
    },
    "Medicine Short Cases": {
        "CVS": ["ASD", "Congenital heart disease", "Valvular heart disease", "SVC/IVC obstruction", "MS/MR/AS/AR", "Various pulses"],
        "RS": ["Pneumothorax", "TB cavity", "Empyaema", "Lobar pneumonia", "Pleural effusion", "Emphysema"],
        "GIT": ["Hepatosplenomegaly", "Hepatomegaly", "Splenomegaly"],
        "Infections": ["Herpes zoster"],
        "Endocrine": ["Acromegaly", "Cushings syndrome", "Myxoedema"],
        "Systemic": ["Ankylosing spondylitis", "Rheumatoid arthritis", "Scleroderma"],
        "Nervous & MS": ["Foot drop", "Wrist drop", "Parkinsonism", "Motor neuron disease", "Friedreich ataxia", "Neurofibromatosis", "Myasthenia gravis", "Ptosis", "Bells palsy", "Spastic paralysis", "3rd nerve palsy", "Cranial nerve palsies", "Rheumatic chorea", "Nystagmus", "Gait abnormalities", "Horners syndrome", "Lateral medullary syndrome", "Transverse myelitis", "Syringomyelia", "Paraplegia", "Myopathies", "Claw hand", "Vertigo"],
        "Miscellaneous": ["Clubbing", "Purpura", "Pempigus"]
    },
    "Surgery Long Cases": {
        "Main": ["PVD", "CA breast", "CA oesophagus", "CA stomach", "Colorectal CA", "Haematemesis", "Chronic pancreatitis", "RIF mass (TB/CA caecum/Appendicular mass)", "Obstructive jaundice", "Biliary disease", "Thyroid (MNG/Graves/Solitary nodule)", "BPH", "CA prostate"],
        "Head & Neck": ["Thyroid MNG without complication", "Thyroid MNG with complication", "Primary CA of thyroid", "CA with secondaries in skull", "Solitary lump in neck"],
        "Chest & Breast": ["CA breast", "Mass in breast"],
        "Vascular": ["Bergers disease", "Varicose veins", "Intermittent claudication", "PVD"],
        "GIT": ["CA oesophagus", "CA stomach", "CA colon", "CA ano rectum", "CA head of pancreas", "Pyloric stenosis with CA", "Pyloric obstruction", "Peptic ulcer", "Pseudo cyst of pancreas", "Chronic pancreatitis", "Chronic cholecystitis", "Obstructive jaundice", "Mucocoele in gallbladder", "Appendicular mass", "Amoebic liver", "Colostomy"],
        "GUT": ["Enlarged prostate", "BPH", "Painless haematuria", "Haematuria", "Renal carcinoma", "CA prostate"]
    },
    "Surgery Short Cases": {
        "Head & Neck": ["Submandibular gland calculi", "Parotitis", "Lump in the neck", "Parotid swelling", "External angular dermoid", "Cx Lymphadenopathy", "Ca tongue", "Malignant ulcers neck", "TB glands/Secondary LN neck", "Cx rib/thoracic inlet syndrome", "Leukoplakia", "Trismus", "Thyroglossal cyst", "Lingual thyroid", "Apical/Dentoalveolar abscess", "Torticollis", "Sternomastoid tumor", "Pre auricular sinus", "Tongue tie", "Ranula", "Black eye"],
        "Paediatric Surgery": ["Club foot", "Meningo myelocoele"],
        "Malignancies": ["CA maxillary antrum", "CA squamous cell", "Basal cell carcinoma", "Malignant melanoma"],
        "Orthopaedics": ["Chronic osteomyelitis", "Bone tumours (Benign)", "Plasters for fractures", "Recurrent dislocation of shoulder", "Fracture Colles", "Osteoma skull", "Osteochondroma", "Bone tumour", "Bursae around knee"],
        "Chest & Breast": ["Fibroadenoma of breast", "Paget's disease", "Gynaecomastia"],
        "Vascular": ["Thrombophlebitis", "Angiomas", "Venous malformations", "Varicose veins", "A-V fistula", "Lymphoedema"],
        "Abdomen & Genitals": ["Hernia - epigastric", "Hernia - Inguinal", "Hernia - Umbilical", "Hernia - Paraumbilical", "Hernia - Incisional", "Hernia - femoral", "Hydrocoele", "Scrotal swelling", "Un/Mal descended testis", "Retractile testis", "Spermatocoele / varicoele", "Meatal stenosis", "Phimosis/Paraphimosis", "Anal fistula", "Rectal prolapse", "Prolapsed Haemorrhoids", "Ano rectal fistula", "Fistulae in ano", "Pilonidal sinus"],
        "Limbs & Trunk": ["Ulcer chronic (Venous / arterial / Traumatic)", "Cellulitis", "Gangrene", "Ganglion", "Keloid", "Papilloma", "Volkmann contracture", "Ulcer-Diabetic foot", "Dupuytrens contracture", "Lipoma", "Nerve palsy wrist / foot drop", "Cystic Hygroma", "Burns contracture", "Benign melanoma", "CTS", "Callosity", "Paronychia", "Dermoid cyst", "Implantation dermoid", "Madura foot", "Trigger finger", "Neurofibromatosis", "Ingrowing toe nail", "Infected sebaceous cyst", "Nerve entrapment syndrome", "Muscle haematoma", "Intra muscular abscess", "Erysipelas"],
        "Miscellaneous": ["Mx stomach", "Mx IC tube", "Mx T tube", "Mx urine catheters"]
    },
    "Paediatric Long Cases": {
        "CVS": ["Rheumatic carditis"],
        "RS": ["Bronchiectasis", "Lung abscess", "Bronchial asthma"],
        "Endocrine": ["Cretinism"],
        "Hematological": ["Haemolytic anaemia", "Haemophilia", "Lymphoma", "Thalassaemia", "ITP", "ALL"],
        "GIT": ["Hepatomegaly", "Viral hepatitis", "Diarrhoea", "Neonatal hepatitis", "Hirschsprung disease", "Shigellosis"],
        "Systemic": ["Stills disease (JIA)", "Rheumatoid arthritis"],
        "GUT": ["Acute nephritis", "Nephrotic syndrome", "UTI"],
        "Nervous & MS": ["Myopathies", "Paraplegia", "Rheumatic arthritis", "Cerebral palsy", "Epilepsy", "Cerebral ataxia", "Hydrocephalus", "TB meningitis", "Meningitis", "Meningism"],
        "Infectious": ["Rheumatic fever", "Glandular fever", "Malaria", "TB", "Typhoid", "Dengue"],
        "Miscellaneous": ["Lymph adenopathy", "Neonatal jaundice", "Rickets", "Jaundice", "Milestone regression", "Failure to thrive", "PUO"]
    },
    "Paediatric Short Cases": {
        "CVS": ["ASD/VSD", "Fallots", "MS/MR", "Infective endocarditis", "PDA", "Dextrocardia", "Cardiomyopathy"],
        "RS": ["Pneumonia"],
        "GIT": ["Hepatomegaly", "Hepatosplenomegaly"],
        "CNS & MS": ["Club foot", "Achondroplasia", "Meningocoele/Meningomyelocoele", "Microcephaly", "Perthes", "CDH", "Erb's palsy", "Syndactyly", "Spina bifida"],
        "Skin": ["Intertrigo", "Phrynoderma"],
        "Haematological": ["Thalassaemia", "Lymphatic Leukaemia", "Splenomegaly", "Haemolytic anaemia", "Haemosiderosis"],
        "Systemic": ["Down syndrome", "Bitot spot", "Gutter pigmentation", "Angioneurotic oedema", "Mongolism", "Turner's syndrome", "Xerophthalmia", "Risus sardonicus"],
        "Neonatal EX": ["Development assessment"]
    },
    "Gynecology Cases": {
        "General": ["Abortion", "H. mole", "Ectopic pregnancy", "DUB", "Post menopausal bleeding", "Amenorrhoea - Primary/Secondary", "Dysmenorrhoea", "Haematocolpos", "Endometriosis", "Subfertility", "Genital prolapse", "Bartholin cyst", "Stress incontinence", "Hypertrophic elongation of Cx", "Chronic cervicitis / vaginitis", "PID", "Vulval dystrophy", "Turner's", "Cx polyp", "UV fistula", "Vaginal septum and polyp", "Cx erosion", "CA vulva", "CA uterine body", "CA cervix", "Fibroid", "Ovarian tumor"]
    },
    "Obstetrics Cases": {
        "General": ["Unknown dates", "Elderly primi", "Grand multipara", "Heart disease", "DM", "IUD", "Rh incompatibility", "Twin", "Anaemia in pregnancy", "PIH", "HI in pregnancy", "APH", "Hydramnios", "Abnormal presentation / Breech", "Fibroid complicating pregnancy", "Past section", "Pyelonephritis in pregnancy", "Hyperemesis gravidarum", "Normal pregnancy", "Placenta previa", "Preterm labour", "PROM", "Non engaged / High head", "Post maturity", "Prolonged labour", "Trial of labour", "Trial of scar", "Retained placenta", "PPH", "Puerperal pyrexia"]
    }
}

# --- 3. CUSTOM CSS INJECTION ---
def local_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* --- Custom Keyframes for Animations --- */
        @keyframes pulse {
            0% {
                box-shadow: 0 0 15px rgba(247, 148, 29, 0.2);
                border-color: rgba(247, 148, 29, 0.4);
                transform: scale(0.97);
            }
            100% {
                box-shadow: 0 0 30px rgba(247, 148, 29, 0.6);
                border-color: rgba(247, 148, 29, 0.9);
                transform: scale(1.03);
            }
        }

        /* --- General Page & Text styling --- */
        [data-testid="stAppViewContainer"] {
            background-color: #0b0c10;
            background-image: radial-gradient(rgba(247, 148, 29, 0.04) 1px, transparent 1px);
            background-size: 24px 24px;
        }

        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        
        h1, h2, h3, h4, h5, h6, .stMarkdown p {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #f1f3f9;
        }

        /* --- Main Title Gradient --- */
        .main-title {
            background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            font-size: 3.4rem !important;
            margin-bottom: 0.2rem;
            letter-spacing: -1px;
            line-height: 1.15;
        }
        
        .main-subtitle {
            color: #e2e8f0;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            letter-spacing: -0.5px;
        }

        .desc-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(10px);
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        }

        .desc-text {
            color: #b2b9c9 !important;
            font-size: 1.05rem !important;
            line-height: 1.6 !important;
        }

        /* --- Sidebar styling --- */
        [data-testid="stSidebar"] {
            background-color: #12131a;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        [data-testid="stSidebar"] [data-testid="stImage"] {
            margin-bottom: 1rem;
        }

        /* --- Custom Cards in Sidebar --- */
        .custom-card {
            background-color: #1a1b23;
            padding: 1.25rem;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.04);
            transition: all 0.3s ease;
        }
        
        .custom-card:hover {
            transform: translateY(-3px);
            border-color: rgba(247, 148, 29, 0.25);
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

        /* --- Buttons Styling --- */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #f7941d 0%, #ffaa4d 100%);
            color: white;
            border-radius: 25px;
            border: none;
            padding: 0.6rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease-in-out;
            width: 100%;
            box-shadow: 0 4px 15px rgba(247, 148, 29, 0.2);
        }
        
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #ffaa4d 0%, #ffc080 100%);
            box-shadow: 0 6px 20px rgba(247, 148, 29, 0.4);
            color: white;
        }

        /* --- Chat Input Container --- */
        [data-testid="stChatInput"] {
            background-color: #171821 !important;
            border-radius: 30px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            padding: 5px 15px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        [data-testid="stChatInput"] textarea {
            color: #fafafa !important;
        }

        /* --- Chat Message Styling (Patient & Examiner) --- */
        .stChatMessage[data-testid="stChatMessage"] {
            border-radius: 16px;
            padding: 1.1rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .stChatMessage[data-testid="stChatMessage"][data-testid="stChatMessage-user"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        
        .stChatMessage[data-testid="stChatMessage"][data-testid="stChatMessage-assistant"] {
            background: linear-gradient(135deg, rgba(247, 148, 29, 0.03) 0%, rgba(0,0,0,0) 100%);
            border: 1px solid rgba(247, 148, 29, 0.12);
            border-left: 4px solid #f7941d;
        }

        /* --- Status Badges --- */
        .status-badge-sim {
            background: linear-gradient(135deg, rgba(46, 213, 115, 0.15) 0%, rgba(46, 213, 115, 0.04) 100%);
            border: 1px solid rgba(46, 213, 115, 0.35);
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
            background: linear-gradient(135deg, rgba(247, 148, 29, 0.15) 0%, rgba(247, 148, 29, 0.04) 100%);
            border: 1px solid rgba(247, 148, 29, 0.35);
            color: #f7941d;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-align: center;
            letter-spacing: 0.5px;
            margin-bottom: 1.2rem;
        }

        /* --- Progress Bar --- */
        .progress-bar-container {
            width: 100%;
            background-color: rgba(255, 255, 255, 0.05);
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

        /* --- Final Review Panel --- */
        .review-panel {
            background: linear-gradient(135deg, rgba(247, 148, 29, 0.04) 0%, rgba(247, 148, 29, 0.01) 100%);
            border: 1px solid rgba(247, 148, 29, 0.3);
            border-radius: 16px;
            padding: 1.75rem;
            box-shadow: 0 12px 36px rgba(247, 148, 29, 0.08);
            margin-top: 1.5rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

local_css()

# --- 4. API KEY SETUP ---
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("Gemini API Key not found. Please set it in `.streamlit/secrets.toml` or Streamlit Cloud Secrets.")
        st.stop()

api_key = get_api_key()
client = genai.Client(api_key=api_key)

# --- 5. FUNCTION TO REFRESH CASE ---
def load_new_case():
    # Use Syllabus directly (no cache) to ensure all categories are always available
    syllabus_types = list(Syllabus.keys())
    exam_type = random.choice(syllabus_types)
    system_options = Syllabus[exam_type]
    system_station = random.choice(list(system_options.keys()))
    diagnosis_list = system_options[system_station]
    diagnosis = random.choice(diagnosis_list)
    
    st.session_state.clinical_case = {
        "Exam Type": exam_type,
        "System/Station": system_station,
        "Diagnosis": diagnosis,
        "Stage": "PATIENT_SIM",
    }
    st.session_state.messages = []
    st.session_state.examiner_review = None

# --- 6. SESSION STATE INITIALIZATION ---
if 'clinical_case' not in st.session_state:
    load_new_case()

# --- 7. SIDEBAR UI (Professional & Thematic Dashboard) ---
with st.sidebar:
    # Stethoscope animated circular emblem instead of broken image
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem; margin-bottom: 1.5rem;">
            <div style="
                background: linear-gradient(135deg, rgba(255, 153, 51, 0.15), rgba(19, 136, 8, 0.15));
                border: 2px solid rgba(247, 148, 29, 0.5);
                border-radius: 50%;
                width: 90px;
                height: 90px;
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0 0 25px rgba(247, 148, 29, 0.25);
                animation: pulse 2s infinite alternate;
            ">
                <span style="font-size: 2.6rem;">🩺</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Dynamic Simulation Stage Badge
    stage = st.session_state.clinical_case["Stage"]
    if stage == "PATIENT_SIM":
        st.markdown('<div class="status-badge-sim">💬 PATIENT INTERVIEW ACTIVE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge-review">🎓 EXAMINER REVIEW ACTIVE</div>', unsafe_allow_html=True)

    # Custom Cards for Metadata
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
        unsafe_allow_html=True
    )

    # Interview metrics card (interactive progress metrics!)
    q_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    # Calculate progress % (say target is 7 questions for a good history)
    progress_pct = min(100, int((q_count / 7) * 100))
    progress_color = "#2ed573" if progress_pct >= 70 else "#f7941d"
    
    st.markdown(
        f"""
        <div class="custom-card">
            <div class="card-header">History Metrics</div>
            <div class="card-value" style="display:flex; justify-content:space-between; align-items:center;">
                <span>Questions:</span>
                <span style="color: {progress_color}; font-weight:700;">{q_count}</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: {progress_pct}%; background: {progress_color};"></div>
            </div>
            <div style="font-size:0.75rem; color:#888; margin-top:0.45rem; line-height:1.25;">
                { "💡 Ready to present your case? Type 'done'." if q_count >= 5 else "💡 Ask at least 5 questions to gather a comprehensive history." }
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    if st.button("🔄 Next Random Case"):
        load_new_case()
        st.rerun()

# --- 8. MAIN UI CONTENT ---
# Header with Dynamic Title
st.markdown('<div class="main-title">LK Final MBBS</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Clinical Case Simulator</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="desc-card">
        <div class="desc-text">
            🇱🇰 මෙමගින් ශ්‍රී ලංකාවේ රජයේ රෝහලක සිටින රෝගියෙකු ප්‍රතිනිර්මාණය කරයි. 
            ප්‍රශ්න අසා නිවැරදි ඉතිහාසය (History) ලබාගන්න. 
            අවසානයේදී විභාග පරීක්ෂක මණ්ඩලයට මුහුණ දීමට <b>done</b> ලෙස ටයිප් කරන්න.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 9. CHAT INTERFACE & LOGIC ---
current_diagnosis = st.session_state.clinical_case["Diagnosis"]

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    sender = message.get("sender")
    with st.chat_message(role):
        if sender == "Patient":
            st.markdown(
                """
                <div style='color:#a6b0c3; font-size:0.85rem; font-weight:700; margin-bottom:0.4rem; letter-spacing:0.5px;'>
                    🩺 PATIENT (රෝගියා)
                </div>
                """, 
                unsafe_allow_html=True
            )
        elif sender == "Examiner":
            st.markdown(
                """
                <div style='color:#f7941d; font-size:0.85rem; font-weight:700; margin-bottom:0.4rem; letter-spacing:0.5px;'>
                    🎓 EXTERNAL EXAMINER (විභාග පරීක්ෂක)
                </div>
                """, 
                unsafe_allow_html=True
            )
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("ප්‍රශ්නයක් අසන්න, නැතහොත් done ලෙස ටයිප් කරන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if prompt.lower().strip() == "done" and st.session_state.clinical_case["Stage"] != "EXAMINER_REVIEW":
        st.session_state.clinical_case["Stage"] = "EXAMINER_REVIEW"
        # Only collect STUDENT questions (user role only), ignoring patient replies
        student_questions = [m['content'] for m in st.session_state.messages if m['role'] == 'user' and m['content'].lower().strip() != 'done']

        if not student_questions:
            st.warning("⚠️ You haven't asked the patient any questions yet! Please take a proper history before requesting an evaluation.")
            st.session_state.clinical_case["Stage"] = "PATIENT_SIM"
            st.rerun()

        with st.spinner("🎓 Examiner is reviewing your performance..."):
            # Build history as a numbered list of student questions only
            history_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(student_questions)])
            
            examiner_instruction = (
                f"You are a Senior Consultant Physician and External Examiner for the University Final MBBS Clinical Examination in Sri Lanka. "
                f"The student just finished taking a history for a patient who actually has: '{current_diagnosis}'. "
                f"Below is the list of ONLY the questions the student asked during history-taking (the patient's replies are NOT shown). "
                f"Based solely on what the student chose to ask, evaluate their clinical history-taking performance in English. "
                f"Assess which components of the history they covered (Presenting Complaint, HPC, PMH, Drug/Allergy history, Social/Family history) and which they missed. "
                f"Point out specific clinical questions they should have asked for '{current_diagnosis}' but did not. "
                f"Be constructively strict, mimicking a real Sri Lankan professor. Then ask them to declare their primary Differential Diagnoses, "
                f"and clearly state what physical signs they would expect to elicit on bedside clinical examination."
            )
            
            try:
                # Wrap as a proper Content object so the API always gets a valid non-empty turn
                examiner_contents = [
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(
                            text=f"Here are the questions I asked the patient during history-taking:\n\n{history_text}\n\nPlease evaluate my performance."
                        )]
                    )
                ]
                response = client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=examiner_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=examiner_instruction,
                        temperature=0.5
                    )
                )
                examiner_response = response.text
                st.session_state.examiner_review = examiner_response
                st.session_state.messages.append({"role": "assistant", "content": examiner_response, "sender": "Examiner"})
            except Exception as e:
                st.error(f"Error during examiner generation: {e}")
        st.rerun()

    elif st.session_state.clinical_case["Stage"] == "PATIENT_SIM":
        # Get patient response
        with st.spinner("🩺 Patient is responding..."):
            patient_instruction = (
                f"You are a Sri Lankan hospital patient admitted to a Teaching Hospital ward. "
                f"You have been diagnosed by the consultants with '{current_diagnosis}' "
                f"under the category '{st.session_state.clinical_case['Exam Type']}' and system '{st.session_state.clinical_case['System/Station']}'.\n\n"
                f"[CRITICAL RULE]: You must NEVER reveal this exact medical diagnosis or clinical jargon to the student.\n\n"
                f"[DYNAMIC SYMPTOMS GENERATION]:\n"
                f"Based on the assigned condition ({current_diagnosis}), you must dynamically imagine and adapt your symptoms "
                f"to perfectly match how a real-world patient with this exact disease would present in a ward. Translate clinical concepts into layperson complaints.\n\n"
                f"[STRICT LANGUAGE & TONE RULE]:\n"
                f"1. You must respond ONLY in Sinhala characters (සිංහල අකුරෙන්). Do not write in English or Singlish characters.\n"
                f"2. Talk like a realistic local Sri Lankan patient (colloquial ward language). Use terms like 'බඩ රිදෙනවා', 'අතපය පණ නැති වුණා', 'කැස්ස', 'මහන්සියි', 'පොත/ක්ලිනික් කාඩ් එක'.\n"
                f"3. When the student asks an open-ended question at the beginning (e.g., 'මොකද අමාරුව?' or 'What brought you here?'), give a natural, layperson-style main complaint that fits '{current_diagnosis}' using Sinhala script.\n"
                f"4. Keep answers short. Only give deeper details (family history, compliance, social background) if she directly asks for them."
            )
            
            # Format conversational contents history for client.models.generate_content
            formatted_contents = []
            for msg in st.session_state.messages:
                role_type = "user" if msg["role"] == "user" else "model"
                formatted_contents.append(
                    types.Content(role=role_type, parts=[types.Part.from_text(text=msg["content"])])
                )
            
            try:
                response = client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=patient_instruction,
                        temperature=0.4
                    )
                )
                patient_response = response.text
                st.session_state.messages.append({"role": "assistant", "content": patient_response, "sender": "Patient"})
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ රෝගියා මඳක් වෙහෙසට පත්ව ඇත (API Rate Limit). තත්පර 10ක් සිට නැවත ප්‍රශ්නය අසන්න.")
                else:
                    st.error(f"Error during patient generation: {e}")
        st.rerun()

    elif st.session_state.clinical_case["Stage"] == "EXAMINER_REVIEW":
        # Get examiner response to student's answer/viva!
        with st.spinner("🎓 Examiner is responding..."):
            examiner_instruction = (
                f"You are a Senior Consultant Physician and External Examiner for the University Final MBBS Clinical Examination in Sri Lanka. "
                f"The case diagnosis is '{current_diagnosis}'. "
                f"You have already provided your initial critique evaluation. The student is now answering your viva questions "
                f"(differential diagnoses, expected physical signs on bed-side examination, etc.) or asking follow-up questions. "
                f"Read the student's response. Respond strictly as the consultant examiner, evaluating their differentials and clinical reasoning. "
                f"Ask further questions if needed, or provide final grade/feedback. Keep your tone constructively strict and academic."
            )
            
            # Format conversational contents history for client.models.generate_content
            formatted_contents = []
            for msg in st.session_state.messages:
                role_type = "user" if msg["role"] == "user" else "model"
                formatted_contents.append(
                    types.Content(role=role_type, parts=[types.Part.from_text(text=msg["content"])])
                )
                
            try:
                response = client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=examiner_instruction,
                        temperature=0.5
                    )
                )
                examiner_response = response.text
                st.session_state.messages.append({"role": "assistant", "content": examiner_response, "sender": "Examiner"})
            except Exception as e:
                st.error(f"Error during examiner review: {e}")
        st.rerun()