from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..services.question_service import QuestionService
from ..services.document_service import DocumentService
from ..schemas.question import QuestionCreate, QuestionResponse

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/{document_id}/question", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    document_id: int,
    question_data: QuestionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Submit a question about a specific document"""
    try:
        # First check if document exists
        doc_service = DocumentService(db)
        document_exists = await doc_service.document_exists(document_id)
        
        if not document_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found"
            )
        
        # Create question and start async processing
        service = QuestionService(db)
        question = await service.create_question(document_id, question_data)
        
        return question
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create question"
        )


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get question status and answer"""
    try:
        service = QuestionService(db)
        question = await service.get_question(question_id)
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found"
            )
        
        return question
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve question"
        ) 