#!/bin/bash

# Legal Triage OpenEnv - Local Startup Script
echo "------------------------------------------------"
echo "🚀 Initializing Legal Triage OpenEnv..."
echo "------------------------------------------------"

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "❌ Error: pip could not be found. Please install Python and pip."
    exit 1
fi

# Install dependencies
echo "📦 Installing/Updating requirements (using --break-system-packages as requested)..."
pip install -r requirements.txt --break-system-packages

# Check for successful installation
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install requirements."
    exit 1
fi

echo "✅ Dependencies satisfied."

# Run the local server
echo "🌐 Starting Local Server at http://127.0.0.1:8000"
echo "💡 Use the UI to set your HF_TOKEN for automated inference."
echo "------------------------------------------------"

python3 run_local.py
