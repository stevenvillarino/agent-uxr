#!/bin/bash

# Agent-UXR Automated Setup Script
# This script sets up the entire environment for a successful demo

set -e  # Exit on any error

echo "🚀 Starting Agent-UXR Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION found"

# Check if we're already in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    print_warning "Already in a virtual environment: $VIRTUAL_ENV"
    print_status "Using existing environment..."
else
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv .venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source .venv/bin/activate
    print_success "Virtual environment activated"
fi

# Upgrade pip
print_status "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
print_status "Installing Python packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "All packages installed successfully"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Azure Speech Services
AZURE_SPEECH_KEY=your_azure_key_here
AZURE_SPEECH_REGION=your_azure_region_here

# Optional: AWS Transcribe
AWS_ACCESS_KEY_ID=your_aws_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_here

# Application Settings
FLASK_ENV=development
DEBUG=True
EOF
    print_warning ".env file created. Please edit it with your actual API keys!"
    print_status "You can edit .env with: nano .env"
else
    print_success ".env file already exists"
fi

# Verify OpenAI installation
print_status "Verifying OpenAI Whisper installation..."
if python -c "import whisper; print('Whisper version:', whisper.__version__)" 2>/dev/null; then
    print_success "OpenAI Whisper is installed and working"
else
    print_error "OpenAI Whisper installation failed"
    exit 1
fi

# Check if OpenAI API key is set
print_status "Checking OpenAI API configuration..."
if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
    print_warning "OpenAI API key is not configured in .env file"
    print_status "The demo will not work until you add your API key"
else
    print_success "OpenAI API key appears to be configured"
fi

# Create outputs directory if it doesn't exist
if [ ! -d "outputs" ]; then
    mkdir -p outputs
    print_success "Created outputs directory"
fi

# Test basic functionality
print_status "Running basic functionality test..."
if python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('✅ Environment loading works')

try:
    import openai
    print('✅ OpenAI package imported')
except ImportError as e:
    print('❌ OpenAI import failed:', e)
    exit(1)

try:
    import whisper
    print('✅ Whisper package imported')
except ImportError as e:
    print('❌ Whisper import failed:', e)
    exit(1)

try:
    import flask
    print('✅ Flask package imported')
except ImportError as e:
    print('❌ Flask import failed:', e)
    exit(1)
" 2>/dev/null; then
    print_success "All core packages are working correctly"
else
    print_error "Package verification failed"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key:"
echo "   ${YELLOW}nano .env${NC}"
echo ""
echo "2. Test the demo with sample data:"
echo "   ${BLUE}python main_enhanced.py sample_data/user_interview_dashboard.txt${NC}"
echo ""
echo "3. Or start the web interface:"
echo "   ${BLUE}python web_app.py${NC}"
echo "   Then open: http://localhost:5000"
echo ""
echo "4. For troubleshooting, see: ${BLUE}STARTUP.md${NC}"
echo ""

# Check if we need to remind about activation
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "💡 Remember to activate the virtual environment in new terminals:"
    echo "   ${YELLOW}source .venv/bin/activate${NC}"
fi