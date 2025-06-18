# <img src="assets/img/logo_no_back.png" alt="Media Finder logo" width="120"/>  Media Finder

Media Finder is an AI-powered platform that helps you discover movies and games faster.  
It combines Retrieval-Augmented Generation (RAG), computer-vision poster search, and a modern social UI so you can:

* Ask natural-language questions about thousands of titles
* Upload a poster and get instant information or similar recommendations
* Keep track of reviews and see what your friends are watching or playing

---

## 🚀 Quick start

```bash
# 1  Clone
$ git clone https://github.com/<your-username>/Dauphine_2425.git
$ cd Dauphine_2425

# 2  Create & activate a virtualenv
$ python3 -m venv venv && source venv/bin/activate  # macOS/Linux
#  (Windows) venv\Scripts\activate

# 3  Install dependencies
$ pip install -r requirements.txt

# 4  Add your Cohere key in a .env file
COHERE_API_KEY="YOUR_API_KEY_HERE"

# 5  Run the full stack (Streamlit + REST + GraphQL)
$ python main.py
```
Visit http://localhost:8501 in your browser.

---

## 🏗️  Architecture snapshot

```
├─ domain/          # Pure business logic & ports      
├─ application/     # Factories / use-case orchestration
├─ infrastructure/  # Adapters (Cohere, ChromaDB, Neo4j…)
├─ web_app/         # Streamlit UI (Home, Chat, Community…)
└─ rest/ & interface/graphql/  # Public APIs
```
* **RAG layer** – `domain/service/rag_service_impl.py`  
  • Sentence-Transformers + ChromaDB (text)  
  • Optional CLIP + ChromaDB (image)  
  • Cohere LLM for answer generation
* **Social layer** – Neo4j via `infrastructure/adapter/neo4j_review_repository.py`

---

## Useful scripts

| Script | Purpose |
|--------|---------|
| `scripts/split_data.py` | Split the full dataset into smaller chunks for fast prototyping |
| `scripts/optimize_rag.py` | Pre-compute embeddings for the entire catalogue |
| `setup_neo4j.py` | (Optional) Launch Neo4j locally and seed sample data |

---

## License
MIT

