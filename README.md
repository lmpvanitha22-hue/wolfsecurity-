# 🛡️ Phishing URL Detector

A permanent public web application that uses two Machine Learning models
(Logistic Regression + Random Forest) to detect phishing URLs in real-time.

---

## 🚀 Deploy to Railway (Free Permanent Public URL)

Follow these steps once to get a live public URL like:
`https://phishing-detector-xxxx.up.railway.app`

---

### Step 1 — Create a GitHub Repository

1. Go to https://github.com and sign in (or create a free account)
2. Click **New repository**
3. Name it `phishing-detector`
4. Set it to **Public**
5. Click **Create repository**

---

### Step 2 — Upload your files to GitHub

Upload these files from `d:\safi` to your GitHub repo:

```
app.py
phishing_detector.py
requirements.txt
Procfile
runtime.txt
railway.json
blacklist.json
templates/
    index.html
static/
    style.css
    app.js
```

You can drag and drop them on the GitHub website, or use Git:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/phishing-detector.git
git push -u origin main
```

---

### Step 3 — Deploy on Railway

1. Go to https://railway.app and sign in with GitHub
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Choose your `phishing-detector` repository
5. Railway auto-detects everything and deploys

**That's it!** Railway will give you a public URL in ~2 minutes.

---

### Step 4 — Get your public URL

1. In Railway dashboard, click your project
2. Click **Settings** → **Domains**
3. Click **Generate Domain**
4. Your URL will be: `https://your-app-name.up.railway.app`

---

## 📁 File Structure

```
phishing-detector/
├── app.py                   ← Local and WSGI entry point
├── phishing_detector.py     ← Flask routes, features, and ML models
├── requirements.txt         ← Python dependencies
├── Procfile                 ← Tells Railway how to start the app
├── runtime.txt              ← Python version
├── railway.json             ← Railway configuration
├── blacklist.json            ← Known-bad domains
├── templates/
│   └── index.html           ← Web UI
└── static/
    ├── style.css            ← Styles
    └── app.js               ← Frontend logic
```

The Logistic Regression and Random Forest models are trained from the sample
URLs in `phishing_detector.py` when the app starts, so separate `.pkl` model
files and a dataset file are not currently required. URL feature extraction is
also defined in that Python file.

---

## ⚙️ Tech Stack

| Component      | Technology                        |
|----------------|-----------------------------------|
| Backend        | Python 3.11 + Flask               |
| ML Models      | scikit-learn (LR + RandomForest)  |
| Web Server     | Gunicorn (production WSGI)        |
| Frontend       | HTML5 + CSS3 + JavaScript         |
| Hosting        | Railway (free tier)               |

---

## 🔗 API Usage

```bash
POST https://your-app.up.railway.app/predict
Content-Type: application/json

{"url": "http://suspicious-site.com"}
```

Response:
```json
{
  "status": "PHISHING",
  "risk_score": 99.7,
  "lr_prob": 99.5,
  "lr_status": "PHISHING",
  "lr_reasons": ["..."],
  "rf_prob": 100.0,
  "rf_status": "PHISHING",
  "rf_reasons": ["..."],
  "reasons": ["..."]
}
```

Submit multiple URLs in one request with a `urls` array (up to 1,000 entries):

```json
{"urls": ["http://suspicious-site.com", "https://www.example.com"]}
```

The response contains a `results` array with one verdict, combined risk score,
Logistic Regression score, and Random Forest score per URL. The web analyzer
accepts up to 1,000 URLs, one per line, and shows each result separately.

`GET /metrics` returns Accuracy, Precision, Recall, and F1-Score for Logistic
Regression and Random Forest, measured with 5-fold stratified cross-validation.
These metrics use the project's 20 synthetic sample URLs and are illustrative,
not representative of production performance.

---

## 💻 Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

---

*For educational & research use only.*
