# 🧠 LearnMate API

> Backend for a personalized study platform powered by Artificial Intelligence.

**LearnMate** is an application that leverages **Generative AI (LLMs)** and **Vector Search (RAG)** to create personalized learning paths, automatic summaries, and quizzes based on user-consumed content.

## 🛠️ Tech Stack

This project was built focusing on performance and modern architecture:

- **Language:** Python 3.10+
- **Web Framework:** FastAPI (ASGI)
- **Server:** Uvicorn
- **Database (Planned):** PostgreSQL & Redis
- **AI & Embeddings:** OpenAI API
- **Architecture:** RESTful API

## 🚀 Features (Roadmap)

- [x] **Initial Setup:** FastAPI environment configuration and Health Check.
- [x] **LLM Integration:** Automatic text summarization via OpenAI.
- [ ] **Database:** Content and user persistence (PostgreSQL).
- [ ] **Vector Search:** Implementation of Embeddings for semantic content recommendation.
- [ ] **Background Tasks:** Asynchronous processing for long texts.

## 📦 How to Run Locally

Follow the steps below to start the API on your machine:

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/learnmate-backend.git](https://github.com/YOUR_USERNAME/learnmate-backend.git)
cd learnmate-backend

2. Create and activate virtual environment
# Linux/Mac/WSL
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run the server
uvicorn main:app --reload

The server will be running at: http://127.0.0.1:8000. Access the interactive documentation (Swagger) at: http://127.0.0.1:8000/docs.
```
## 🤝 Contribution
Project developed for study and portfolio purposes. Suggestions are welcome!

Developed by Vinícius Castelhano Mantovani
