# InsightDeck Agent - Deployment Guide

**Last Updated:** October 2, 2025  
**Deployment Method:** Cloudflare Tunnel with Zero Trust

---

## 🎯 Overview

This guide covers deploying InsightDeck Agent using **Cloudflare Tunnel**, which provides:
- ✅ Secure HTTPS access without exposing ports
- ✅ Built-in Zero Trust authentication
- ✅ No code changes required
- ✅ Free hosting
- ✅ Global CDN performance

---

## 📋 Prerequisites

- Cloudflare account with a domain
- macOS/Linux/Windows machine to run the app
- Flask app running locally on port 8080

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Cloudflared

```bash
# macOS
brew install cloudflare/cloudflare/cloudflared

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Windows
# Download from: https://github.com/cloudflare/cloudflared/releases
```

### Step 2: Authenticate with Cloudflare

```bash
cloudflared tunnel login
```

This opens your browser to authorize cloudflared. Select your domain.

### Step 3: Create the Tunnel

```bash
cloudflared tunnel create insightdeck-agent
```

**Save the Tunnel ID** that's displayed (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### Step 4: Create Configuration File

```bash
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

**Add this configuration:**

```yaml
tunnel: YOUR_TUNNEL_ID_HERE
credentials-file: /Users/YOUR_USERNAME/.cloudflared/YOUR_TUNNEL_ID_HERE.json

ingress:
  - hostname: insightdeck.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
```

**Replace:**
- `YOUR_TUNNEL_ID_HERE` with your actual tunnel ID
- `YOUR_USERNAME` with your system username
- `yourdomain.com` with your Cloudflare domain

### Step 5: Route DNS

```bash
cloudflared tunnel route dns insightdeck-agent insightdeck.yourdomain.com
```

This automatically creates a CNAME record in your Cloudflare DNS.

### Step 6: Start the Services

**Terminal 1 - Start Flask App:**
```bash
cd /Users/stevenvillarino/Projects/stevenvillarino/agent-uxr
source venv/bin/activate
python web_app.py
```

**Terminal 2 - Start Cloudflare Tunnel:**
```bash
cloudflared tunnel run insightdeck-agent
```

**✅ Your app is now live at:** `https://insightdeck.yourdomain.com`

---

## 🔒 Add Zero Trust Authentication

Protect your app so only authorized users can access it.

### Step 1: Go to Cloudflare Zero Trust

1. Visit: https://one.dash.cloudflare.com/
2. Navigate to: **Access** → **Applications**
3. Click: **Add an application**

### Step 2: Configure Application

**Application Type:** Self-hosted

**Application Settings:**
- **Application name:** InsightDeck Agent
- **Session Duration:** 24 hours (or as needed)
- **Application domain:**
  - Subdomain: `insightdeck`
  - Domain: `yourdomain.com`

### Step 3: Create Access Policy

**Policy Name:** Allow Team Members

**Action:** Allow

**Configure rules:**

**Option A - Email Domain:**
```
Include:
- Emails ending in: @yourcompany.com
```

**Option B - Specific Users:**
```
Include:
- Emails: user1@example.com, user2@example.com
```

**Option C - Everyone with Login:**
```
Include:
- Everyone
```

### Step 4: Identity Providers

Choose how users authenticate:
- ✅ **One-time PIN** (email-based, easiest)
- ✅ **Google Workspace**
- ✅ **GitHub**
- ✅ **Microsoft Azure AD**
- ✅ **Okta**

### Step 5: Save & Test

1. Click **Save application**
2. Visit `https://insightdeck.yourdomain.com`
3. You'll see Cloudflare Access login page
4. Authenticate and access your app!

---

## 🔧 Run as System Service (Optional)

To keep the tunnel running even after logout:

### macOS/Linux

**Create service file:**
```bash
sudo cloudflared service install
```

**Edit config:**
```bash
sudo nano /etc/cloudflared/config.yml
```

**Start service:**
```bash
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

**Check status:**
```bash
sudo systemctl status cloudflared
```

---

## 🐳 Docker Deployment (Alternative)

If you prefer containerization:

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Run app
CMD ["python", "web_app.py"]
```

### Build & Run

```bash
# Build
docker build -t insightdeck-agent .

# Run
docker run -d \
  -p 8080:8080 \
  --env-file .env \
  --name insightdeck-agent \
  insightdeck-agent

# View logs
docker logs -f insightdeck-agent
```

### Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:8080"
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./outputs:/app/outputs
      - ./sample_data:/app/sample_data

  cloudflared:
    image: cloudflare/cloudflared:latest
    command: tunnel run
    volumes:
      - ~/.cloudflared:/etc/cloudflared
    restart: unless-stopped
    depends_on:
      - web
