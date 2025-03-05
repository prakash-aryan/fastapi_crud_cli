#!/usr/bin/env python3

import os
import sys
import subprocess
import threading
import time
import socket
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))

def is_port_in_use(port, host='127.0.0.1'):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def start_api_server():
    """Start the FastAPI server as a subprocess"""
    global API_PORT  # Declare global at beginning of function
    
    # Check if port is already in use
    if is_port_in_use(API_PORT, API_HOST):
        print(f"Port {API_PORT} is already in use.")
        choice = input("Do you want to (1) use the existing server, (2) try a different port, or (3) exit? [1/2/3]: ")
        
        if choice == '1':
            print(f"Using existing server at http://{API_HOST}:{API_PORT}")
            return True
        elif choice == '2':
            # Try to find an available port
            for port in range(API_PORT + 1, API_PORT + 100):
                if not is_port_in_use(port, API_HOST):
                    print(f"Found available port: {port}")
                    API_PORT = port
                    break
            else:
                print("Could not find an available port. Exiting.")
                return False
        else:
            print("Exiting application.")
            return False
    
    print(f"Starting FastAPI server on port {API_PORT}...")
    # Set environment variable to control uvicorn logging 
    os.environ["UVICORN_LOG_LEVEL"] = "error"
    
    # Run with log suppression
    subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", API_HOST, "--port", str(API_PORT), 
         "--log-level", "error", "--no-access-log"],
        stdout=subprocess.DEVNULL,  # Suppress standard output
        stderr=sys.stderr  # Keep stderr for error messages
    )
    return True

def check_api_server():
    """Check if API server is running"""
    import requests
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get(f"http://{API_HOST}:{API_PORT}")
            if response.status_code == 200:
                print("API server is running.")
                return True
        except:
            pass
        
        attempts += 1
        print(f"Waiting for API server to start (attempt {attempts}/{max_attempts})...")
        time.sleep(1)
    
    print("Failed to connect to API server.")
    return False

def start_cli():
    """Start the CLI application"""
    from cli.cli import CrudCLI
    # Update the CLI with the potentially changed port
    cli = CrudCLI(api_port=API_PORT)
    cli.run()

if __name__ == "__main__":
    # Start API server first
    if not start_api_server():
        sys.exit(1)
    
    # Wait for API server to start
    if check_api_server():
        # Start CLI application
        start_cli()
    else:
        print("Failed to start API server. Exiting.")
        sys.exit(1)