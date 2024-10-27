import os
from datetime import datetime, timedelta
from typing import Optional
from services.document_service import DocumentService

class TerminalUI:
    def __init__(self, document_service: DocumentService):
        self.document_service = document_service
        self.current_user = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print("=== System Archiwizacji Dokumentów ===")
        if self.current_user:
            print(f"Zalogowany użytkownik: {self.current_user}")
        print("=" * 37 + "\n")

    def login(self):
        self.print_header()
        username = input("Podaj nazwę użytkownika: ")
        # W prawdziwej aplikacji tutaj byłaby walidacja hasła
        self.current_user = username
        print(f"Zalogowano jako: {username}")
        input("Naciśnij Enter, aby kontynuować...")

    def display_menu(self):
        self.print_header()
        print("1. Wyświetl wszystkie dokumenty")
        print("2. Wyszukaj dokumenty")
        print("3. Dodaj nowy dokument")
        print("4. Edytuj dokument")
        print("5. Usuń dokument")
        print("6. Wypożycz dokument")
        print("7. Zwróć dokument")
        print("8. Pokaż historię dokumentu")
        print("0. Wyjście")
        return input("\nWybierz opcję: ")

    def display_all_documents(self):
        self.print_header()
        print("Lista wszystkich dokumentów:\n")
        documents = self.document_service.get_all_documents()
        for i, doc in enumerate(documents, 1):
            status = "Wypożyczony" if doc.borrowed_by else "Dostępny"
            print(f"{i}. {doc.title} ({doc.year})")
            print(f"   UUID: {doc.uuid}")
            print(f"   Kategoria: {doc.category}")
            print(f"   Lokalizacja: {doc.storage_location}")
            print(f"   Status: {status}")
            if doc.borrowed_by:
                print(f"   Wypożyczony przez: {doc.borrowed_by}")
                print(f"   Data zwrotu: {doc.return_date}")
            print()
        input("\nNaciśnij Enter, aby kontynuować...")

    def search_documents(self):
        self.print_header()
        print("Wyszukiwanie dokumentów\n")
        year = input("Rok (Enter aby pominąć): ")
        title = input("Tytuł (Enter aby pominąć): ")
        location = input("Lokalizacja (Enter aby pominąć): ")

        year = int(year) if year.isdigit() else None
        title = title if title else None
        location = location if location else None

        results = self.document_service.search_documents(year, title, location)
        
        print("\nWyniki wyszukiwania:")
        if not results:
            print("Nie znaleziono dokumentów spełniających kryteria.")
        else:
            for i, doc in enumerate(results, 1):
                print(f"\n{i}. {doc.title} ({doc.year})")
                print(f"   Lokalizacja: {doc.storage_location}")
                print(f"   Status: {'Wypożyczony' if doc.borrowed_by else 'Dostępny'}")

        input("\nNaciśnij Enter, aby kontynuować...")

    def add_document(self):
        self.print_header()
        print("Dodawanie nowego dokumentu\n")
        
        title = input("Tytuł: ")
        while True:
            try:
                year = int(input("Rok: "))
                break
            except ValueError:
                print("Proszę podać prawidłowy rok.")
        
        category = input("Kategoria: ")
        storage_location = input("Lokalizacja: ")
        while True:
            try:
                copies = int(input("Liczba kopii: "))
                break
            except ValueError:
                print("Proszę podać prawidłową liczbę kopii.")

        try:
            document = self.document_service.create_document(
                title=title,
                year=year,
                category=category,
                storage_location=storage_location,
                copies=copies,
                user=self.current_user
            )
            print("\nDokument został dodany pomyślnie!")
            print(f"UUID dokumentu: {document.uuid}")
        except Exception as e:
            print(f"\nBłąd podczas dodawania dokumentu: {str(e)}")

        input("\nNaciśnij Enter, aby kontynuować...")

    def edit_document(self):
        self.print_header()
        print("Edycja dokumentu\n")
        
        uuid = input("Podaj UUID dokumentu do edycji: ")
        documents = self.document_service.get_all_documents()
        document = next((doc for doc in documents if doc.uuid == uuid), None)
        
        if not document:
            print("Nie znaleziono dokumentu o podanym UUID.")
            input("\nNaciśnij Enter, aby kontynuować...")
            return

        print(f"\nEdycja dokumentu: {document.title}")
        print("(Zostaw puste pole, aby zachować obecną wartość)")
        
        title = input(f"Tytuł [{document.title}]: ") or document.title
        year_str = input(f"Rok [{document.year}]: ")
        year = int(year_str) if year_str.isdigit() else document.year
        category = input(f"Kategoria [{document.category}]: ") or document.category
        location = input(f"Lokalizacja [{document.storage_location}]: ") or document.storage_location
        copies_str = input(f"Liczba kopii [{document.copies}]: ")
        copies = int(copies_str) if copies_str.isdigit() else document.copies

        updated_data = {
            'title': title,
            'year': year,
            'category': category,
            'storage_location': location,
            'copies': copies
        }

        try:
            self.document_service.update_document(uuid, updated_data, self.current_user)
            print("\nDokument został zaktualizowany pomyślnie!")
        except Exception as e:
            print(f"\nBłąd podczas aktualizacji dokumentu: {str(e)}")

        input("\nNaciśnij Enter, aby kontynuować...")

    def delete_document(self):
        self.print_header()
        print("Usuwanie dokumentu\n")
        
        uuid = input("Podaj UUID dokumentu do usunięcia: ")
        confirm = input("Czy na pewno chcesz usunąć ten dokument? (t/n): ")
        
        if confirm.lower() == 't':
            try:
                self.document_service.delete_document(uuid)
                print("\nDokument został usunięty pomyślnie!")
            except Exception as e:
                print(f"\nBłąd podczas usuwania dokumentu: {str(e)}")
        else:
            print("\nOperacja anulowana.")

        input("\nNaciśnij Enter, aby kontynuować...")

    def borrow_document(self):
        self.print_header()
        print("Wypożyczanie dokumentu\n")
        
        uuid = input("Podaj UUID dokumentu do wypożyczenia: ")
        days = int(input("Na ile dni chcesz wypożyczyć dokument?: "))
        return_date = datetime.now() + timedelta(days=days)
        
        try:
            self.document_service.borrow_document(uuid, self.current_user, return_date)
            print("\nDokument został wypożyczony pomyślnie!")
            print(f"Data zwrotu: {return_date.strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"\nBłąd podczas wypożyczania dokumentu: {str(e)}")

        input("\nNaciśnij Enter, aby kontynuować...")

    def return_document(self):
        self.print_header()
        print("Zwrot dokumentu\n")
        
        uuid = input("Podaj UUID dokumentu do zwrotu: ")
        
        try:
            self.document_service.return_document(uuid, self.current_user)
            print("\nDokument został zwrócony pomyślnie!")
        except Exception as e:
            print(f"\nBłąd podczas zwrotu dokumentu: {str(e)}")

        input("\nNaciśnij Enter, aby kontynuować...")

    def show_document_history(self):
        self.print_header()
        print("Historia dokumentu\n")
        
        uuid = input("Podaj UUID dokumentu: ")
        documents = self.document_service.get_all_documents()
        document = next((doc for doc in documents if doc.uuid == uuid), None)
        
        if not document:
            print("Nie znaleziono dokumentu o podanym UUID.")
        else:
            print(f"\nHistoria dokumentu: {document.title}")
            for entry in document.history:
                print(f"\nAkcja: {entry['action']}")
                print(f"Użytkownik: {entry['user']}")
                print(f"Data: {entry['date']}")

        input("\nNaciśnij Enter, aby kontynuować...")

    def run(self):
        self.login()
        while True:
            choice = self.display_menu()
            
            if choice == '0':
                print("\nDo widzenia!")
                break
            elif choice == '1':
                self.display_all_documents()
            elif choice == '2':
                self.search_documents()
            elif choice == '3':
                self.add_document()
            elif choice == '4':
                self.edit_document()
            elif choice == '5':
                self.delete_document()
            elif choice == '6':
                self.borrow_document()
            elif choice == '7':
                self.return_document()
            elif choice == '8':
                self.show_document_history()
            else:
                input("Nieprawidłowa opcja. Naciśnij Enter, aby kontynuować...")
