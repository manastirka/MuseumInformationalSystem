# FINAL FIX - Manual Steps Required

## The Problem Found!

You have **TWO instances** of the application running:

1. **Port 8000** (Gunicorn via systemd) ← This is what nginx uses
   - Running OLD code WITHOUT CSRF fix
   - This is why 192.168.144.48 shows "token missing"

2. **Port 5000** (Direct app.py) ← This was my test instance
   - Has the new code WITH CSRF exempt
   - This is why localhost:5000 worked differently

## The Solution

You need to restart the systemd service to pick up the new code.

### Run These Commands:

```bash
# 1. Restart the systemd service (needs sudo password)
sudo systemctl restart museum-system

# 2. Check it's running
sudo systemctl status museum-system

# 3. Verify it's on port 8000
ss -tlnp | grep 8000
```

### After Restart:

1. **CLEAR YOUR BROWSER COOKIES** (or use Incognito mode)
2. Go to: `http://192.168.144.48/login`
3. Login with:
   - Email: `admin`
   - Password: `admin123`

## What I Fixed in the Code:

1. ✅ Added `.env` loading (app.py:22-24)
2. ✅ Fixed Session/CSRF initialization order (app.py:84-85)
3. ✅ Temporarily exempted login from CSRF (app.py:1730)
4. ✅ Added SESSION_FILE_DIR config (config.py:26)
5. ✅ Added CSRF tokens to all 29 templates

## If It Still Doesn't Work:

Check the logs:
```bash
sudo journalctl -u museum-system -n 50
```

Look for any error messages.

---

**I cannot run `sudo` commands, so you need to restart the service manually.**

Run:
```bash
sudo systemctl restart museum-system
```

Then test login at http://192.168.144.48/login
