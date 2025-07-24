import os
import base64
import json
import PyPDF2
from PIL import Image
from groq import Groq
import pytesseract
from io import BytesIO
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MedicalReportAnalyzer:
    def __init__(self, groq_api_key=None):
        """Initialize the medical report analyzer with Groq API key"""
        # Get API key from .env file
        api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        
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
        """Analyze medical report using Groq API"""
        
        if not self.api_configured:
            return f"API Error: {self.api_error}. Please configure your Groq API key."
        
        system_prompt = """
        You are an expert medical AI assistant that analyzes medical reports and provides comprehensive health insights. 
        Your task is to analyze the medical report and provide:

        1. **Problem Identification**: Clearly explain what health issues or conditions are identified
        2. **Severity Assessment**: Rate as Normal/Mild/Moderate/Severe with reasoning
        3. **Doctor Consultation**: Recommend which type of specialist to consult
        4. **Dietary Recommendations**: Suggest specific foods to include/avoid
        5. **Precautions & Lifestyle**: List important precautions and lifestyle changes
        6. **Treatment Overview**: Explain potential treatment approaches
        7. **Follow-up**: Recommend monitoring and follow-up schedule

        Important: 
        - Always include medical disclaimers
        - Be clear about when immediate medical attention is needed
        - Provide evidence-based recommendations
        - Use simple, understandable language
        - Structure your response clearly with headings
        """
        
        user_prompt = f"""
        Please analyze this medical report with EXTREME DETAIL about the medical problems identified. I want very comprehensive explanations about the conditions found, but keep other sections standard length.

        MEDICAL REPORT TEXT:
        {report_text}

        Please provide your analysis in the following format:

        ## 🔍 WHAT'S WRONG WITH YOUR HEALTH? (DETAILED EXPLANATION)

        
        ### **HEALTH PROBLEMS FOUND:**

        [For each condition/abnormality, explain:]

        **Problem 1: [Name in simple terms, e.g., "High Blood Sugar" instead of "Hyperglycemia"]**

        **What is this?**
        - Explain in everyday language what this condition means
        - Use comparisons to things people understand (like "your blood is like soup that's too thick")
        - Avoid medical terms, or if used, immediately explain them in simple words

        **How does this affect your body?**
        - Describe step-by-step what happens inside your body
        - Explain which parts of your body are affected and how
        - Use simple analogies (like "your heart works like a pump")
        - Describe any symptoms this might cause

        **Why did this happen?**
        - Explain the most common reasons this occurs
        - Use simple cause-and-effect explanations
        - Relate to lifestyle, age, genetics, or other easy-to-understand factors

        **What do your test numbers mean?**
        - Compare your numbers to what's normal (e.g., "Normal is 80-100, yours is 150")
        - Explain if this is slightly high, very high, or extremely high
        - Use simple comparisons ("This is like having 3 teaspoons of sugar in your blood when you should only have 2")

        **Is this serious?**
        - Clearly state if this is minor, moderate, or serious
        - Explain what could happen if not treated
        - Use simple terms about risks

        **Problem 2: [If more problems exist]**
        [Same detailed, simple explanation for each additional problem]

        ### **HOW ARE THESE PROBLEMS CONNECTED?**
        - Explain in simple terms how different health issues might be related
        - Use easy examples of how one problem can cause another
        - Help the person understand the "big picture" of their health

        ### **WHAT DO YOUR TEST RESULTS MEAN?**
        [For any lab values or test results:]
        - **Your number vs. Normal number**: Clear comparison in simple terms
        - **What this means**: Explain without medical jargon
        - **Is this good or bad?**: Direct, honest assessment
        - **How much off from normal?**: Use percentages or simple comparisons

        ## ⚠️ HOW SERIOUS IS THIS?
        **Level**: [Normal/Mild/Moderate/Severe]
        **In Simple Terms**: [Explain severity using everyday language - e.g., "This is like having a warning light on your car dashboard - not an emergency, but needs attention soon"]

        ## 🏥 WHICH DOCTOR TO SEE
        **Type of Doctor**: [Specialist name]
        **Why This Doctor**: [Simple explanation of what this doctor specializes in]
        **How Soon**: [Urgent/Soon/Routine - with simple explanation]

        ## 🥗 FOODS THAT HELP OR HURT
        **Foods That Will Help You**:
        - [List with simple explanations of why each food helps]

        **Foods to Avoid**:
        - [List with simple explanations of why each food is harmful]

        **Easy Diet Tips**: [Simple, practical advice]

        ## 🛡️ THINGS TO DO AND AVOID
        **Important Things to Do Right Now**:
        - [Simple, actionable steps]

        **Changes to Make in Daily Life**:
        - [Easy-to-understand lifestyle changes]

        **Activities to Be Careful With**:
        - [Clear activity guidelines]

        ## 💊 TREATMENT - WHAT TO EXPECT
        [Explain treatments in simple terms - what they do, how they work, what to expect]

        ## 📅 FOLLOW-UP - WHAT HAPPENS NEXT
        [Simple timeline of what needs to be done and when]

        ## ⚕️ IMPORTANT REMINDER
        This explanation is to help you understand your health better, but you must still see a real doctor. They know your full medical history and can give you proper treatment. Don't make medical decisions based only on this analysis.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Using Llama 3.3 70B for comprehensive medical analysis
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=8000  # Increased token limit for detailed analysis
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error analyzing report: {str(e)}"
    
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

# Streamlit Web Application
def main():
    st.set_page_config(
        page_title="Medical Report Analyzer",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 AI Medical Report Analyzer")
    st.markdown("Upload your medical report (PDF or Image) for comprehensive health insights")
    
    # Initialize analyzer - API key is automatically loaded from .env
    try:
        analyzer = MedicalReportAnalyzer()
        if analyzer.api_configured:
            st.success("✅ AI Medical Analyzer Ready!")
        else:
            st.error(f"❌ API Configuration Error: {analyzer.api_error}")
            st.info("Please check your .env file and ensure GROQ_API_KEY is set correctly.")
            return
    except ValueError as e:
        st.error(f"❌ Configuration Error: {str(e)}")
        st.info("Make sure you have a .env file with GROQ_API_KEY in your project directory.")
        return
    except Exception as e:
        st.error(f"❌ Initialization Error: {str(e)}")
        return
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a medical report file",
        type=['pdf', 'jpg', 'jpeg', 'png', 'tiff', 'bmp'],
        help="Upload PDF documents or image files of medical reports"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ File uploaded successfully!")
            for key, value in file_details.items():
                st.write(f"**{key}:** {value}")
        
        with col2:
            # Show preview for images
            if uploaded_file.type.startswith('image/'):
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        # Determine file type
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        # Process button
        if st.button("🔍 Analyze Medical Report", type="primary"):
            with st.spinner("Processing your medical report..."):
                try:
                    # Process the file
                    result = analyzer.process_file(uploaded_file, file_type)
                    
                    if isinstance(result, dict):
                        # Display extracted text
                        with st.expander("📄 Extracted Text from Report", expanded=False):
                            st.text_area("Raw Text", result["extracted_text"], height=200)
                        
                        # Display analysis
                        st.markdown("## 📋 Medical Analysis Report")
                        st.markdown(result["analysis"])
                        
                        # Download option
                        analysis_text = f"MEDICAL REPORT ANALYSIS\n{'='*50}\n\n{result['analysis']}"
                        st.download_button(
                            label="💾 Download Analysis Report",
                            data=analysis_text,
                            file_name=f"medical_analysis_{uploaded_file.name}.txt",
                            mime="text/plain"
                        )
                        
                    else:
                        st.error(result)
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Please check if Tesseract OCR is installed for image processing.")
    
    # Instructions and disclaimers
    with st.sidebar:
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. Configure your Groq API key above
        2. Upload a medical report (PDF/Image)
        3. Click 'Analyze Medical Report'
        4. Review the comprehensive analysis
        5. Download the report if needed
        """)
        
        st.markdown("### ⚠️ Important Notes")
        st.markdown("""
        - This tool is for informational purposes only
        - Always consult healthcare professionals
        - Do not delay seeking medical attention
        - Keep your medical data secure
        """)
        
        st.markdown("### 🔧 Supported Formats")
        st.markdown("""
        - **PDF**: Medical reports, lab results
        - **Images**: JPG, PNG, TIFF, BMP
        - **OCR**: Automatic text extraction
        """)
        
        st.markdown("### 💡 Tips for Better Results")
        st.markdown("""
        - Use high-quality, clear images
        - Ensure text is readable and not blurry
        - For images, good lighting helps OCR
        - PDF files generally work better than images
        """)

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
        """Analyze PDF file"""
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
        """Analyze image file"""
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
        """Display analysis result"""
        if isinstance(result, dict):
            print(f"\n📄 Analysis for: {file_path}")
            print("=" * 50)
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
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Run CLI version
        cli = CLIMedicalAnalyzer()
        cli.run()
    else:
        # Run Streamlit web app
        main()