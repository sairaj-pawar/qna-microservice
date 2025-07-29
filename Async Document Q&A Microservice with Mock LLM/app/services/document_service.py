from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from ..models.document import Document
from ..schemas.document import DocumentCreate, DocumentResponse


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_document(self, document_data: DocumentCreate) -> DocumentResponse:
        """Create a new document"""
        try:
            document = Document(
                title=document_data.title,
                content=document_data.content
            )
            self.db.add(document)
            await self.db.commit()
            await self.db.refresh(document)
            
            return DocumentResponse.from_orm(document)
        except Exception as e:
            await self.db.rollback()
            raise

    async def get_document(self, document_id: int) -> Optional[DocumentResponse]:
        """Get a document by ID"""
        try:
            query = select(Document).where(Document.id == document_id)
            result = await self.db.execute(query)
            document = result.scalar_one_or_none()
            
            if document:
                return DocumentResponse.from_orm(document)
            else:
                return None
        except Exception as e:
            raise

    async def get_all_documents(self) -> List[DocumentResponse]:
        """Get all documents"""
        try:
            query = select(Document)
            result = await self.db.execute(query)
            documents = result.scalars().all()
            
            return [DocumentResponse.from_orm(doc) for doc in documents]
        except Exception as e:
            raise

    async def document_exists(self, document_id: int) -> bool:
        """Check if a document exists"""
        try:
            query = select(Document).where(Document.id == document_id)
            result = await self.db.execute(query)
            document = result.scalar_one_or_none()
            
            return document is not None
        except Exception as e:
            raise 