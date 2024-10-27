import json
from typing import List, Optional
from datetime import datetime
from models.document import Document

class DocumentRepository:
    def __init__(self, file_path: str = 'documents.json'):
        self.file_path = file_path
        self.documents = self._load_documents()
    
    def _load_documents(self) -> List[Document]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:  # dodajemy encoding='utf-8'
                data = json.load(f)
                if isinstance(data, dict) and 'documents' in data:
                    return [Document.from_dict(doc_data) for doc_data in data['documents']]
                return []
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Błąd podczas parsowania pliku JSON: {e}")
            return []
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")
            return []
    
    def _save_documents(self):
        with open(self.file_path, 'w') as f:
            json.dump([doc.to_dict() for doc in self.documents], f, indent=2)
    
    def add_document(self, document: Document, user: str):
        document.last_modified_by = user
        document.last_modified_date = datetime.now()
        self.documents.append(document)
        self._save_documents()
    
    def remove_document(self, uuid: str):
        self.documents = [doc for doc in self.documents if doc.uuid != uuid]
        self._save_documents()
    
    def update_document(self, uuid: str, updated_data: dict, user: str):
        for doc in self.documents:
            if doc.uuid == uuid:
                for key, value in updated_data.items():
                    if hasattr(doc, key):
                        setattr(doc, key, value)
                doc.last_modified_by = user
                doc.last_modified_date = datetime.now()
                doc.history.append({
                    'action': 'modified',
                    'user': user,
                    'date': datetime.now().isoformat()
                })
                break
        self._save_documents()
    
    def borrow_document(self, uuid: str, user: str, return_date: datetime):
        for doc in self.documents:
            if doc.uuid == uuid:
                doc.borrowed_by = user
                doc.return_date = return_date
                doc.history.append({
                    'action': 'borrowed',
                    'user': user,
                    'date': datetime.now().isoformat()
                })
                break
        self._save_documents()
    
    def return_document(self, uuid: str, user: str):
        for doc in self.documents:
            if doc.uuid == uuid:
                doc.borrowed_by = None
                doc.return_date = None
                doc.history.append({
                    'action': 'returned',
                    'user': user,
                    'date': datetime.now().isoformat()
                })
                break
        self._save_documents()
    
    def search_documents(self, year: Optional[int] = None, title: Optional[str] = None, 
                        location: Optional[str] = None) -> List[Document]:
        results = self.documents
        
        if year:
            results = [doc for doc in results if doc.year == year]
        if title:
            results = [doc for doc in results if title.lower() in doc.title.lower()]
        if location:
            results = [doc for doc in results if location.lower() in doc.storage_location.lower()]
        
        return results
    
    def get_all_documents(self) -> List[Document]:
        return self.documents
