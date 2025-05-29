import google.generativeai as genai
import os

def generate_analysis_code(file_info, analysis_type):
    # Setup Gemini
    genai.configure(api_key=os.getenv("AIzaSyAjFIgztRUqg3ex5fos61atuGGTxKiwPh0"))
    model = genai.GenerativeModel('gemini-pro')
    
    # Create secure prompt
    prompt = f"""
    Create Python code for {analysis_type} with these security rules:
    - Only use: pandas, matplotlib, numpy, scipy
    - No internet access or file writing
    - Handle errors gracefully
    - Save plot as 'output.png'
    - Print results as JSON at the end
    
    Data file: {file_info['path']} ({file_info['type']})
    """
    
    # Get response from Gemini
    response = model.generate_content(prompt)
    return response.text