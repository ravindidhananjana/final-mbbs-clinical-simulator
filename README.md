# 🇱🇰 Sri Lankan Final MBBS Clinical Case Simulator

An interactive AI-powered clinical case simulator built specifically for Sri Lankan medical students preparing for their **Final MBBS Clinical Examinations** (Long Cases and Short Cases).

The simulator uses **Streamlit** for the UI and the **Google GenAI SDK** (Gemini) to dynamically model patient scenarios and senior examiner assessments — grounded in local Sri Lankan ward settings and the undergraduate clinical syllabus.

---

## 🚀 Features

### 📚 Syllabus-Aligned Case Directory
Randomly selects cases from **8 exam categories** spanning the full Final MBBS clinical syllabus:

| Category | Systems Covered |
|---|---|
| Medicine Long Cases | CVS, RS, GIT, GUT, Nervous & MS, Endocrine, Systemic, Haematological, Infections |
| Medicine Short Cases | CVS, RS, GIT, Abdomen, GUT, Nervous & MS, Endocrine, Haematological |
| Surgery Long Cases | Vascular, Head & Neck, Chest & Breast, GIT, GUT, Orthopaedics |
| Surgery Short Cases | Vascular, Head & Neck, Chest & Breast, GIT, GUT, Orthopaedics, Miscellaneous |
| Paediatric Long Cases | CVS, RS, Endocrine, Haematological, GIT, Systemic, GUT, Nervous & MS, Infectious |
| Paediatric Short Cases | CVS, RS, CNS & MS, Haematological, Abdomen, GUT, Skin, Other |
| Gynecology Cases | Benign & Malignant Gynecology, Infertility, Prolapse, Endocrine, Infections |
| Obstetrics Cases | Antenatal, Postnatal, Intrapartum, High-risk Obstetrics |

> **The diagnosis is always hidden from the student** — only the Exam Type and System/Station are shown in the sidebar, mimicking a real MBBS clinical examination.

---

### 🤖 Dual-Phase AI Simulation Engine

#### Phase 1 — Patient Simulation (`PATIENT_SIM`)
- The AI plays a patient admitted to a local Sri Lankan Teaching Hospital ward.
- Responds **strictly in Sinhala script** using authentic colloquial ward language  
  (e.g., *"බඩ රිදෙනවා"*, *"හුස්ම ගන්න අමාරුයි"*, *"ක්ලිනික් කාඩ් එක ගෙනාවා"*).
- Adapts all symptom responses to fit the assigned hidden diagnosis.
- Maintains **full conversational context** across the entire history-taking session.

#### Phase 2 — Examiner Review (`EXAMINER_REVIEW`)
- Triggered by typing **`done`** in the chat input.
- The AI transforms into a **Senior Consultant Physician & University External Examiner**.
- Evaluates **only the questions the student asked** (patient replies are hidden from the evaluator) — so the report reflects the student's own clinical reasoning, not the patient's story.
- Provides a structured English-language critique covering:
  - Presenting Complaint (PC) coverage
  - History of Presenting Complaint (HPC) depth
  - Past Medical / Drug / Allergy / Social / Family history gaps
  - **Clinical omissions** specific to the hidden diagnosis
  - Prompts for **Differential Diagnoses**
  - Expected **physical signs** on bedside examination
- After the initial report, continues as an **interactive viva** — the examiner responds to each of the student's answers and probes further.

#### Guard Rails
- If the student types `done` without asking any questions first, they receive a warning and are returned to the patient interview.

---

### 📊 History Metrics Card (Sidebar)
- Live counter of questions asked during the session.
- Animated colour-coded progress bar (🟠 orange → 🟢 green) that turns green once ≥ 5 questions have been asked.
- Hint prompt reminding the student to type `done` when ready.

---

### 🎨 UI / UX
- Dark glassmorphic theme with orange-and-green Sri Lankan colour accents.
- *Plus Jakarta Sans* Google Font typography.
- Animated pulsing stethoscope emblem in the sidebar.
- Chat messages clearly labelled by speaker role:
  - 🩺 **PATIENT (රෝගියා)**
  - 🎓 **EXTERNAL EXAMINER (විභාග පරීක්ෂක)**
- **Next Random Case** button cycles across all 8 exam categories.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Framework | [Streamlit](https://streamlit.io/) |
| AI Model | `gemini-3.1-flash-lite` via [Google GenAI SDK](https://github.com/googleapis/python-genai) |
| Language | Python 3.9+ |
| Styling | Vanilla CSS (glassmorphism, animations) |

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd cases
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create `.streamlit/secrets.toml` (already listed in `.gitignore`):
```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

> [!NOTE]
> Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).

### 4. Run the App
```bash
streamlit run app.py
```
App opens at `http://localhost:8501`.

---

## 📂 Project Structure

```text
cases/
├── .streamlit/
│   └── secrets.toml      # Local secrets — API key (git-ignored)
├── .gitignore
├── app.py                # Main Streamlit app — all simulation logic
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 📝 How to Use

1. Open `http://localhost:8501` in your browser.
2. The **Exam Type** and **System/Station** are shown in the sidebar. The diagnosis is hidden.
3. Ask history-taking questions in **Sinhala** (e.g., *"කෑස්ස කොපමණ කලක් ඉඳල ද?"*, *"රාත්‍රියේ දහඩිය දේ ද?"*).
4. Watch the **History Metrics** bar — aim for at least 5 comprehensive questions.
5. When ready, type **`done`** and press Enter to call the examiner.
6. Read the **Examiner Report**, then answer the viva questions interactively.
7. Click **🔄 Next Random Case** in the sidebar to start a fresh simulation.

---

## ⚠️ Known Limitations

- The simulator evaluates history-taking only — physical examination and investigation interpretation are not currently simulated.
- Responses are in Sinhala script. Students using other regional languages will need to adapt their input.
- API availability depends on Google GenAI service uptime.
