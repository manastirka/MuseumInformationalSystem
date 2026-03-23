# Fix Systemd Service Error - Step by Step

## ❌ Current Issue

The service file with `EnvironmentFile` is failing. We need to use a simpler approach.

## ✅ Solution - Use Simple Service File

Instead of loading the `.env` file, we'll set the environment variable directly in the service file.

---

## 🔧 Commands to Run:

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem

# 1. Copy the SIMPLE service file (no EnvironmentFile)
sudo cp museum-system.service.simple /etc/systemd/system/museum-system.service

# 2. Reload systemd
sudo systemctl daemon-reload

# 3. Start the service
sudo systemctl start museum-system

# 4. Check status
sudo systemctl status museum-system
```

---

## 📊 What's Different:

**Old (broken):**
```
EnvironmentFile=/home/aleksandarlukovic/MuseumInfoSystem/.env
```

**New (working):**
```
Environment="ENABLE_FALLBACK_AUTH=True"
Environment="FLASK_ENV=development"
```

We're setting the environment variables DIRECTLY in the service file instead of loading from `.env`.

---

## 🧪 After Running Commands:

1. Service should start successfully
2. Go to: `http://192.168.144.48/login`
3. Login with:
   - Email: `admin`
   - Password: `admin123`

---

## 🆘 If Service Still Won't Start:

Check the error:
```bash
sudo journalctl -xeu museum-system.service --no-pager | tail -30
```

---

## 📋 Quick Fix (Copy & Paste):

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
sudo cp museum-system.service.simple /etc/systemd/system/museum-system.service
sudo systemctl daemon-reload
sudo systemctl start museum-system
sudo systemctl status museum-system
```

Then test login at: **http://192.168.144.48/login**

---

**This simpler approach should work!**
