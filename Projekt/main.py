from datetime import datetime, timedelta
from repositories.document_repository import DocumentRepository
from services.document_service import DocumentService

def main():
    # Inicjalizacja repozytorium i serwisu
    doc_repository = DocumentRepository('documents.json')
    doc_service = DocumentService(doc_repository)
    
    # Przykład użycia
    # Dodanie nowego dokumentu
    doc_service.create_document(
        title="Historia Polski",
        year=1999,
        category="Książka historyczna",
        storage_location="Regał A1",
        copies=3,
        user="admin"
    )
    
    # Wyszukiwanie dokumentów
    results = doc_service.search_documents(title="Historia")
    for doc in results:
        print(f"Znaleziono: {doc.title} ({doc.year})")
    
    # Wypożyczenie dokumentu
    if results:
        doc_service.borrow_document(
            results[0].uuid,
            user="jan_kowalski",
            return_date=datetime.now() + timedelta(days=14)
        )

if __name__ == "__main__":
    main()