from datetime import datetime
from typing import List, Optional
from models.document import Document
from repositories.document_repository import DocumentRepository

class DocumentService:
    def __init__(self, document_repository: DocumentRepository):
        self.repository = document_repository
    
    def create_document(self, title: str, year: int, category: str, 
                       storage_location: str, copies: int, user: str) -> Document:
        document = Document(title, year, category, storage_location, copies)
        self.repository.add_document(document, user)
        return document
    
    def update_document(self, uuid: str, updated_data: dict, user: str):
        self.repository.update_document(uuid, updated_data, user)
    
    def delete_document(self, uuid: str):
        self.repository.remove_document(uuid)
    
    def borrow_document(self, uuid: str, user: str, return_date: datetime):
        self.repository.borrow_document(uuid, user, return_date)
    
    def return_document(self, uuid: str, user: str):
        self.repository.return_document(uuid, user)
    
    def search_documents(self, year: Optional[int] = None, title: Optional[str] = None, 
                        location: Optional[str] = None) -> List[Document]:
        return self.repository.search_documents(year, title, location)
    
    def get_all_documents(self) -> List[Document]:
        return self.repository.get_all_documents()