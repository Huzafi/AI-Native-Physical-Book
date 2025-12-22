# Quickstart Guide: AI-Native Book with Docusaurus

## Prerequisites
- Node.js 18+
- Python 3.11+
- npm or yarn
- Docker (for local backend services)

## Setup Instructions

### 1. Clone and Initialize Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Setup Frontend (Docusaurus)
```bash
cd website
npm install
```

### 3. Setup Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Environment
Create `.env` files in both directories with appropriate settings:

**website/.env:**
```
REACT_APP_API_URL=http://localhost:8000
```

**backend/.env:**
```
DATABASE_URL=postgresql://user:password@localhost:5432/ai_book
QDRANT_URL=http://localhost:6333
```

### 5. Start Services

#### Option A: Development Mode (separate terminals)
```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start frontend
cd website
npm start
```

#### Option B: Using Docker
```bash
docker-compose up --build
```

### 6. Add Book Content
1. Create MDX files in `website/docs/` directory following the chapter structure
2. Update `website/sidebars.js` to include new content in navigation
3. Run `npm run build` to rebuild the site

### 7. Index Content for Search and AI
```bash
# After adding new content, run the indexing script
cd backend
python -m scripts.index_content
```

## Running Tests
```bash
# Frontend tests
cd website
npm test

# Backend tests
cd backend
pytest
```

## Deployment
The frontend (Docusaurus) builds to static files that can be hosted on any static hosting service. The backend API can be deployed to any Python-compatible hosting platform.

For a complete deployment setup, see the deployment documentation in the `docs/deployment/` directory.