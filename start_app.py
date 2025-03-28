import subprocess
import sys
import os
import time
import webbrowser

def start_servers():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Start the backend server
    backend_cmd = [sys.executable, "run.py"]
    backend_process = subprocess.Popen(
        backend_cmd,
        cwd=current_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for backend to start
    time.sleep(2)
    
    # Start the frontend server
    frontend_dir = os.path.join(current_dir, "src", "frontend")
    frontend_cmd = [sys.executable, "-m", "http.server", "3000"]
    frontend_process = subprocess.Popen(
        frontend_cmd,
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("Starting servers...")
    print("Backend server running at http://localhost:8000")
    print("Frontend server running at http://localhost:3000")
    
    # Open the frontend in the default browser
    webbrowser.open("http://localhost:3000")
    
    try:
        # Wait for both processes
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped")

if __name__ == "__main__":
    start_servers() 