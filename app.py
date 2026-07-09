import os
import base64
import json
import PyPDF2
from PIL import Image
from groq import Groq
import pytesseract
from io import BytesIO
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load environment variables from .env file
load_dotenv()

class MedicalReportAnalyzer:
    def __init__(self, groq_api_key=None):
        """Initialize the medical report analyzer with Groq API key"""
        api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if api_key:
            api_key = api_key.strip("'\"")
        
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Please check your .env file.")
        
        # Store the API key for later use
        self.api_key = api_key
        
        try:
            self.client = Groq(api_key=api_key)
            self.api_configured = True
        except Exception as e:
            self.client = None
            self.api_configured = False
            self.api_error = str(e)
        
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file"""
        try:
            # Reset file pointer to beginning
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip() if text.strip() else "No text could be extracted from the PDF"
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"
    
    def extract_text_from_image(self, image_file):
        """Extract text from image using OCR"""
        try:
            # Reset file pointer to beginning
            image_file.seek(0)
            
            # Open image with PIL
            image = Image.open(image_file)
            
            # Convert to RGB if necessary (for better OCR results)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform OCR
            text = pytesseract.image_to_string(image, config='--psm 6')
            
            return text.strip() if text.strip() else "No text could be extracted from the image"
        except Exception as e:
            return f"Error extracting image text: {str(e)}. Make sure Tesseract is installed."
    
    def analyze_medical_report(self, report_text):
        """Analyze medical report using Groq API in JSON mode"""
        
        if not self.api_configured:
            return json.dumps({"error": f"API Error: {self.api_error}. Please configure your Groq API key."})
        
        system_prompt = """
        You are an expert medical AI assistant that analyzes medical reports and provides structured JSON data.
        Your task is to analyze the medical report and return a JSON object with the following fields:
        
        1. "problems": A list of health problems or conditions found. Each problem must be an object with:
           - "name": Simple, understandable name (e.g. "High Blood Sugar" instead of "Hyperglycemia").
           - "what_is_it": A clear explanation in everyday language of what this condition means, using simple analogies if helpful.
           - "body_effect": A step-by-step description of what this does inside the body and what parts it affects.
           - "causes": Common reasons why this happens (lifestyle, age, genetics, etc.).
           - "numbers_meaning": Interpretation of the test numbers, comparing their value to the normal range, explained simply.
           - "severity": Rating of this specific condition as "Normal", "Mild", "Moderate", or "Severe".
           - "is_serious": Summary of risks if left untreated.
           
        2. "connections": A simple explanation of how the found problems are connected or how one might relate to another.
        
        3. "overall_severity": An object containing:
           - "level": The overall severity classification ("Normal", "Mild", "Moderate", or "Severe").
           - "explanation": In simple terms, what this severity means (e.g. like a dashboard warning light).
           
        4. "doctor": An object containing:
           - "specialist": The type of doctor to consult.
           - "reason": Why this specialist is appropriate.
           - "timeline": How soon to see them ("Urgent", "Soon", or "Routine").
           
        5. "diet": An object containing:
           - "helpful_foods": A list of objects, each with "food" (name) and "reason" (why it helps).
           - "avoid_foods": A list of objects, each with "food" (name) and "reason" (why it hurts).
           - "tips": List of simple, practical eating tips.
           
        6. "lifestyle": An object containing:
           - "immediate_actions": List of things to do right away.
           - "daily_changes": List of daily life adjustments.
           - "precautions": List of activities to be careful with or avoid.
           
        7. "treatment": List of strings explaining potential treatment approaches and what to expect.
        
        8. "follow_up": List of strings explaining monitoring and follow-up timeline.
        
        9. "disclaimer": Standard medical disclaimer clarifying that this is informational and they must consult a real doctor.

        CRITICAL: You must return ONLY a raw JSON object. Do not wrap it in markdown formatting or add any leading/trailing text. Ensure the JSON is valid and parses correctly.
        """
        
        user_prompt = f"""
        Please analyze this medical report with EXTREME DETAIL about the medical problems identified. I want very comprehensive explanations about the conditions found.

        MEDICAL REPORT TEXT:
        {report_text}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
                max_tokens=8000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return json.dumps({"error": f"Error analyzing report: {str(e)}"})
    
    def process_file(self, file, file_type):
        """Process uploaded file and return analysis"""
        
        # Extract text based on file type
        if file_type == "pdf":
            extracted_text = self.extract_text_from_pdf(file)
        elif file_type in ["jpg", "jpeg", "png", "tiff", "bmp"]:
            extracted_text = self.extract_text_from_image(file)
        else:
            return "Unsupported file type. Please upload PDF or image files."
        
        if extracted_text.startswith("Error"):
            return extracted_text
        
        if not extracted_text or extracted_text.strip() == "":
            return "No text could be extracted from the file. Please ensure the file contains readable text."
        
        # Analyze the extracted text
        analysis = self.analyze_medical_report(extracted_text)
        
        return {
            "extracted_text": extracted_text,
            "analysis": analysis
        }


