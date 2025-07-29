from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import asyncio

from ..models.question import Question, QuestionStatus
from ..models.document import Document
from ..schemas.question import QuestionCreate, QuestionResponse


class QuestionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_question(self, document_id: int, question_data: QuestionCreate) -> QuestionResponse:
        """Create a new question and start async processing"""
        try:
            # Check if document exists
            doc_query = select(Document).where(Document.id == document_id)
            doc_result = await self.db.execute(doc_query)
            document = doc_result.scalar_one_or_none()
            
            if not document:
                raise ValueError(f"Document with ID {document_id} not found")
            
            # Create question
            question = Question(
                document_id=document_id,
                question=question_data.question,
                status=QuestionStatus.PENDING
            )
            self.db.add(question)
            await self.db.commit()
            await self.db.refresh(question)
            
            # Start async processing
            asyncio.create_task(self._process_question_async(question.id))
            
            return QuestionResponse.from_orm(question)
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def get_question(self, question_id: int) -> Optional[QuestionResponse]:
        """Get a question by ID"""
        try:
            query = select(Question).where(Question.id == question_id)
            result = await self.db.execute(query)
            question = result.scalar_one_or_none()
            
            if question:
                return QuestionResponse.from_orm(question)
            else:
                return None
        except Exception as e:
            raise
    
    async def get_questions_by_document(self, document_id: int) -> List[QuestionResponse]:
        """Get all questions for a document"""
        try:
            query = select(Question).where(Question.document_id == document_id)
            result = await self.db.execute(query)
            questions = result.scalars().all()
            
            return [QuestionResponse.from_orm(q) for q in questions]
        except Exception as e:
            raise
    
    async def _process_question_async(self, question_id: int):
        """Simulate async LLM processing"""
        try:
            # Simulate processing time (5 seconds as per requirements)
            await asyncio.sleep(5)
            
            # Get the question
            query = select(Question).where(Question.id == question_id)
            result = await self.db.execute(query)
            question = result.scalar_one_or_none()
            
            if question:
                # Generate mock answer
                mock_answer = f"This is a generated answer to your question: {question.question}"
                
                # Update question with answer
                question.answer = mock_answer
                question.status = QuestionStatus.ANSWERED
                
                await self.db.commit()
            else:
                # Try to update status to indicate error
                try:
                    query = select(Question).where(Question.id == question_id)
                    result = await self.db.execute(query)
                    question = result.scalar_one_or_none()
                    if question:
                        question.status = QuestionStatus.PENDING  # Keep as pending on error
                        await self.db.commit()
                except Exception as update_error:
                    pass
                
        except Exception as e:
            # Try to update status to indicate error
            try:
                query = select(Question).where(Question.id == question_id)
                result = await self.db.execute(query)
                question = result.scalar_one_or_none()
                if question:
                    question.status = QuestionStatus.PENDING  # Keep as pending on error
                    await self.db.commit()
            except Exception as update_error:
                pass 