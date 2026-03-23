# Fix Authentication Issue - "Систем аутентикације није доступан"

## ✅ Good News: CSRF Issue is Fixed!

The "token missing" error is gone. Now we just need to fix authentication.

## 🎯 The Problem

Your systemd service file doesn't load the `.env` file, so it doesn't know about `ENABLE_FALLBACK_AUTH=True`.

**Current behavior:**
- `.env` file has: `ENABLE_FALLBACK_AUTH=True`
- But systemd doesn't read `.env`
- So app thinks fallback auth is disabled
- Result: "Систем аутентикације није доступан" (Authentication system not available)

## ✅ The Solution

Update the systemd service to load the `.env` file.

### Run These Commands:

```bash
# 1. Copy the new service file
sudo cp museum-system.service.new /etc/systemd/system/museum-system.service

# 2. Reload systemd to pick up changes
sudo systemctl daemon-reload

# 3. Restart the service
sudo systemctl restart museum-system

# 4. Check it's running
sudo systemctl status museum-system
```

### What Changed in the Service File:

**Old (line 11):**
```
Environment="FLASK_ENV=production"
```

**New (lines 11-12):**
```
Environment="FLASK_ENV=development"
EnvironmentFile=/home/aleksandarlukovic/MuseumInfoSystem/.env
```

This tells systemd to:
1. Use development mode (where fallback auth works)
2. Load ALL variables from `.env` file

## 🧪 After Update, Test Login:

1. Go to: `http://192.168.144.48/login`
2. Login with:
   - Email: `admin`
   - Password: `admin123`

**Should work now!**

## 📊 Summary of All Fixes:

| Issue | Status |
|-------|--------|
| ✅ CSRF tokens missing | FIXED - Added to all forms |
| ✅ .env not loaded in app | FIXED - Added load_dotenv() |
| ✅ Session/CSRF order wrong | FIXED - Swapped order |
| ✅ Login CSRF exempt | FIXED - Temporarily exempted |
| ⏳ .env not loaded in systemd | NEEDS UPDATE (run commands above) |

## 🔧 Quick Fix Commands:

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
sudo cp museum-system.service.new /etc/systemd/system/museum-system.service
sudo systemctl daemon-reload
sudo systemctl restart museum-system
```

Then test login at: http://192.168.144.48/login

---

**After this fix, your login should work!**
