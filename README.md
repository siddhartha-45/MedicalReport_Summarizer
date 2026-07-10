# 🏥 Medical Report Summarizer

**AI-Powered Health Report Analyzer – Extract, Analyze, and Understand Your Medical Reports in Seconds.**

---

## 🔬 About the Project

The **Medical Report Summarizer** is an intelligent tool designed to bridge the gap between complex medical reports and patient understanding. It allows users to upload a PDF or an image-based health report and translates it into easy-to-understand terms.

Powered by **Groq's LLaMA 3.3 70B** model, the system performs a thorough analysis of clinical metrics and provides detailed explanations, specialist consultations, and lifestyle recommendations. 

The application offers both a **modern Flask-based Web Dashboard** (complete with dark/light mode and support for 9 languages) and a developer-friendly **Command Line Interface (CLI)**.

> [!IMPORTANT]
> **Disclaimer:** This tool is for educational and informational purposes only. It is not a replacement for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

---

## ⚙️ Features

- 📄 **Multiformat Support:** Analyze both digital and scanned files (PDF, PNG, JPG, JPEG, TIFF, BMP).
- 🔍 **OCR Engine:** Scans image-based reports using Tesseract OCR.
- 🛡️ **Medical Document Validation:** Automatically detects and rejects non-medical documents (e.g., bills, receipts, code, or random text).
- 🌐 **Multilingual Analysis:** Receive explanations and advice in 9 languages (English, Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati).
- 📊 **Clinical Analysis Dashboard:**
  - **Health Problems Found:** Explains conditions in simple terms with everyday analogies, causes, and numeric result interpretations.
  - **Condition Connections:** Details how different issues or metrics are related.
  - **Specialist Consultation:** Advises which practitioner to see and how urgently (Urgent, Soon, Routine).
  - **Diet & Nutrition:** Lists custom foods to include, foods to avoid, and general tips.
  - **Habits & Lifestyle:** Summarizes immediate actions, daily changes, and lifestyle precautions.
  - **Care & Timeline:** Outlines treatment expectations and follow-up monitoring.
- 💾 **Export Options:** Print or save a PDF summary, or download the raw JSON analysis data.
- 🎨 **Modern Glassmorphic UI:** Smooth, responsive interface with customized light/dark modes and glowing visual elements.
- 💻 **CLI Support:** Run full scans and view structured medical reports directly in the terminal.

---

## 🚀 Getting Started

### 🔧 Prerequisites

- **Python 3.8+**
- **Tesseract OCR** installed on your system.
  - **Windows:** Download the installer from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and ensure you add the install path (e.g., `C:\Program Files\Tesseract-OCR`) to your System's `PATH` environment variable.
  - **macOS:** Install via Homebrew: `brew install tesseract`
  - **Linux:** Install via apt: `sudo apt install tesseract-ocr`

### 🔑 API Setup

1. Get a free API key from the [Groq Console](https://console.groq.com/).
2. Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

> [!WARNING]
> Do NOT share or commit your `.env` file to public version control systems.

---

### 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/siddhartha-45/MedicalReport_Summarizer.git
   cd MedicalReport_Summarizer
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Usage

### 🌐 Run Web App (Flask)

Start the local Flask development server:
```bash
python app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser to access the interactive web interface.

---

### 💻 Run CLI Version

To run the program inside your terminal:
```bash
python app.py --cli
```
Follow the interactive prompts to load PDF/image paths, display analysis, and optionally save the results as a text file.

---

## 📁 Project Structure

```
MedicalReport_Summarizer/
│
├── app.py                # Main application entry point (Flask Web App & CLI)
├── requirements.txt      # Python package dependencies
├── .env                  # Environment configuration (not committed)
├── templates/
│   └── index.html        # Web app dashboard template
├── static/
│   ├── style.css         # Modern Glassmorphic CSS design system
│   └── main.js           # Frontend logic (file uploading, language select, tabs)
└── README.md             # This documentation file
```

---

## 🧪 Sample Output (CLI)

```
🏥 Medical Report Analyzer CLI
========================================
[OVERALL SEVERITY: MODERATE]
Explanation: Some lab indicators are outside their normal boundaries.

HEALTH PROBLEMS FOUND:

  Problem 1: High Blood Sugar
    - What is this: Elevated glucose levels in the bloodstream.
    - Body effect: Affects energy storage, makes kidneys work harder.
    - Causes: Lifestyle, diet, genetics.
    - Numbers interpretation: 140 mg/dL (Normal is < 100 mg/dL).
    - Specific severity: Moderate

CONNECTIONS:
  High blood sugar and slight blood pressure elevation are co-related metabolic indicators.

RECOMMENDED SPECIALIST:
  Consult Endocrinologist (Soon) - Reason: For detailed glycemic control and guidance.
```

---

## 🔒 Security & Privacy

- **Local File Processing:** Documents are processed in-memory. They are not stored on any remote server.
- **Secure Transmission:** The text payload is securely transmitted to Groq's API and is processed according to their privacy guidelines.
- **No logs or databases:** The application does not persist any patient data locally or in any database.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📃 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more details.

---

## 🙏 Acknowledgements

- [Groq API](https://groq.com/) — Fast inference engine powered by LPU
- [Meta LLaMA 3.3](https://llama.meta.com/) — Core LLM analysis model
- [Flask](https://flask.palletsprojects.com/) — Web framework
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — Optical Character Recognition
- [PyPDF2](https://github.com/py-pdf/pypdf) — PDF parsing library

---

## 📫 Contact

**Siddhartha Chitikela**  
📧 [Email Me](mailto:chjvsidddhartha45@gmail.com)  
🌐 [LinkedIn](https://linkedin.com/in/chjvsidddhartha1545)
