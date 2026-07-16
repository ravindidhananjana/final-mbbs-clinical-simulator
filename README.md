# 🇱🇰 Sri Lankan Final MBBS Clinical Case Simulator

An interactive AI-powered clinical case simulator built specifically for Sri Lankan medical students preparing for their **Final MBBS Clinical Examinations** (Long Cases and Short Cases).

The simulator uses **Streamlit** for the UI and the **Google GenAI SDK** (`gemini-3.1-flash-lite`) to dynamically model patient scenarios and senior examiner assessments — grounded in local Sri Lankan ward settings and the undergraduate clinical syllabus.

---

## 🚀 Key Features

### 🎙️ Hands-Free Voice-to-Text Input (New!)
- **Native Browser Integration:** Uses the browser's native Web Speech API embedded directly inside the chat input box.
- **Multilingual Recognition:** Speak in **Sinhala**, **Singlish**, or **English**. The browser instantly transcribes your speech.
- **Auto-Submit:** When you finish speaking, the simulator automatically submits your question to the patient. No need to click "Send" or press Enter!
- **Blazing Fast Text Responses:** The AI patient responds immediately in text format (no slow audio-generation overhead).

### 🗣️ Multilingual Patient Engine
The patient dynamically mirrors your language based on your input:
- Speak/type in **Sinhala script** (e.g., *"මොකද අමාරුව?"*) → Patient replies in colloquial Sinhala script.
- Speak/type in **Singlish** (e.g., *"mokada amaruwa?"*) → Patient replies in natural Singlish.
- Speak/type in **English** → Patient replies in English with a realistic Sri Lankan persona.

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

## 🤖 Dual-Phase AI Simulation Engine

#### Phase 1 — Patient Simulation (`PATIENT_SIM`)
- The AI plays a patient admitted to a local Sri Lankan Teaching Hospital ward.
- Adapts all symptom responses to fit the assigned hidden diagnosis without ever revealing the medical terminology.
- Maintains **full conversational context** across the entire history-taking session.

#### Phase 2 — Examiner Review (`EXAMINER_REVIEW`)
- Triggered by typing **`done`** in the chat input.
- Evaluates **only the questions the student asked** (patient replies are hidden from the evaluator) to accurately assess clinical reasoning.
- Provides a structured English-language critique covering:
  - Presenting Complaint (PC) & History of Presenting Complaint (HPC) depth.
  - Past Medical / Drug / Social history gaps.
  - **Clinical omissions** specific to the hidden diagnosis.
  - Prompts for **Differential Diagnoses** and expected **physical signs**.
- Continues as an **interactive viva** — the examiner responds to the student's answers and probes further.

---

## 🎨 UI / UX
- Dark glassmorphic theme with orange-and-green Sri Lankan colour accents.
- *Plus Jakarta Sans* Google Font typography.
- Animated pulsing stethoscope emblem in the sidebar.
- Integrated, sleek microphone button for voice input natively inside the text box.
- History Metrics Card tracks progress and ensures you ask at least 5 questions before submitting to the examiner.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Framework | [Streamlit](https://streamlit.io/) >= 1.31 |
| AI Model | `gemini-3.1-flash-lite` via `google-genai` SDK |
| Voice Input| Web Speech API (`webkitSpeechRecognition`) injected via JS |
| Styling | Vanilla CSS (glassmorphism, animations) |

*(Note: `gTTS` and audio-playback dependencies have been completely removed to prioritize speed and stability).*

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

### 4. Run the App
```bash
streamlit run app.py
```
App opens at `http://localhost:8501`.

---

## 📝 How to Use

1. Open `http://localhost:8501` in your browser.
2. The **Exam Type** and **System/Station** are shown in the sidebar. The diagnosis is hidden.
3. **Click the Microphone** in the chat bar and speak your question in Sinhala/Singlish/English. The app will auto-transcribe and submit it instantly. Alternatively, you can type your questions.
4. Watch the **History Metrics** bar — aim for at least 5 comprehensive questions.
5. When ready, type **`done`** and press Enter to call the examiner.
6. Read the **Examiner Report**, then answer the viva questions interactively.
7. Click **🔄 Next Random Case** in the sidebar to start a fresh simulation.
