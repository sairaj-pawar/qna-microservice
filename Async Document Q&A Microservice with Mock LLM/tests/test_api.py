import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.database import get_db
from app.models import Document, Question


@pytest.fixture
async def async_client():
    """Create async client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def db_session():
    """Create database session for testing"""
    async for session in get_db():
        yield session


@pytest.mark.asyncio
async def test_health_check(async_client):
    """Test health check endpoint"""
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Async Document Q&A Microservice"


@pytest.mark.asyncio
async def test_root_endpoint(async_client):
    """Test root endpoint"""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Async Document Q&A Microservice"
    assert "docs" in data
    assert "health" in data


@pytest.mark.asyncio
async def test_create_document(async_client):
    """Test document creation"""
    document_data = {
        "title": "Test Document",
        "content": "This is a test document content."
    }
    
    response = await async_client.post("/documents/", json=document_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == document_data["title"]
    assert data["content"] == document_data["content"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_document(async_client):
    """Test document retrieval"""
    # First create a document
    document_data = {
        "title": "Test Document for Retrieval",
        "content": "This is a test document for retrieval."
    }
    
    create_response = await async_client.post("/documents/", json=document_data)
    assert create_response.status_code == 201
    created_doc = create_response.json()
    
    # Then retrieve it
    response = await async_client.get(f"/documents/{created_doc['id']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == created_doc["id"]
    assert data["title"] == document_data["title"]
    assert data["content"] == document_data["content"]


@pytest.mark.asyncio
async def test_get_nonexistent_document(async_client):
    """Test retrieving non-existent document"""
    response = await async_client.get("/documents/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_question(async_client):
    """Test question creation"""
    # First create a document
    document_data = {
        "title": "Test Document for Questions",
        "content": "This is a test document for questions."
    }
    
    create_doc_response = await async_client.post("/documents/", json=document_data)
    assert create_doc_response.status_code == 201
    created_doc = create_doc_response.json()
    
    # Then create a question
    question_data = {
        "question": "What is this document about?"
    }
    
    response = await async_client.post(
        f"/questions/{created_doc['id']}/question",
        json=question_data
    )
    assert response.status_code == 201
    
    data = response.json()
    assert data["question"] == question_data["question"]
    assert data["document_id"] == created_doc["id"]
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_question_status(async_client):
    """Test question status retrieval"""
    # First create a document
    document_data = {
        "title": "Test Document for Question Status",
        "content": "This is a test document for question status."
    }
    
    create_doc_response = await async_client.post("/documents/", json=document_data)
    assert create_doc_response.status_code == 201
    created_doc = create_doc_response.json()
    
    # Then create a question
    question_data = {
        "question": "What is this document about?"
    }
    
    create_q_response = await async_client.post(
        f"/questions/{created_doc['id']}/question",
        json=question_data
    )
    assert create_q_response.status_code == 201
    created_question = create_q_response.json()
    
    # Then check its status
    response = await async_client.get(f"/questions/{created_question['id']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == created_question["id"]
    assert data["question"] == question_data["question"]
    assert data["document_id"] == created_doc["id"]
    assert data["status"] in ["pending", "answered"]


@pytest.mark.asyncio
async def test_create_question_for_nonexistent_document(async_client):
    """Test creating question for non-existent document"""
    question_data = {
        "question": "What is this document about?"
    }
    
    response = await async_client.post("/questions/99999/question", json=question_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_question(async_client):
    """Test retrieving non-existent question"""
    response = await async_client.get("/questions/99999")
    assert response.status_code == 404 