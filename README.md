# 🤖 RAGbot: Retrieval-Augmented Generation Chatbot

RAGbot is a modern, web-based chatbot that combines the power of Large Language Models (LLMs) with real-time information retrieval. Built with Python, Flask, LangChain, and MongoDB, RAGbot can answer questions using both its own knowledge and up-to-date information from curated web sources.

---

## ✨ Features

- **Retrieval-Augmented Generation (RAG):** Combines LLM reasoning with document retrieval for accurate, context-rich answers.
- **Modern Web UI:** Clean, responsive interface built with Flask and custom CSS.
- **MongoDB Vector Search:** Stores and retrieves document embeddings for fast, relevant search.
- **Multi-source Routing:** Answers questions using either a vector database or Wikipedia, depending on the query.
- **Easy Customization:** Add your own documents or data sources for domain-specific Q&A.
- **No OpenAI Key Required:** Uses Groq LLMs by default for open, accessible deployment.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the project root with the following:
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=ragbot_db
MONGODB_COLLECTION=ragbot_vectors
GROQ_API_KEY=your-groq-api-key
```

### 4. Run the app
```bash
python RAGbot/ragbot_flask.py
```

### 5. Open your browser
Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to chat with RAGbot!

---

## 🛠️ Tech Stack
- Python, Flask
- LangChain, LangGraph
- MongoDB (Vector Search)
- Groq LLMs
- HTML/CSS (custom, modern UI)

---

## 📂 Project Structure
```
RAGbot/
  ├── RAGbot/
  │     ├── ragbot.py           # Core backend logic
  │     └── ragbot_flask.py     # Flask web UI
  ├── requirements.txt
  └── README.md
```

---

## 📝 License

MIT License

---

## 🙋‍♂️ Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📣 Acknowledgements
- [LangChain](https://github.com/langchain-ai/langchain)
- [Groq](https://groq.com/)
- [MongoDB](https://www.mongodb.com/)
- [Flask](https://flask.palletsprojects.com/)

---

Enjoy building with RAGbot! 🚀 