```

**Run:**
```bash
docker-compose up -d
```

---

## 🌍 Alternative Deployment Options

### Option 1: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**Add environment variables in Railway dashboard**

### Option 2: Render

1. Connect GitHub repo to Render
2. Create new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python web_app.py`
5. Add environment variables

### Option 3: Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

### Option 4: Cloudflare Workers (Requires Refactoring)

For serverless deployment, the Flask app would need to be converted to Workers format.

---

## 📊 Production Checklist

Before going to production:

### Security
- [ ] Enable Cloudflare Zero Trust authentication
- [ ] Set up rate limiting in Cloudflare
- [ ] Enable WAF (Web Application Firewall)
- [ ] Use secrets management (not .env file)
- [ ] Enable HTTPS only (disable HTTP)
- [ ] Set secure session cookies
- [ ] Add CSRF protection
- [ ] Implement API key rotation

### Performance
- [ ] Enable Cloudflare caching for static assets
- [ ] Use CDN for JavaScript/CSS libraries
- [ ] Optimize image sizes
- [ ] Enable gzip compression
- [ ] Use production WSGI server (gunicorn/uwsgi)
- [ ] Set up connection pooling
- [ ] Cache API responses where appropriate

### Reliability
- [ ] Set up health checks
- [ ] Configure auto-restart on failure
- [ ] Set up monitoring (Cloudflare Analytics)
- [ ] Enable error logging
- [ ] Configure backups for outputs
- [ ] Set up alerting for errors
- [ ] Test failover scenarios

### Monitoring
- [ ] Set up Cloudflare Analytics
- [ ] Configure log aggregation
- [ ] Set up uptime monitoring
- [ ] Track API usage/costs
- [ ] Monitor error rates
- [ ] Set up performance metrics

---

## 🔧 Configuration Examples

### Production WSGI Server (Gunicorn)

**Install:**
```bash
pip install gunicorn
```

**Run:**
```bash
gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 120 web_app:app
```

**Update requirements.txt:**
```txt
gunicorn==21.2.0
```

### Nginx Reverse Proxy (Optional)

```nginx
server {
    listen 8080;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for long-running transcription
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

---

## 🐛 Troubleshooting

### Tunnel won't start

```bash
# Check tunnel status
cloudflared tunnel info insightdeck-agent

# View tunnel logs
cloudflared tunnel run insightdeck-agent --loglevel debug

# List all tunnels
cloudflared tunnel list

# Clean up old tunnels
cloudflared tunnel delete OLD_TUNNEL_NAME
```

### DNS not resolving

```bash
# Check DNS records
dig insightdeck.yourdomain.com

# Verify CNAME record in Cloudflare dashboard
# Should point to: YOUR_TUNNEL_ID.cfargotunnel.com
```

### App not accessible

```bash
# Check if Flask is running
curl http://localhost:8080

# Check cloudflared connection
cloudflared tunnel info insightdeck-agent

# Test DNS resolution
nslookup insightdeck.yourdomain.com
```

### Zero Trust blocking access

1. Check Access logs in Cloudflare dashboard
2. Verify user email matches policy rules
3. Check identity provider is configured
4. Try disabling policy temporarily to test

---

## 📝 Maintenance

### Update Application

```bash
# Pull latest code
git pull origin master

# Restart Flask app
pkill -f "python.*web_app.py"
source venv/bin/activate
python web_app.py
```

### Update Cloudflared

```bash
# macOS
brew upgrade cloudflare/cloudflare/cloudflared

# Linux
sudo cloudflared update
```

### Rotate API Keys

1. Update `.env` file with new keys
2. Restart Flask app
3. Test connections in Settings page

### View Logs

```bash
# Flask app logs (if running in background)
tail -f nohup.out

# Cloudflared logs
journalctl -u cloudflared -f

# Or if running directly
cloudflared tunnel run insightdeck-agent --loglevel info
```

---

## 💰 Cost Estimates

### Cloudflare Tunnel
- **Free** for personal/small business use
- Unlimited bandwidth
- Unlimited requests

### API Costs (Monthly)
- **OpenAI GPT-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **ElevenLabs Speech-to-Text**: ~$0.30 per hour of audio (Free tier: 10K characters)
- **Total estimated**: $10-50/month depending on usage

### Alternative Hosting (if not self-hosted)
- **Railway**: Free tier → $5-20/month
- **Render**: Free tier → $7/month
- **Fly.io**: Free tier → $10/month

---

## 🔗 Useful Links

- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [Cloudflare Zero Trust](https://developers.cloudflare.com/cloudflare-one/applications/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Cloudflare documentation
3. Check application logs
4. Verify API keys and configuration

---

**Deployment Status:** Ready for production ✅
