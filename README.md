
# 🏥 Medical Report Summarizer

**AI-Powered Health Report Analyzer – Extract, Analyze, and Understand Your Medical Reports in Seconds.**

---

## 🔬 About the Project

The **Medical Report Summarizer** is an intelligent tool designed to:
- 📄 Extract text from **PDF** or **image-based** medical reports using OCR.
- 🧠 Analyze the text using **Groq's LLM (LLaMA 3.3 70B)** to:
  - Identify medical problems
  - Rate severity
  - Recommend specialists
  - Suggest diet & lifestyle changes
  - Provide treatment overviews
  - Suggest follow-up actions

The application provides both a **Streamlit web interface** and a **Command Line Interface (CLI)**.

---

## ⚙️ Features

- 📑 **PDF & Image support**
- 🧠 **Medical insights via Groq API**
- 🧾 **Detailed analysis with human-readable explanations**
- 🔍 **OCR for scanned reports using Tesseract**
- 🧪 **Test result interpretation**
- 💾 **Downloadable analysis reports**
- 👨‍💻 **Web UI + CLI support**

---

## 📷 Demo

![App Screenshot](https://user-images.githubusercontent.com/your-username/demo-screenshot.png)  
> Upload → Analyze → Understand

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- Tesseract OCR installed and in your system's PATH  
  - [Download Tesseract](https://github.com/tesseract-ocr/tesseract)

### 🔑 API Setup

1. Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ **Do NOT share or commit your `.env` file.**

---

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/siddhartha-45/MedicalReport_Summarizer.git
cd MedicalReport_Summarizer

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🖥️ Usage

### ✅ Run Web App (Streamlit)

```bash
streamlit run app.py
```

Then open: `http://localhost:8501` in your browser.

---

### 💻 Run CLI Version

```bash
python app.py --cli
```

---

## 📂 Supported File Types

- PDF (`.pdf`)
- Images (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`)

---

## 📁 Project Structure

```
MedicalReport_Summarizer/
│
├── app.py                # Main application (Web + CLI)
├── .env                  # API key (not pushed to GitHub)
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── ...
```

---

## 🧪 Sample Output

```
## 🔍 WHAT'S WRONG WITH YOUR HEALTH?
Problem 1: High Blood Sugar
- What is this? ...
- How does this affect your body? ...
...

## ⚠️ HOW SERIOUS IS THIS?
Level: Moderate
...

## 📅 FOLLOW-UP - WHAT HAPPENS NEXT
- Recheck in 2 weeks
- Consult endocrinologist
```

---

## 🔐 Security & Disclaimer

- Your data is processed locally and via secure API.
- **No data is stored or logged**.
- This tool **does not replace** professional medical advice.
- Always consult a qualified doctor for health decisions.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📃 License

[MIT License](LICENSE)

---

## 🙏 Acknowledgements

- [Groq API](https://groq.com/)
- [Streamlit](https://streamlit.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [OpenAI](https://openai.com/)
- [LLaMA 3](https://llama.meta.com/)

---

## 📫 Contact

**Siddhartha Chitikela**  
📧 [Email Me](mailto:chjvsidddhartha45@gmail.com)  
🌐 [LinkedIn](https://linkedin.com/in/chjvsidddhartha1545)

---
