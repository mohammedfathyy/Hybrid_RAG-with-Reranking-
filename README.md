# 🧠 RAG App

A production-ready **Retrieval-Augmented Generation (RAG)** application built with FastAPI, Streamlit, Pinecone, and Google Gemini. Upload your documents, index them with state-of-the-art embeddings, and chat with them using hybrid retrieval + cross-encoder reranking.

---

## ✨ Features

| Feature | Details |
|---|---|
| 📤 **Document Upload** | Upload PDF & TXT files (up to 10 MB each) via drag-and-drop |
| ⚙️ **Smart Chunking** | Recursive character splitting with configurable chunk size & overlap |
| 🔍 **Hybrid Retrieval** | Dense (Pinecone) + Sparse (BM25) retrieval combined via `EnsembleRetriever` |
| 🏆 **Cross-Encoder Reranking** | HuggingFace cross-encoder reranks top candidates for precision |
| 🤖 **Gemini 2.5 Flash LLM** | Answers grounded strictly in your documents |
| 🎨 **Streamlit UI** | Beautiful dark-mode chat interface with real-time status indicators |
| 🗑️ **Data Management** | One-click wipe of all files + Pinecone index vectors |

---

## 🏗️ Architecture

```
RAG_APP/
├── streamlit.py            ← Streamlit frontend (this file)
└── src/
    ├── main.py             ← FastAPI app + model initialisation (lifespan)
    ├── .env                ← API keys (never commit!)
    ├── .env.example        ← Template for .env
    ├── requirements.txt    ← Python dependencies
    ├── saved_data/         ← Uploaded files are stored here temporarily
    ├── routes/
    │   ├── data.py         ← POST /upload
    │   ├── process.py      ← GET  /process
    │   ├── ask.py          ← GET  /ask?question=...
    │   └── delete.py       ← DELETE /delete
    ├── controller/
    │   ├── DataController.py           ← File validation
    │   ├── ProcessController.py        ← Chunking + Pinecone upsert (batched)
    │   ├── Retrieve_AskController.py   ← Hybrid retriever + QA chain
    │   └── DeleteController.py         ← File + index cleanup
    ├── assets/
    │   └── utils.py        ← Shared vectorstore singleton
    ├── models/
    │   └── reranker/       ← Local HuggingFace cross-encoder weights
    └── helpers/
        └── config.py       ← (reserved for future config helpers)
```

### Request Flow

```
User Question
     │
     ▼
Streamlit UI  ──HTTP GET /ask──▶  FastAPI
                                     │
                          ┌──────────┴──────────┐
                          ▼                     ▼
                  Dense Retriever          BM25 Retriever
                  (Pinecone k=5)           (BM25 k=5)
                          └──────────┬──────────┘
                                     ▼
                            EnsembleRetriever
                            (0.7 dense / 0.3 sparse)
                                     │
                                     ▼
                          CrossEncoderReranker (top 3)
                                     │
                                     ▼
                          Gemini 2.5 Flash (answer)
                                     │
                                     ▼
                              Streamlit Chat UI
```

---

## 🚀 Quick Start

### 1 · Prerequisites

- Python 3.10+
- A [Pinecone](https://www.pinecone.io/) account (free tier works)
- A [Google AI Studio](https://aistudio.google.com/) API key (for Gemini embeddings + LLM)

### 2 · Clone & Install

```bash
git clone <your-repo-url>
cd RAG_APP

# Install all dependencies
pip install -r src/requirements.txt
pip install streamlit
```

### 3 · Configure Environment

```bash
cp src/.env.example src/.env
```

Edit `src/.env`:

```env
PINECONE_API_KEY=your_pinecone_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 4 · Download the Reranker Model

The app uses a local cross-encoder for reranking. Save it to `src/models/reranker/`:

```python
# Run once: save_model.py
# python src/save_model.py
```

### 5 · Start the Backend

```bash
cd src
uvicorn main:app --reload --port 8000
```

The FastAPI docs will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 6 · Start the Streamlit Frontend

Open a **second terminal** from the project root:

```bash
streamlit run streamlit.py
```

The UI will open at [http://localhost:8501](http://localhost:8501).

---

## 🖥️ Using the App

| Step | Action |
|---|---|
| **1** | Go to **📄 Documents** → upload one or more PDF/TXT files |
| **2** | Click **⬆️ Upload to Server** to persist them on the backend |
| **3** | Click **🚀 Process Documents** to chunk & index into Pinecone |
| **4** | Switch to **💬 Chat** and ask anything about your documents |
| **5** | (Optional) Go to **⚙️ Settings → Danger Zone** to wipe all data |

---

## 🔌 API Reference

All endpoints are served by FastAPI on `http://127.0.0.1:8000`.

| Method | Path | Description |
|---|---|---|
| `POST` | `/upload` | Upload a file (multipart/form-data, field: `file`) |
| `GET` | `/process` | Chunk all saved files and upsert to Pinecone |
| `GET` | `/ask?question=...` | Ask a question; returns the LLM answer as plain text |
| `DELETE` | `/delete` | Delete all saved files and wipe the Pinecone index |

---

## ⚙️ Configuration

| Parameter | Location | Default | Description |
|---|---|---|---|
| `index_name` | `main.py` | `rag-app` | Pinecone index name |
| `dimension` | `main.py` | `3072` | Embedding dimension (Gemini `gemini-embedding-001`) |
| `chunk_size` | `ProcessController.py` | `500` | Tokens per chunk |
| `chunk_overlap` | `ProcessController.py` | `50` | Overlap between chunks |
| `dense k` | `Retrieve_AskController.py` | `5` | Dense retriever candidates |
| `sparse k` | `Retrieve_AskController.py` | `5` | BM25 retriever candidates |
| `top_n` | `Retrieve_AskController.py` | `3` | Reranker final documents |
| `temperature` | `main.py` | `0.3` | LLM temperature |
| `BATCH_SIZE` | `ProcessController.py` | `50` | Upsert batch size |

---

## 🛠️ Tech Stack

- **FastAPI** — async REST backend
- **Streamlit** — interactive frontend UI
- **LangChain** — orchestration (loaders, splitters, chains, retrievers)
- **Pinecone** — managed vector database
- **Google Gemini** — embeddings (`gemini-embedding-001`) + LLM (`gemini-2.5-flash`)
- **HuggingFace** — cross-encoder reranker (local)
- **BM25** — sparse keyword retrieval

---

## 📝 License

MIT — feel free to use, modify, and distribute.
