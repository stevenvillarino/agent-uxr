#!/bin/bash

# Quick Start Script for Testing the Fixed Application
# This script helps you verify that the text analysis bug has been fixed

set -e  # Exit on error

echo "============================================================================="
echo "InsightDeck Agent - Quick Start Test"
echo "============================================================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Please create a .env file with your OpenAI API key:"
    echo "  cp .env.template .env"
    echo "  # Then edit .env and add your OPENAI_API_KEY"
    echo ""
    exit 1
fi

# Check if OpenAI key is configured
if grep -q "your_openai_api_key_here" .env; then
    echo "❌ OpenAI API key not configured!"
    echo ""
    echo "Please edit .env and replace 'your_openai_api_key_here' with your actual key"
    echo ""
    exit 1
fi

echo "✅ Environment configuration found"
echo ""

# Check Python dependencies
echo "📦 Checking Python dependencies..."
python -c "import openai" 2>/dev/null || {
    echo "❌ OpenAI package not installed"
    echo "Installing dependencies..."
    pip install -r requirements.txt
}

python -c "import flask" 2>/dev/null || {
    echo "❌ Flask not installed"
    echo "Installing dependencies..."
    pip install -r requirements.txt
}

echo "✅ Dependencies installed"
echo ""

# Run the standalone test
echo "============================================================================="
echo "Step 1: Testing OpenAI Integration"
echo "============================================================================="
echo ""
python test_analysis.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================================="
    echo "Step 2: Starting Web Application"
    echo "============================================================================="
    echo ""
    echo "The web server will start on http://localhost:5000"
    echo ""
    echo "To test the fix:"
    echo "  1. Open http://localhost:5000 in your browser"
    echo "  2. Enter a presentation title"
    echo "  3. Choose 'Paste Text' option"
    echo "  4. Paste some sample text (or use demo samples)"
    echo "  5. Click 'Generate Presentation'"
    echo "  6. Verify the analysis matches your pasted content"
    echo ""
    echo "Press Ctrl+C to stop the server when done testing"
    echo ""
    read -p "Press Enter to start the web server..."
    
    python web_app.py
else
    echo ""
    echo "❌ OpenAI integration test failed!"
    echo "Please check your API key and try again."
    exit 1
fi
