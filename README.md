---
# 📄 **README.md — Resume Intelligence Platform**

# 🧠 Resume Intelligence Platform

End-to-end, AI-powered JD–Resume Matching & Ranking System
Built using **FastAPI**, **React**, **FAISS RAG**, **HuggingFace Embeddings**, and **LangChain architecture principles**.
---

## 🚀 Overview

The **Resume Intelligence Platform** automatically evaluates candidate resumes against job descriptions (JD) using:

- 🔍 **RAG (Retrieval-Augmented Generation)**
- ✨ **Semantic similarity scoring**
- 🧩 **Skill keyword overlap**
- 📊 **Experience extraction**
- 🧠 **Adaptive memory** that remembers the best resume per JD and compares new ones
- ⚛️ **React frontend** for user-friendly uploads
- ⚙️ **FastAPI backend**
- 📦 **Docker support**
- ☁️ **CI/CD to AWS EC2 using GitHub Actions & ECR**

It helps recruiters automatically shortlist candidates and compare multiple resumes with a given JD.

---

## 🏗️ Features

### 🔧 Backend (FastAPI)

- PDF text extraction (JD + Resume)
- Chunking + vector embeddings (MiniLM)
- FAISS vector store for RAG retrieval
- Similarity scoring pipeline:

  - Semantic similarity
  - Skill overlap
  - Experience detection
  - Combined suitability score

- In-memory storage that:

  - Saves best resume for each JD
  - Compares new resumes to previous best
  - Maintains history

---

### 🎨 Frontend (React)

- Upload JD PDF
- Upload Resume PDF
- Provide JD name
- Visual JSON output of scoring + verdict
- Handles errors & loading states

---

### ☁️ Deployment

- Multi-stage Dockerfile (React build + FastAPI)
- GitHub Actions CI/CD:

  - Build Docker image
  - Push to AWS ECR
  - SSH deploy to EC2

- Production-ready structure

---

## 📁 Project Structure

```
Resume-Intelligence-Platform/
│
├── app/                         # Backend API
│   ├── main.py                  # FastAPI server
│   ├── rag_utils.py             # PDF → chunks → embeddings
│   ├── scoring.py               # JD-Resume scoring engine
│   ├── memory_store.py          # In-memory candidate tracking
│   ├── schemas.py               # Pydantic response models
│   └── __init__.py
│
├── Client/                      # Frontend React application
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── components/
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── vite.config.js
│
├── Dockerfile                   # Multi-stage build (Node + Python)
├── requirements.txt             # Backend dependencies
├── run.sh                       # FastAPI entrypoint script
└── .github/
    └── workflows/
        └── cicd.yaml           # CI/CD pipeline for AWS
```

---

# ⚙️ Installation & Local Development

## 1️⃣ Clone the Repository

```sh
git clone https://github.com/YOUR_USERNAME/Resume-Intelligence-Platform.git
cd Resume-Intelligence-Platform
```

---

## 2️⃣ Backend Setup

### Install dependencies:

```sh
pip install -r requirements.txt
```

### Start FastAPI server:

```sh
./run.sh
```

or

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend is now running at:

```
http://localhost:8000
```

---

## 3️⃣ Frontend Setup (React)

```
cd Client
npm install
npm run dev
```

Visit:

```
http://localhost:5173
```

---

# 🧪 API Usage

## Endpoint:

### `POST /evaluate`

Uploads JD PDF + Resume PDF + JD Name.

Example using `curl`:

```sh
curl -X POST http://localhost:8000/evaluate \
  -F "jd_name=python_dev" \
  -F "jd_file=@JD.pdf" \
  -F "resume_file=@candidate_resume.pdf"
```

---

# 🧠 Scoring Metrics

| Metric                  | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| **Semantic Similarity** | Vector-based similarity between JD & resume            |
| **Skill Overlap**       | Keyword intersection between JD skills & resume skills |
| **Experience Score**    | Years of experience detection                          |
| **Suitability Score**   | Combined final score (0–100)                           |

The system automatically determines if a resume is:

- Better than previous best
- Worse
- Equal
- First for this JD

---

# 📦 Docker Build & Run

Build:

```sh
docker build -t resume-intel .
```

Run:

```sh
docker run -p 8000:8000 resume-intel
```

---

# ☁️ CI/CD Pipeline (GitHub → AWS → EC2)

- Push to `main`
- GitHub Actions builds Docker image
- Pushes to AWS ECR
- SSH into EC2
- Pull latest image
- Restart container

Secrets Needed:

```
AWS_ACCESS_KEY
AWS_SECRET_KEY
EC2_HOST
EC2_SSH_PRIVATE_KEY
```

---

# 🚀 Roadmap

- Add GPT-4o scoring engine
- Multi-resume batch comparison dashboard
- Cloud memory with Redis or DynamoDB
- JD categorization model
- Recruiter admin dashboard
- Generate interview questions automatically

---

# 🤝 Contributing

Pull requests are welcome!
To contribute:

```
git checkout -b feature-branch
git commit -m "Add awesome feature"
git push origin feature-branch
```

---

# ⭐ Support

If you like this project:

✔ Star the repo
✔ Fork it
✔ Share it

---