# Flask Application Setup
app = Flask(__name__, static_folder="static", template_folder="templates")
analyzer = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    global analyzer
    if not analyzer:
        try:
            analyzer = MedicalReportAnalyzer()
        except Exception as e:
            return jsonify({"error": f"Analyzer config error: {str(e)}"}), 500

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
        
    file_type = file.filename.split('.')[-1].lower()
    if file_type not in ["pdf", "jpg", "jpeg", "png", "tiff", "bmp"]:
        return jsonify({"error": "Unsupported file format. Please upload PDF or images."}), 400
        
    try:
        # Read file into memory buffer
        file_bytes = BytesIO(file.read())
        
        result = analyzer.process_file(file_bytes, file_type)
        
        if isinstance(result, str):
            return jsonify({"error": result}), 500
            
        # Parse analysis JSON string
        try:
            analysis_json = json.loads(result["analysis"])
        except Exception as json_err:
            analysis_json = {
                "error": "Failed to parse AI response as JSON",
                "raw_text": result["analysis"]
            }
            
        return jsonify({
            "extracted_text": result["extracted_text"],
            "analysis": analysis_json
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Command Line Interface
class CLIMedicalAnalyzer:
    def __init__(self):
        print("🏥 Medical Report Analyzer CLI")
        print("=" * 40)
        
        # Get API key from .env file
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            api_key = input("Enter your Groq API key: ").strip()
        
        try:
            self.analyzer = MedicalReportAnalyzer(groq_api_key=api_key)
            if self.analyzer.api_configured:
                print("✅ API key configured successfully!")
            else:
                print(f"❌ Configuration Error: {self.analyzer.api_error}")
                self.analyzer = None
        except Exception as e:
            print(f"❌ Initialization Error: {str(e)}")
            self.analyzer = None
    
    def run(self):
        """Run the CLI version"""
        if not self.analyzer:
            return
        
        while True:
            print("\nOptions:")
            print("1. Analyze PDF report")
            print("2. Analyze image report")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                self.analyze_pdf()
            elif choice == '2':
                self.analyze_image()
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def analyze_pdf(self):
        file_path = input("Enter PDF file path: ").strip()
        try:
            with open(file_path, 'rb') as file:
                result = self.analyzer.process_file(file, 'pdf')
                self.display_result(result, file_path)
        except FileNotFoundError:
            print("❌ File not found!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def analyze_image(self):
        file_path = input("Enter image file path: ").strip()
        try:
            with open(file_path, 'rb') as file:
                file_ext = file_path.split('.')[-1].lower()
                result = self.analyzer.process_file(file, file_ext)
                self.display_result(result, file_path)
        except FileNotFoundError:
            print("❌ File not found!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def display_result(self, result, file_path):
        if isinstance(result, dict):
            print(f"\n📄 Analysis for: {file_path}")
            print("=" * 50)
            
            # Print parsed JSON details in a nice readable text format
            try:
                data = json.loads(result["analysis"])
                print(f"\n[OVERALL SEVERITY: {data.get('overall_severity', {}).get('level', 'N/A')}]")
                print(f"Explanation: {data.get('overall_severity', {}).get('explanation', 'N/A')}")
                
                print("\nHEALTH PROBLEMS FOUND:")
                for i, prob in enumerate(data.get("problems", [])):
                    print(f"\n  Problem {i+1}: {prob.get('name')}")
                    print(f"    - What is it: {prob.get('what_is_it')}")
                    print(f"    - Body effect: {prob.get('body_effect')}")
                    print(f"    - Causes: {prob.get('causes')}")
                    print(f"    - Numbers interpretation: {prob.get('numbers_meaning')}")
                    print(f"    - Specific severity: {prob.get('severity')}")
                    
                print(f"\nCONNECTIONS:\n  {data.get('connections')}")
                
                doc = data.get('doctor', {})
                print(f"\nRECOMMENDED SPECIALIST:\n  Consult {doc.get('specialist')} ({doc.get('timeline')}ly) - Reason: {doc.get('reason')}")
                
            except Exception:
                print(result["analysis"])
            
            save = input("\n💾 Save analysis to file? (y/n): ").lower()
            if save == 'y':
                output_file = f"analysis_{os.path.basename(file_path)}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"MEDICAL REPORT ANALYSIS\n{'='*50}\n\n{result['analysis']}")
                print(f"✅ Analysis saved to: {output_file}")
        else:
            print(f"❌ {result}")


if __name__ == "__main__":
    import sys
    
    # Initialize analyzer for backend
    try:
        analyzer = MedicalReportAnalyzer()
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli = CLIMedicalAnalyzer()
        cli.run()
    else:
        # Run Flask web app
        port = int(os.getenv("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=True)