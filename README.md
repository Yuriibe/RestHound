
# 🐾 RestHound — REST API Enumerator & CORS Analyzer

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.org/)

**RestHound** is a CLI tool for API reconnaissance and security analysis. It discovers RESTful API endpoints, checks HTTP method support, detects CORS misconfigurations, and fingerprints technologies using passive header inspection.

---

## ✨ Features

- 🔍 Discover reachable API endpoints
- 📮 Detect supported HTTP methods (via `OPTIONS`)
- 🚨 Detect insecure CORS behavior
- 🧬 Fingerprint server-side technologies via headers
- ✅ Clean, human-readable CLI summary output

---

![RestHound Demo](assets/restHound.gif)


## 📦 Requirements

- Python 3.12+

Install requirements:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
python resthound.py -u https://httpbin.org -w wordlist.txt
```
To see all available options, use:

```bash
python resthound.py -h
```

---

## 📋 Example Output (Partial)

```text
============================================================
✅ Reachable Endpoints:
============================================================
  • https://httpbin.org/get
  • https://httpbin.org/post

============================================================
🔍 Valid Endpoints with Allowed Methods:
============================================================
  [200] https://httpbin.org/get
      ↳ Allowed Methods: HEAD, OPTIONS, GET
  [200] https://httpbin.org/post
      ↳ Allowed Methods: POST, OPTIONS

============================================================
🚨 CORS Reflection Check:
============================================================
  [!] https://httpbin.org/get
      ↳ Access-Control-Allow-Origin: https://evil.com
      ↳ Access-Control-Allow-Credentials: true

============================================================
🧬 Header Fingerprint Summary:
============================================================
  https://httpbin.org/get
    ↳ Server: gunicorn/19.9.0
    ↳ X-Powered-By: None
```

---

## 🛡️ Disclaimer

This tool is intended for **authorized testing**, research, and educational use only. Do not scan or probe systems without explicit permission.

---
