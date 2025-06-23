 <p align="center">
  <img src="assets/img/media_finder_logo.png" alt="Media Finder logo" width="250"/> 
</p>

**Media Finder** is an AI-powered platform designed to help you discover movies and games more efficiently.
It leverages Retrieval-Augmented Generation (RAG), computer vision for poster-based search, and a modern social interface to let you:

* Ask natural-language questions about thousands of titles
* Upload a poster to get instant info or recommendations
* See what your friends are watching or playing, and share reviews

## 🚀 Quick start

```bash

git clone https://github.com/<your-username>/Dauphine_2425.git
cd Dauphine_2425

python3 -m venv venv && source venv/bin/activate    # macOS/Linux

pip install -r requirements.txt

# ⚠️ Note: All libraries are external. If you're not using a virtual environment,
# double-check that their versions don't conflict with your global setup.

# Add your Cohere API key to a .env file
COHERE_API_KEY="YOUR_API_KEY_HERE"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="your_username"
NEO4J_PASSWORD="your_password"

python main.py
```

Once started, open [http://localhost:8501](http://localhost:8501) in your browser.

## ⚙️ Required GraphQL & Neo4j Setup

* An instance of **GraphQL** should be running to support metadata queries.
* Credentials for the **Neo4j database** (URI, username, password) must be defined in your `.env` file.
* You must **populate the graph database** with media and user data for the social features to work.

  * Use `setup_neo4j.py` or your own Cypher scripts to seed the graph.

## 🧠 Neo4j Database Initialization (.cypher)

To make the application work correctly, the Neo4j database must be populated with a specific structure. Below is a list of required **nodes**, **relationships**, and **properties**.

---

### 📦 Node Types

#### `User`
Represents an application user.

| Property     | Type   | Description                            |
|--------------|--------|----------------------------------------|
| `name`       | String | The user’s name (e.g., `"Alice"`)      |
| `avatarUrl`  | String | URL to the user's profile picture      |

#### `Content`
Represents cultural content (movie, series, or video game).

| Property     | Type   | Description                                       |
|--------------|--------|---------------------------------------------------|
| `title`      | String | Title of the content                              |
| `type`       | String | `"movie"` / `"series"` / `"game"`                |
| `platform`   | String | Platform (e.g., `"Netflix"`, `"PlayStation"`)     |
| `posterUrl`  | String | URL to the poster image (displayed on homepage)  |

#### `Review`
Represents a review written by a user for a specific content.

| Property     | Type     | Description                        |
|--------------|----------|------------------------------------|
| `rating`     | Integer  | Rating out of 10                   |
| `comment`    | String   | User's comment                     |
| `createdAt`  | DateTime | Timestamp of the review creation   |

---

### 🔗 Relationship Types

#### `(:User)-[:FRIENDS_WITH]->(:User)`
Defines a friendship between two users.

#### `(:User)-[:WROTE]->(:Review)`
Links a user to the review they wrote.

#### `(:Review)-[:REVIEWS]->(:Content)`
Links a review to the content it is about.

## 🏗️ Project hexagonal architecture

```
├─ domain/          # Core business logic and interface definitions
├─ application/     # Service wiring and factory methods
├─ infrastructure/  # External adapters (Cohere, ChromaDB, Neo4j, etc.)
├─ web_app/         # Streamlit UI: Home, Chat, Community, etc.
└─ rest/ & interface/graphql/  # Public API layers (REST + GraphQL)
```

### ✳️ Key components

* **RAG layer** – `domain/service/rag_service_impl.py`

  * Sentence-Transformers + ChromaDB for text search
  * Optional CLIP + ChromaDB for poster-based search
  * Cohere LLM for generating intelligent responses

* **Social layer** – Powered by Neo4j

  * See `infrastructure/adapter/neo4j_review_repository.py` for graph-based reviews and friendships


## 🔧 Useful Scripts

| Script                    | Description                                                             |
| ------------------------- | ----------------------------------------------------------------------- |
| `scripts/split_data.py`   | Splits the full dataset into smaller chunks for quicker development     |
| `scripts/optimize_rag.py` | Pre-generates embeddings to speed up runtime performance                |
| `setup_neo4j.py`          | (Optional) Sets up a local Neo4j instance and seeds it with sample data |


