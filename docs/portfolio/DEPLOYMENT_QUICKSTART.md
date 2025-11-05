# 🚀 InsightDeck Agent: Deployment Quick Start
## Get Your Portfolio Demo Live in 15 Minutes

**Last Updated:** November 4, 2025

---

## 🎯 Goal: Deploy for Portfolio Showcase

**What you'll get:**
- ✅ Public demo URL for portfolio
- ✅ Secure access with authentication
- ✅ Professional presentation
- ✅ Zero monthly costs (using free tier)

**Recommended: Cloudflare Tunnel (Free + Secure)**

---

## 📋 Prerequisites

Before starting, make sure you have:

- [ ] **OpenAI API Key** - Get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- [ ] **Cloudflare Account** - Sign up free at [cloudflare.com](https://cloudflare.com)
- [ ] **Domain name** - Can use a free Cloudflare subdomain or your own
- [ ] **macOS/Linux/Windows** computer to run the app

---

## ⚡ Option 1: Cloudflare Tunnel (Recommended for Portfolio)

**Pros:** Free, secure, no port forwarding, built-in authentication
**Time:** 15 minutes
**Cost:** $0/month

### Step 1: Install Cloudflared

```bash
# macOS
brew install cloudflare/cloudflare/cloudflared

# Linux (Ubuntu/Debian)
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Windows
# Download from: https://github.com/cloudflare/cloudflared/releases
```

### Step 2: Authenticate

```bash
cloudflared tunnel login
```

This opens your browser - select your domain and authorize.

### Step 3: Create Tunnel

```bash
cloudflared tunnel create insightdeck-demo
```

**Save the Tunnel ID** shown (looks like `a1b2c3d4-1234-5678-90ab-cdef12345678`)

### Step 4: Configure DNS

Replace `yourdomain.com` with your actual domain:

```bash
cloudflared tunnel route dns insightdeck-demo insightdeck.yourdomain.com
```

This creates a CNAME record automatically.

### Step 5: Create Config File

```bash
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

Add this configuration (replace placeholders):

```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /Users/YOUR_USERNAME/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: insightdeck.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
```

### Step 6: Set Up Your App

```bash
# Clone repo (if not done already)
git clone https://github.com/stevenvillarino/agent-uxr.git
cd agent-uxr

# Set API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Run with Docker (recommended)
docker compose up -d
```

**OR run locally:**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
python web_app.py
```

### Step 7: Start Tunnel

In a **new terminal**:

```bash
cloudflared tunnel run insightdeck-demo
```

### Step 8: Test Access

Visit: `https://insightdeck.yourdomain.com`

You should see your InsightDeck Agent interface!

---

## 🔒 Add Authentication (Optional but Recommended)

Protect your demo so only you (or invited users) can access it.

### Step 1: Go to Cloudflare Zero Trust

Visit: [https://one.dash.cloudflare.com/](https://one.dash.cloudflare.com/)

### Step 2: Create Application

1. Navigate to: **Access** → **Applications**
2. Click: **Add an application**
3. Choose: **Self-hosted**

### Step 3: Configure

**Application Settings:**
- Application name: `InsightDeck Demo`
- Session duration: `24 hours`
- Domain: `insightdeck.yourdomain.com`

**Access Policy:**
- Policy name: `Portfolio Viewers`
- Action: `Allow`
- Include: `Emails` → Add your email(s)

**OR for public demo with email gate:**
- Include: `Everyone`
- Authentication method: `One-time PIN`

### Step 4: Save and Test

1. Save the application
2. Visit your URL
3. You'll see Cloudflare Access login
4. Enter email → receive code → access granted!

---

## 🐳 Option 2: Docker + Cloud Hosting

**Pros:** More control, scalable
**Time:** 20 minutes
**Cost:** $5-10/month

### Quick Deploy to DigitalOcean

```bash
# Create droplet (via DigitalOcean dashboard)
# - Choose Docker image
# - $6/month plan
# - Add SSH key

# SSH into droplet
ssh root@your-droplet-ip

# Clone and run
git clone https://github.com/stevenvillarino/agent-uxr.git
cd agent-uxr
echo "OPENAI_API_KEY=sk-your-key" > .env
docker compose up -d

# Access via: http://your-droplet-ip:8080
```

### Add Domain (Optional)

In DigitalOcean dashboard:
1. Go to **Networking** → **Domains**
2. Add your domain
3. Create A record: `insightdeck` → `your-droplet-ip`
4. Access via: `http://insightdeck.yourdomain.com:8080`

---

## 📱 Option 3: Local Demo (For Development)

**Pros:** Fastest to start, no hosting needed
**Time:** 5 minutes
**Cost:** $0
**Cons:** Not accessible from internet

```bash
# Clone repo
git clone https://github.com/stevenvillarino/agent-uxr.git
cd agent-uxr

# Set API key
echo "OPENAI_API_KEY=sk-your-key" > .env

# Run with Docker
docker compose up

# OR run locally
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python web_app.py

# Access at: http://localhost:8080
```

**For portfolio demos:**
- Use screen recording to create demo video
- Take screenshots for case study
- Use ngrok for temporary public access

**Temporary public access with ngrok:**
```bash
# Install ngrok
brew install ngrok  # macOS
# or download from ngrok.com

# Start tunnel
ngrok http 8080

# Use the https URL provided for demos
```

---

## 🎬 Portfolio Integration

### Create Demo Video

**Script (2-3 minutes):**

1. **Intro (15 sec)**
   - "Hi, I'm Steven. Let me show you InsightDeck Agent..."

2. **Problem (30 sec)**
   - "UX researchers spend 4-6 hours per interview on manual synthesis..."
   - Show traditional workflow diagram

3. **Demo (90 sec)**
   - Upload sample interview file
   - Show processing (sped up if needed)
   - Reveal generated insights and presentation
   - Highlight key themes extracted

4. **Impact (30 sec)**
   - "This reduces synthesis time by 85%..."
   - Show ROI calculation
   - Mention Roku background

**Tools:**
- Screen recording: QuickTime (Mac), OBS (all platforms)
- Video editing: iMovie, DaVinci Resolve (free)
- Hosting: YouTube, Vimeo, Loom

### Screenshots for Portfolio

Capture these screens:
1. Main upload interface
2. Processing status
3. Generated insights dashboard
4. Sample presentation output
5. Settings panel (with API keys redacted)

### Portfolio Page Structure

```markdown
# InsightDeck Agent

## AI-Powered UX Research Synthesis

[Live Demo Button] [View Code on GitHub]

### The Problem
UX researchers waste 60-80% of time on manual synthesis...

### The Solution
AI-powered pipeline that transforms interviews into presentations in 15 minutes.

[Demo Video Embed]

### Key Features
- 85% time reduction
- Automatic theme extraction
- Professional presentations
- Production-ready deployment

### Tech Stack
Python • Flask • OpenAI GPT-4o • Docker • React (planned)

[Screenshots Gallery]

### Impact
- $15K-45K annual savings per researcher
- 7x increase in research throughput
- Used at [Company/Demo Users]

[Link to Full Case Study]
```

---

## ✅ Pre-Launch Checklist

Before sharing your portfolio:

- [ ] Demo is accessible via public URL
- [ ] Sample data is loaded and tested
- [ ] Processing works end-to-end
- [ ] API keys are set and working (but not exposed)
- [ ] Screenshots are professional quality
- [ ] Demo video is polished and clear
- [ ] Case study document is complete
- [ ] GitHub README is comprehensive
- [ ] Error handling works gracefully
- [ ] Mobile responsive (test on phone)
- [ ] Load time is acceptable (<3 seconds)
- [ ] Authentication is configured (if needed)

---

## 🐛 Troubleshooting

### App Not Loading

```bash
# Check if app is running
curl http://localhost:8080

# Check Docker logs
docker compose logs -f

# Or check Flask logs if running locally
python web_app.py  # Look for errors in output
```

### Tunnel Not Working

```bash
# Check tunnel status
cloudflared tunnel info insightdeck-demo

# View tunnel logs
cloudflared tunnel run insightdeck-demo --loglevel debug

# Verify DNS
dig insightdeck.yourdomain.com
# Should show CNAME to *.cfargotunnel.com
```

### API Key Issues

```bash
# Verify .env file exists
cat .env | grep OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-your-key"

# Restart app to reload environment
docker compose restart  # or restart Python process
```

### Processing Fails

Check:
- API key is valid and has credits
- File size is under limits (25MB audio, 10MB text)
- File format is supported (.txt, .mp3, .wav, .m4a)
- OpenAI API is operational: [status.openai.com](https://status.openai.com)

---

## 💰 Cost Breakdown

### Free Option (Cloudflare Tunnel)
- Cloudflare Tunnel: **$0/month**
- Domain (if you have one): **$0-15/year**
- Server (run on your computer): **$0/month**
- **Total: $0-1.25/month**

### Paid Option (Cloud Hosting)
- DigitalOcean Droplet: **$6/month**
- Domain: **$15/year** ($1.25/month)
- Cloudflare (optional): **$0/month**
- **Total: $7.25/month**

### API Usage Costs
- OpenAI API: **~$0.15-0.60 per interview**
- For portfolio demos: **~$5-10/month** (20-50 demos)

**Recommendation for portfolio:** Use Cloudflare Tunnel (free) and budget $10-20 for API usage during job search.

---

## 🚀 Going Live Checklist

**Day 1: Setup**
- [ ] Deploy app
- [ ] Configure tunnel
- [ ] Test end-to-end
- [ ] Add authentication

**Day 2: Content**
- [ ] Record demo video
- [ ] Take screenshots
- [ ] Write portfolio page
- [ ] Update GitHub README

**Day 3: Launch**
- [ ] Share on LinkedIn
- [ ] Add to portfolio website
- [ ] Email to network
- [ ] Post in relevant communities

---

## 📞 Need Help?

**Common Issues:**
- Check [docs/deployment/DEPLOYMENT.md](../deployment/DEPLOYMENT.md) for detailed guide
- Search GitHub issues: [github.com/stevenvillarino/agent-uxr/issues](https://github.com/stevenvillarino/agent-uxr/issues)

**For Portfolio/Demo Questions:**
- Example portfolio pages: [Include examples]
- Demo video templates: [Link to templates]

---

## 🎉 You're Ready!

Your InsightDeck Agent is now live and ready to showcase:

✅ **Live demo URL** for recruiters and hiring managers
✅ **Professional presentation** of your work
✅ **Real, working product** (not just a prototype)
✅ **Clear business value** and technical skills

**Next steps:**
1. Share your demo URL in applications
2. Record walkthrough video
3. Write blog post about your journey
4. Present at portfolio reviews

**Good luck with your portfolio showcase!** 🚀

---

*Last Updated: November 4, 2025*
