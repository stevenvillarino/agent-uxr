# 🚀 Quick Deployment Guide

## One-Command Setup

```bash
./setup-tunnel.sh
```

This interactive script will:
1. ✅ Install cloudflared (if needed)
2. ✅ Authenticate with Cloudflare
3. ✅ Create tunnel
4. ✅ Configure DNS
5. ✅ Generate config files

---

## Start Services

### Terminal 1: Flask App
```bash
cd /Users/stevenvillarino/Projects/stevenvillarino/agent-uxr
source venv/bin/activate
python web_app.py
```

### Terminal 2: Cloudflare Tunnel
```bash
cloudflared tunnel run insightdeck-agent
```

---

## Access Your App

**Local:** http://localhost:8080  
**Public:** https://insightdeck.yourdomain.com

---

## Add Zero Trust Authentication

1. Go to: https://one.dash.cloudflare.com/
2. Navigate to: **Access** → **Applications**
3. Click: **Add an application**
4. Choose: **Self-hosted**
5. Configure:
   - Application name: InsightDeck Agent
   - Domain: insightdeck.yourdomain.com
6. Add policy:
   - Action: Allow
   - Include: Emails ending in @yourcompany.com
7. Save!

Now only authorized users can access your app.

---

## Useful Commands

### Check tunnel status
```bash
cloudflared tunnel info insightdeck-agent
cloudflared tunnel list
```

### View tunnel logs
```bash
cloudflared tunnel run insightdeck-agent --loglevel debug
```

### Stop services
```bash
# Stop Flask (Ctrl+C in Terminal 1)
# Stop tunnel (Ctrl+C in Terminal 2)
```

### Update app
```bash
git pull origin master
# Restart Flask app
```

---

## Troubleshooting

**App not accessible?**
```bash
# Check if Flask is running
curl http://localhost:8080

# Check tunnel
cloudflared tunnel info insightdeck-agent
```

**DNS not working?**
```bash
# Verify DNS record
dig insightdeck.yourdomain.com

# Should show CNAME to: YOUR_TUNNEL_ID.cfargotunnel.com
```

**API keys not loading?**
```bash
# Make sure .env file exists
cat .env | grep API_KEY

# Restart Flask app to reload environment
```

---

## Production Checklist

- [ ] Enable Zero Trust authentication
- [ ] Set up rate limiting in Cloudflare
- [ ] Enable Cloudflare WAF
- [ ] Use production WSGI server (gunicorn)
- [ ] Set up error monitoring
- [ ] Configure backups for outputs/
- [ ] Test with sample data
- [ ] Document access procedures for team

---

## Cost Overview

- **Cloudflare Tunnel:** Free
- **OpenAI API:** ~$0.15-0.60 per 1M tokens
- **ElevenLabs:** ~$0.30 per hour of audio (10K chars free)
- **Total:** ~$10-50/month depending on usage

---

## Need Help?

📖 Full guide: [DEPLOYMENT.md](DEPLOYMENT.md)  
🐛 Issues: Check troubleshooting section above  
📧 Contact: [Your email]

**Status:** ✅ Ready for Production
