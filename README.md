# I-Grow Discipleship Guide - CMS

An interactive Bible study guide for campus and workplace small groups with content management capabilities.

## Features

- 📖 **Interactive Study Guide** - Engaging reading and reflection sections
- 🔐 **Admin Login** - Secure content editing for authorized users
- 💾 **Persistent Storage** - Weekly content updates that persist
- 🎨 **Beautiful Design** - Lighthouse Tagaytay brand colors
- 📱 **Responsive** - Works on all devices

## Quick Start

### For Regular Users (Viewers)

Simply visit the deployed app URL and navigate through the weekly Bible study material.

### For Editors (Admin)

1. Click the 🔧 button in the bottom-right corner
2. Enter the admin password
3. Edit content in the sidebar
4. Click "Save Changes" to update
5. Logout when done

**Default Password:** `password` (change this before deploying!)

## Deployment

### Deploy to Streamlit Cloud

1. Fork or clone this repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with GitHub
4. Create new app:
   - **Repository:** Your forked repo
   - **Branch:** main
   - **Main file:** `igrow_cms_app.py`
5. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app`

### Change Admin Password

Before deploying, change the default password:

1. Run this Python code to generate a new hash:
```python
import hashlib
password = "YOUR_NEW_PASSWORD"
print(hashlib.sha256(password.encode()).hexdigest())
```

2. Replace line 234 in `igrow_cms_app.py`:
```python
ADMIN_PASSWORD_HASH = "YOUR_NEW_HASH_HERE"
```

3. Commit and push the change

## Weekly Content Updates

1. Log in as admin
2. Update content fields in the sidebar:
   - Main title and topic
   - Ice breaker question
   - Big idea
   - Scripture passage
   - 3 main sections
   - Key insight
   - Action step
3. Click "Save Changes"
4. Content updates immediately for all viewers
5. Changes persist in `igrow_content.json`

## Files

- `igrow_cms_app.py` - Main application
- `igrow_content.json` - Content storage (tracked in Git)
- `requirements.txt` - Python dependencies
- `.gitignore` - Files to exclude from Git

## Technology

- **Streamlit** - Web framework
- **Python** - Backend language
- **JSON** - Content storage
- **SHA-256** - Password hashing

## Security Notes

- Password is hashed with SHA-256
- Session-based authentication
- Admin button is subtle but accessible
- Content file is version-controlled for backup

## Support

For issues or questions, contact your Bible study group administrator.

---

Built with ❤️ for Lighthouse Tagaytay small groups
