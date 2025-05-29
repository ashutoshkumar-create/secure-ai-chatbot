import base64
import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from gemini_integration import generate_analysis_code
from sandbox import run_in_sandbox
from security_utils import safe_extension

# Load environment variables
load_dotenv()

# Setup page
st.title("🔒 Secure Data Analysis Chatbot")
st.write("Upload your data and choose analysis type")

# File upload
uploaded_file = st.file_uploader("Choose CSV or Excel file", type=["csv", "xlsx"])

# Analysis selection
analysis_type = st.selectbox(
    "Select analysis type",
    ["Scatter Plot", "Line Chart", "Histogram", "Linear Regression"]
)

# Process button
if st.button("Run Analysis") and uploaded_file:
    if not safe_extension(uploaded_file.name):
        st.error("Only CSV or Excel files allowed!")
    else:
        with st.spinner("Processing securely..."):
            try:
                # Save file temporarily
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    file_path = tmp.name
                
                # Generate code
                file_info = {"path": file_path, "type": uploaded_file.type}
                code = generate_analysis_code(file_info, analysis_type)
                
                # Run in sandbox
                results = run_in_sandbox(code, file_path)
                
                # Show results
                if "image" in results:
                    st.image(base64.b64decode(results["image"]))
                else:
                    st.write(results["output"])
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                # Clean up
                if os.path.exists(file_path):
                    os.remove(file_path)