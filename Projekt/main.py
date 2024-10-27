from repositories.document_repository import DocumentRepository
from services.document_service import DocumentService
from ui.terminal_ui import TerminalUI

def main():
    # Inicjalizacja repozytorium i serwisu
    doc_repository = DocumentRepository('documents.json')
    doc_service = DocumentService(doc_repository)
    terminal_ui = TerminalUI(doc_service)
    terminal_ui.run()
    
if __name__ == "__main__":
    main()