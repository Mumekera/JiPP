from datetime import datetime
import uuid

class Document:
    def __init__(self, title: str, year: int, category: str, storage_location: str, 
                 copies: int):
        self.uuid = str(uuid.uuid4())
        self.title = title
        self.year = year
        self.category = category
        self.storage_location = storage_location
        self.copies = copies
        self.history = []
        self.borrowed_by = None
        self.return_date = None
        self.last_modified_by = None
        self.last_modified_date = None
    
    def to_dict(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'year': self.year,
            'category': self.category,
            'storage_location': self.storage_location,
            'copies': self.copies,
            'history': self.history,
            'borrowed_by': self.borrowed_by,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'last_modified_by': self.last_modified_by,
            'last_modified_date': self.last_modified_date.isoformat() if self.last_modified_date else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        doc = cls(
            title=data['title'],
            year=data['year'],
            category=data['category'],
            storage_location=data['storage_location'],
            copies=data['copies']
        )
        doc.uuid = data['uuid']
        doc.history = data['history']
        doc.borrowed_by = data['borrowed_by']
        doc.return_date = datetime.fromisoformat(data['return_date']) if data['return_date'] else None
        doc.last_modified_by = data['last_modified_by']
        doc.last_modified_date = datetime.fromisoformat(data['last_modified_date']) if data['last_modified_date'] else None
        return doc