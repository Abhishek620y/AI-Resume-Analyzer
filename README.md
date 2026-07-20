# 🚀 AI Resume Analyzer

![React](https://img.shields.io/badge/React-19-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Python](https://img.shields.io/badge/Python-3.11-yellow)
![License](https://img.shields.io/badge/License-MIT-red)
![Deployment](https://img.shields.io/badge/Deployment-Vercel%20%2B%20Render-success)


# 🚀 AI Resume Analyzer

An AI-powered Resume Analyzer and ATS Scoring System built using **React**, **FastAPI**, and **SQLite/PostgreSQL**. The application helps job seekers improve their resumes by analyzing ATS compatibility, extracting skills, matching resumes with job descriptions, and providing AI-powered suggestions.

---

## 🌐 Live Demo

### 🔗 LIVE DEMO (Vercel)
https://ai-resume-analyzer-4uj6g56pm.vercel.app

### 🔗 Backend API (Render)
https://ai-resume-analyzer-c35a.onrender.com

### 📖 API Documentation (Swagger UI)
https://ai-resume-analyzer-c35a.onrender.com/docs

---

## ✨ Features

- 🔐 User Authentication (Candidate & Recruiter)
- 📄 Resume Upload (PDF & DOCX)
- 🤖 AI Resume Analysis
- 📊 ATS Score Calculation
- 💼 Job Description Matching
- 🎯 Resume Match Percentage
- 🧠 Skill Extraction
- ⚡ Missing Skills Detection
- 💡 AI Resume Improvement Suggestions
- 📈 Recruiter Dashboard
- 📁 Resume History
- 🔎 Resume Search

---

## 🛠 Tech Stack

### Frontend
- React.js
- Vite
- Tailwind CSS
- Axios

### Backend
- FastAPI
- SQLAlchemy
- JWT Authentication
- Pydantic

### Database
- SQLite (Development)
- PostgreSQL (Production Ready)

### AI
- OpenAI API
- Google Gemini API
- Mock AI Provider

### Resume Parsing
- PyMuPDF
- pdfplumber
- python-docx

---

## 📸 Screenshots

> Add screenshots here

- Login Page
- Dashboard
- Resume Analysis
- ATS Score
- Job Match Results

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/Abhishek620y/AI-Resume-Analyzer.git
```

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## ⚙ Environment Variables

Backend

```env
DATABASE_URL=sqlite:///./database/app.db

JWT_SECRET_KEY=your-secret-key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

AI_PROVIDER=mock

OPENAI_API_KEY=

GEMINI_API_KEY=
```

Frontend

```env
VITE_API_URL=https://ai-resume-analyzer-c35a.onrender.com/api
```

---

## 📚 API Documentation

Swagger UI

https://ai-resume-analyzer-c35a.onrender.com/docs

---

## 📂 Project Structure

```
AI-Resume-Analyzer
│
├── frontend
│
├── backend
│   ├── app
│   ├── database
│   ├── requirements.txt
│   └── .env.example
│
└── uploads
```

---

## 🔮 Future Improvements

- Resume Ranking
- Multiple Resume Comparison
- Interview Question Generator
- AI Resume Builder
- Recruiter Analytics
- Email Notifications
- Export Analysis Report
- Admin Dashboard

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Abhishek Kumar Yadav**

GitHub:
https://github.com/Abhishek620y

LinkedIn:
https://www.linkedin.com/in/abhishek-yadav6205/
