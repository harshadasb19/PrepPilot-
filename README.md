# 🎯 PrepPilot — AI-Powered Interview Trainer

<div align="center">

![PrepPilot Banner](https://img.shields.io/badge/PrepPilot-AI%20Interview%20Trainer-0f62fe?style=for-the-badge&logo=ibm&logoColor=white)
![IBM SkillsBuild](https://img.shields.io/badge/IBM-SkillsBuild%202025-054ada?style=for-the-badge&logo=ibm&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-24a148?style=for-the-badge)

**An AI-powered Interview Trainer built on IBM enterprise technology.**  
Personalised question generation · Model answers · Real-time AI feedback · Readiness scoring.

</div>

---

## 📌 Overview

PrepPilot is an AI-powered Interview Trainer developed as part of the **IBM SkillsBuild Internship 2025** program.

It leverages a fully deployed AI agent in **IBM watsonx Orchestrate** — backed by **IBM watsonx.ai foundation models**, a **RAG pipeline** reading from **IBM Cloud Object Storage** — to deliver hyper-personalised interview preparation for any job role, company, or experience level.

> **The AI agent is fully created, tested, and deployed in IBM watsonx Orchestrate.**  
> This repository contains only the **Streamlit frontend** that communicates with the agent.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│                       (app.py)                          │
│   Candidate Form → Interview Config → Results Display   │
└───────────────────────────┬─────────────────────────────┘
                            │  HTTPS / REST
                            ▼
┌─────────────────────────────────────────────────────────┐
│              IBM watsonx Orchestrate Agent               │
│         (Deployed · Tested · Production-Ready)           │
└──────┬──────────────────────────┬───────────────────────┘
       │                          │
       ▼                          ▼
┌──────────────┐        ┌──────────────────────────────┐
│ IBM watsonx  │        │  IBM Cloud Object Storage    │
│    .ai LLM   │        │  (Resume + Knowledge Base)   │
│  (Granite /  │        │                              │
│   Llama 3)   │        │  ┌──────────────────────┐    │
└──────────────┘        │  │   RAG Retriever       │    │
                        │  │  (Vector + Keyword)   │    │
                        │  └──────────────────────┘    │
                        └──────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧑‍💼 Candidate Profile | Full Name, Email, Job Role, Company, Experience, Skills |
| 📄 Resume Upload | Upload PDF/DOCX — parsed by AI for personalised questions |
| 🎯 Interview Types | Technical, HR, Behavioral, Mixed |
| 🔧 Technical Questions | Domain-specific questions tailored to the role and skills |
| 🤝 HR Questions | Culture-fit and motivation-based questions |
| 💬 Behavioral Questions | STAR-format situational questions |
| 📖 Model Answers | AI-crafted reference answers for common questions |
| 💡 Preparation Tips | Expert strategies personalised to the target company |
| 📊 Interview Feedback | Per-dimension score bars (Technical, Communication, etc.) |
| 🏆 Readiness Score | Single score (0–100) with coaching recommendation |

---

## 🚀 Quick Start

### Prerequisites

- Python **3.10** or higher
- `pip` package manager
- (Optional) IBM watsonx Orchestrate agent credentials

### 1 — Clone the repository

```bash
git clone https://github.com/your-username/preppilot.git
cd preppilot
```

### 2 — Create a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Configure environment variables

```bash
cp .env.example .env
```

Open `.env` in your editor and fill in your IBM credentials (see [Configuration](#configuration) below).  
**The app runs in full demo mode if credentials are left blank.**

### 5 — Run the application

```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**.

---

## ⚙️ Configuration

All credentials are managed via `.env`. Copy `.env.example` → `.env` and populate:

| Variable | Description | Required |
|---|---|---|
| `ORCHESTRATE_URL` | Full URL of the deployed Orchestrate agent endpoint | For live mode |
| `ORCHESTRATE_API_KEY` | API key from IBM watsonx Orchestrate | For live mode |
| `WATSONX_API_URL` | Regional URL (e.g. `https://us-south.ml.cloud.ibm.com`) | Optional |
| `WATSONX_API_KEY` | IBM Cloud IAM API key | Optional |
| `WATSONX_PROJECT_ID` | watsonx.ai project ID | Optional |
| `WATSONX_SPACE_ID` | watsonx.ai deployment space ID | Optional |
| `COS_API_KEY` | IBM Cloud Object Storage API key | Optional |
| `COS_SERVICE_INSTANCE_ID` | COS service CRN | Optional |
| `COS_ENDPOINT` | COS regional endpoint | Optional |
| `COS_BUCKET_NAME` | Bucket used for resume/knowledge storage | Optional |
| `DEMO_MODE` | `true` to force demo data | Optional |

> **Security note:** `.env` is in `.gitignore`. Never commit real credentials.

---

## 🗂️ Project Structure

```
preppilot/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Your local credentials (git-ignored)
├── .gitignore              # Git ignore rules
│
├── assets/                 # Static assets (logo, icons)
│   └── logo.png
│
└── README.md               # This file
```

---

## 🌐 Deployment

### Option A — Streamlit Community Cloud (Recommended for demos)

1. Push your code to a **public or private GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select your repository → set **Main file path** to `app.py`.
4. Under **Advanced settings → Secrets**, paste the contents of your `.env` file.
5. Click **Deploy** — your app is live at `https://your-app.streamlit.app`.

### Option B — IBM Code Engine (IBM Cloud Serverless)

```bash
# 1. Install IBM Cloud CLI + Code Engine plugin
ibmcloud plugin install code-engine

# 2. Target your resource group and region
ibmcloud target -r us-south -g Default

# 3. Create or select a Code Engine project
ibmcloud ce project select --name preppilot

# 4. Deploy the application
ibmcloud ce app create \
  --name preppilot \
  --image icr.io/your-namespace/preppilot:latest \
  --port 8501 \
  --env-from-secret preppilot-secrets

# Or deploy directly from source (Buildpack)
ibmcloud ce app create \
  --name preppilot \
  --build-source . \
  --port 8501
```

### Option C — Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

```bash
docker build -t preppilot .
docker run -p 8501:8501 --env-file .env preppilot
```

### Option D — IBM Kubernetes Service (IKS)

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: preppilot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: preppilot
  template:
    metadata:
      labels:
        app: preppilot
    spec:
      containers:
        - name: preppilot
          image: icr.io/your-namespace/preppilot:latest
          ports:
            - containerPort: 8501
          envFrom:
            - secretRef:
                name: preppilot-secrets
---
apiVersion: v1
kind: Service
metadata:
  name: preppilot-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8501
  selector:
    app: preppilot
```

```bash
kubectl apply -f k8s-deployment.yaml
```

---

## 🧩 API Integration

The frontend calls your deployed Orchestrate agent via a single POST request:

```python
POST {ORCHESTRATE_URL}
Authorization: Bearer {ORCHESTRATE_API_KEY}
Content-Type: application/json

{
  "candidate": {
    "full_name": "Sarah Johnson",
    "email": "sarah@email.com",
    "job_role": "Data Scientist",
    "target_company": "IBM",
    "experience_level": "Mid-Level (2–5 years)",
    "skills": "Python, ML, SQL",
    "resume_uploaded": true,
    "interview_type": "Mixed",
    "num_questions": 5
  }
}
```

**Expected response shape:**

```json
{
  "technical_questions":  ["Q1…", "Q2…"],
  "hr_questions":         ["Q1…", "Q2…"],
  "behavioral_questions": ["Q1…", "Q2…"],
  "model_answers":        {"Tell me about yourself": "…"},
  "preparation_tips":     [["💡", "Tip text…"]],
  "feedback_items":       [["Technical Depth", 88, "#0f62fe"]],
  "readiness_score":      87,
  "score_color":          "#24a148",
  "score_label":          "Excellent",
  "generated_at":         "June 01, 2025 · 10:30 AM"
}
```

---

## 🎨 UI Theme

PrepPilot uses a custom **IBM Carbon Design System**-inspired theme:

| Token | Hex | Usage |
|---|---|---|
| IBM Blue | `#0f62fe` | Primary actions, highlights |
| IBM Blue Dark | `#0043ce` | Hover states |
| IBM Teal | `#009d9a` | Secondary accents |
| IBM Green | `#24a148` | Success states, readiness |
| IBM Purple | `#8a3ffc` | Model answers |
| IBM Yellow | `#f1c21b` | Warnings, behavioral |
| IBM Gray 900 | `#161616` | Body text |

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | 1.35.0 | Frontend framework |
| `python-dotenv` | 1.0.1 | Environment variable loading |
| `requests` | 2.32.3 | HTTP calls to Orchestrate agent |
| `ibm-watsonx-ai` | 1.1.2 | Direct watsonx.ai SDK (optional) |
| `ibm-cos-sdk` | 2.13.6 | IBM Cloud Object Storage |
| `PyPDF2` | 3.0.1 | PDF resume parsing |
| `python-docx` | 1.1.2 | DOCX resume parsing |
| `pandas` | 2.2.2 | Data manipulation |
| `numpy` | 1.26.4 | Numerical operations |
| `Pillow` | 10.3.0 | Image handling |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **IBM SkillsBuild** — for the internship opportunity and cloud resources
- **IBM watsonx** — for the enterprise AI platform
- **Streamlit** — for the rapid UI framework
- **IBM Carbon Design System** — for design inspiration

---

<div align="center">

**PrepPilot** — Built with ❤️ for IBM SkillsBuild Internship 2025

[![IBM](https://img.shields.io/badge/IBM-SkillsBuild-054ada?logo=ibm&logoColor=white)](https://skillsbuild.org)
[![watsonx](https://img.shields.io/badge/IBM-watsonx-8a3ffc?logo=ibm&logoColor=white)](https://www.ibm.com/watsonx)

</div>
