#!/bin/bash

# InsightDeck Agent - Cloudflare Tunnel Setup Script
# This script helps you set up Cloudflare Tunnel for secure deployment

set -e

echo "🚀 InsightDeck Agent - Cloudflare Tunnel Setup"
echo "=============================================="
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared is not installed"
    echo ""
    echo "Installing cloudflared..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install cloudflare/cloudflare/cloudflared
        else
            echo "❌ Homebrew not found. Please install Homebrew first:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i cloudflared-linux-amd64.deb
        rm cloudflared-linux-amd64.deb
    else
        echo "❌ Unsupported OS. Please install cloudflared manually:"
        echo "   https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
        exit 1
    fi
fi

echo "✅ cloudflared is installed"
echo ""

# Step 1: Login
echo "📝 Step 1: Authenticate with Cloudflare"
echo "========================================"
echo "This will open your browser. Please select your domain."
echo ""
read -p "Press Enter to continue..."

cloudflared tunnel login

echo ""
echo "✅ Authentication complete"
echo ""

# Step 2: Create tunnel
echo "📝 Step 2: Create Tunnel"
echo "========================"
echo ""
read -p "Enter a name for your tunnel (default: insightdeck-agent): " TUNNEL_NAME
TUNNEL_NAME=${TUNNEL_NAME:-insightdeck-agent}

echo "Creating tunnel: $TUNNEL_NAME..."
TUNNEL_OUTPUT=$(cloudflared tunnel create "$TUNNEL_NAME")
TUNNEL_ID=$(echo "$TUNNEL_OUTPUT" | grep -o '[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}' | head -n 1)

if [ -z "$TUNNEL_ID" ]; then
    echo "❌ Failed to create tunnel"
    exit 1
fi

echo "✅ Tunnel created successfully"
echo "   Tunnel ID: $TUNNEL_ID"
echo ""

# Step 3: Configure tunnel
echo "📝 Step 3: Configure Tunnel"
echo "==========================="
echo ""
read -p "Enter your domain (e.g., yourdomain.com): " DOMAIN
read -p "Enter subdomain (default: insightdeck): " SUBDOMAIN
SUBDOMAIN=${SUBDOMAIN:-insightdeck}

FULL_DOMAIN="$SUBDOMAIN.$DOMAIN"

echo ""
echo "Creating configuration file..."

# Find credentials file
CREDS_FILE="$HOME/.cloudflared/$TUNNEL_ID.json"

# Create config directory if it doesn't exist
mkdir -p "$HOME/.cloudflared"

# Create config file
cat > "$HOME/.cloudflared/config.yml" << EOF
tunnel: $TUNNEL_ID
credentials-file: $CREDS_FILE

ingress:
  - hostname: $FULL_DOMAIN
    service: http://localhost:8080
  - service: http_status:404
EOF

echo "✅ Configuration file created: $HOME/.cloudflared/config.yml"
echo ""

# Step 4: Route DNS
echo "📝 Step 4: Route DNS"
echo "===================="
echo ""
echo "Creating DNS record for $FULL_DOMAIN..."

cloudflared tunnel route dns "$TUNNEL_NAME" "$FULL_DOMAIN"

echo "✅ DNS record created"
echo ""

# Step 5: Instructions
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Your tunnel is ready to use. To start the services:"
echo ""
echo "Terminal 1 - Start Flask App:"
echo "  cd $(pwd)"
echo "  source venv/bin/activate"
echo "  python web_app.py"
echo ""
echo "Terminal 2 - Start Cloudflare Tunnel:"
echo "  cloudflared tunnel run $TUNNEL_NAME"
echo ""
echo "Your app will be accessible at: https://$FULL_DOMAIN"
echo ""
echo "📚 Next Steps:"
echo "1. Start both services (see commands above)"
echo "2. Visit https://$FULL_DOMAIN in your browser"
echo "3. (Optional) Set up Zero Trust authentication:"
echo "   https://one.dash.cloudflare.com/"
echo ""
echo "📖 For more details, see DEPLOYMENT.md"
echo ""

# Offer to install as service
echo "Would you like to install cloudflared as a system service?"
echo "This will make the tunnel start automatically on boot."
read -p "(y/N): " INSTALL_SERVICE

if [[ "$INSTALL_SERVICE" == "y" || "$INSTALL_SERVICE" == "Y" ]]; then
    echo ""
    echo "Installing cloudflared as a service..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sudo cloudflared service install
        echo "✅ Service installed"
        echo ""
        echo "To manage the service:"
        echo "  sudo launchctl start com.cloudflare.cloudflared"
        echo "  sudo launchctl stop com.cloudflare.cloudflared"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo cloudflared service install
        sudo systemctl start cloudflared
        sudo systemctl enable cloudflared
        echo "✅ Service installed and started"
        echo ""
        echo "To manage the service:"
        echo "  sudo systemctl status cloudflared"
        echo "  sudo systemctl restart cloudflared"
        echo "  sudo systemctl stop cloudflared"
    fi
fi

echo ""
echo "🚀 Ready to deploy!"
