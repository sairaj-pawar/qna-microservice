# Async Document Q&A Microservice with Mock LLM

A Python backend microservice built with FastAPI, PostgreSQL, and async programming that allows users to upload documents, ask questions, and receive simulated LLM-generated answers asynchronously.

## Features

- Upload and retrieve documents
- Submit questions about specific documents
- Simulate LLM processing with background tasks (async)
- Monitor question processing status
- RESTful API endpoints

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy
- **Async Processing**: asyncio
- **Validation**: Pydantic

## Prerequisites

- Python 3.8+
- PostgreSQL

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd async-document-qa-microservice
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL and update `.env` file (see `.env.example`):
- Create a database (e.g., `document_qa`)
- Set correct credentials in `.env`

5. Run migrations:
```bash
alembic upgrade head
```

6. Start the application:
```bash
uvicorn app.main:app --reload
```

7. Open API docs in your browser: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/documents/` | POST | Upload a document |
| `/documents/{id}` | GET | Retrieve a document |
| `/questions/{document_id}/question` | POST | Submit a question about a document |
| `/questions/{id}` | GET | Get question status and answer |

### Example Usage

#### 1. Upload a Document
```bash
curl -X POST "http://localhost:8000/documents/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Document",
    "content": "This is the content of the document that will be used for Q&A."
  }'
```

#### 2. Ask a Question
```bash
curl -X POST "http://localhost:8000/questions/1/question" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this document about?"
  }'
```

#### 3. Check Question Status
```bash
curl -X GET "http://localhost:8000/questions/1"
```

#### 4. Retrieve a Document
```bash
curl -X GET "http://localhost:8000/documents/1"
```

## Project Structure

```
async-document-qa-microservice/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection
│   ├── models/                 # SQLAlchemy models
│   │   ├── document.py
│   │   └── question.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── document.py
│   │   └── question.py
│   ├── services/               # Business logic
│   │   ├── document_service.py
│   │   └── question_service.py
│   └── api/                    # API routes
│       ├── documents.py
│       └── questions.py
├── alembic/                    # Database migrations
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and update the values:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/document_qa
SECRET_KEY=your-secret-key
DEBUG=True
```

---
For any questions or issues, please open an issue on GitHub. 