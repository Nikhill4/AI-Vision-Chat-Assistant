# 🤖 AI Vision Chat Assistant

A professional full-stack web application combining **Image Recognition** and **AI Chatbot** features. Powered by TensorFlow's MobileNetV2 and a rule-based AI assistant.

---

## ✨ Features

- 🖼️ **Image Recognition**: Upload images to get instant AI predictions using MobileNetV2.
- 💬 **AI Chatbot**: Intelligent rule-based assistant for technical questions.
- 🕒 **Analysis History**: Keeps track of your previous image predictions (persisted locally).
- 🌓 **Theme Toggle**: Seamless Dark and Light mode support.
- 🖱️ **Drag & Drop**: Modern, user-friendly file upload interaction.
- ✨ **Glassmorphic UI**: Premium "Midnight & Neon" design with smooth animations.
- 📱 **Responsive Design**: Works perfectly on desktop and mobile.

---

## 🚀 Quick Start

### 1. Setup Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

### 2. Setup Frontend
```powershell
cd frontend\client
npm install
npm start
```

---

## 🏗️ Project Structure

```
AI_Vision_Chat_Assistant/
├── backend/
│   ├── app.py              # Flask server with API endpoints
│   ├── image_model.py      # TensorFlow ML logic
│   ├── chatbot.py          # AI assistant logic
│   └── uploads/            # Temporary storage for analysis
└── frontend/
    └── client/
        ├── src/
        │   ├── App.js      # Main View Container
        │   ├── Chat.js     # AI Chat Component
        │   └── ImageUpload.js # Vision Analysis Component
        └── index.css       # Global Midnight Design System
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/predict` | POST | Analyze uploaded image files |
| `/chat` | POST | Send messages to AI Assistant |
| `/health` | GET | Check backend server status |

---

## 🔧 Troubleshooting

- **Backend Connection**: Ensure Flask is running on `http://localhost:5000`.
- **First Load**: TensorFlow model may take 30-60 seconds to download on first run.
- **Port Conflict**: If port 5000 is occupied, use `netstat -ano | findstr :5000` to find and kill the process.

---

**Last Updated:** February 25, 2026 | **Version:** 3.0 (Professional Redesign)
