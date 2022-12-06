import datetime
import os

from peewee import MySQLDatabase, InternalError as PeeweeInternalError
from domain_models.book import Book
from repository.library import Library
from files.pdf_file import PdfFile


class ConsoleLibrary:

    def _input_year(self):
        string_input = input("Enter book year:")
        year = int(float(string_input)) if '.' in string_input else int(string_input)
        while year <= 0 or year > int(datetime.date.today().year):
            string_input = input("Try entering year again:")
            year = int(float(string_input)) if '.' in string_input else int(string_input)
        return year

    def add_book(self):
        os.system("cls")
        title = input("Enter book title:")
        author = input("Enter book author:")
        year = self._input_year()
        book = Book(title, year, author)
        change_option = input("Do you want to create book %s? 1-yes, 2-no: " % book)

        if change_option == '1':
            self.library.add(book=book)

        input("Press enter to go to main menu...")

    def delete_book(self):
        os.system("cls")
        book_number = input("Enter book number to delete:")
        book = self.library.get_at(book_number)
        if not book:
            input("Book not found. Press enter to go to main menu...")
            return

        change_option = input("Do you want to delete book %s? 1-yes, 2-no: " % book)

        if change_option == '1':
            self.library.remove_at(book_number)
            print("Deleted a book! ", book)
            
        input("Press enter to go to main menu...")

    def change_title(self, book_number, book):
        os.system("cls")
        title = input("Enter book title (empty to keep unchanged): ")
        if title == "" or book.title == title:
            input("Title is empty or did not change. Press enter to go to main menu...")
            return
        book.title = title
        change_option = input("Do you want to update book %s? 1-yes, 2-no: " % book)

        if change_option == '1':
            self.library.update_at(book_number, book)
            print("Updated a book! ", book)

    def change_author(self, book_number, book):
        os.system("cls")
        author = input("Enter book author (empty to keep unchanged): ")
        if author == "" or book.author == author:
            input("Author is empty or did not change. Press enter to go to main menu...")
            return
        book.author = author
        change_option = input("Do you want to update book %s? 1-yes, 2-no: " % book)

        if change_option == '1':
            self.library.update_at(book_number, book)
            print("Updated a book! ", book)

    def change_year(self, book_number, book):
        os.system("cls")

        year = self._input_year()

        if book.year == year:
            input("Year did not change. Press enter to go to main menu...")
            return
        book.year = year

        change_option = input("Do you want to update book %s? 1-yes, 2-no: " % book)

        if change_option == '1':
            self.library.update_at(book_number, book)
            print("Updated a book! ", book)

    def update_book(self):
        os.system("cls")
        book_id = input("Enter book number to update: ")
        book = self.library.get_at(book_id)

        if not book:
            input("Book not found. Press enter to go to main menu...")
            return

        print("Updating book ", book)
        change_option = input("What do you want to change? \n 1-title /n 2-author \n 3-year \n 4-cancel input, go back to main menu \n Enter: ")

        if change_option == "1":
            self.change_title(book_id, book)
        elif change_option == "2":
            self.change_author(book_id, book)
        elif change_option == "3":
            self.change_year(book_id, book)

        input("Press enter to go to main menu...")
        
    def count_books(self):
        os.system("cls")
        books = self.library.get_all_books()
        print("Total books: ", len(books))
        input("Press enter to go to main menu...")

    def find_books_year(self):
        os.system("cls")
        year = self._input_year()
        book = self.library.find_by_year(year)
        print("Found: ", book)
        return book

    def find_books_author(self):
        os.system("cls")
        author = input("Input author to search: ")
        book = self.library.find_by_author(author)
        print("Found: ", book)
        return book

    def find_books_title(self):
        os.system("cls")
        title = input("Input title to search: ")
        book = self.library.find_by_title(title)
        print("Found: ", book)
        return book

    def find_books(self):
        os.system("cls")
        search = input("Search books by \n 1 - year \n 2 - author \n 3 - title? \n Enter:")
        result = None
        if search == "1":
            result = self.find_books_year()
        elif search == "2":
            result = self.find_books_author()
        elif search == "3":
            result = self.find_books_title()
        input("Press enter to go to main menu...")
        return result

    def print_all_books(self):
        os.system("cls")
        pdf = PdfFile()
        books = self.library.get_all_books()
        pdf.save(books)
        input("Press enter to go back to main menu...")

    def __init__(self):
        self.library = Library(data_base=MySQLDatabase('бдартем', user='Artem', password='@t@Yj-!BJiYyNU_D', host='localhost', port=3306))

        self.library.connect()

    def run(self):
        try:
            while True:
                os.system("cls")

                command = input(
                    'Select:\n 1-add \n 2-delete \n 3-update \n 4-find \n 5-count \n 6-print \n 7-exit \n Enter:')
                if command == "7":
                    break
                elif command == "1":
                    self.add_book()
                elif command == "2":
                    self.delete_book()
                elif command == "3":
                    self.update_book()
                elif command == "4":
                    self.find_books()
                elif command == "5":
                    self.count_books()
                elif command == "6":
                    self.print_all_books()

            self.library.close()
        except PeeweeInternalError as px:
            print(str(px))

        print("Console Library finished!")
