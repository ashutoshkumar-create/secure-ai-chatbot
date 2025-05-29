from e2b import Sandbox
import base64
import os

def run_in_sandbox(code, file_path):
    # Create isolated environment
    with Sandbox() as sandbox:
        # Upload data file
        file_name = os.path.basename(file_path)
        sandbox.filesystem.write(file_name, open(file_path, "rb").read())
        
        # Upload code
        sandbox.filesystem.write("/code.py", code)
        
        # Install required packages
        sandbox.process.start_and_wait("pip install pandas matplotlib numpy scipy")
        
        # Execute code safely
        process = sandbox.process.start_and_wait("python /code.py", timeout=30)
        
        # Get results
        if process.exit_code == 0:
            if sandbox.filesystem.exists("output.png"):
                image = sandbox.filesystem.read("output.png")
                return {"image": base64.b64encode(image).decode("utf-8")}
            return {"output": process.stdout}
        else:
            raise Exception(f"Error: {process.stderr}")