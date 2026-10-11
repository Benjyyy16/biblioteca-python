
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Database:
    BOOKS_FILE = "books.json"
    USERS_FILE = "users.json"
    USER_BOOKS_FILE = "user_books.json"

    def __init__(self, data_dir=BASE_DIR):
        self.data_dir = data_dir
        self.books = self._load(self.BOOKS_FILE, [])
        self.users = self._load(self.USERS_FILE, [{"username": "user", "password": "user"}])
        self.user_books = self._load(self.USER_BOOKS_FILE, {})

    def _path(self, filename):
        return os.path.join(self.data_dir, filename)

    def _load(self, filename, default):
        try:
            with open(self._path(filename), "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return default

    def _save(self, filename, data):
        with open(self._path(filename), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def save_books(self):
        self._save(self.BOOKS_FILE, self.books)

    def save_users(self):
        self._save(self.USERS_FILE, self.users)

    def save_user_books(self):
        self._save(self.USER_BOOKS_FILE, self.user_books)

    def get_books(self):
        return self.books

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def delete_book(self, index):
        if 0 <= index < len(self.books):
            del self.books[index]
            self.save_books()

    def get_users(self):
        return self.users

    def add_user(self, user):
        if any(u['username'] == user['username'] for u in self.users):
            return False
        self.users.append(user)
        self.save_users()
        return True

    def delete_user(self, username):
        self.users = [u for u in self.users if u['username'] != username]
        self.save_users()

    def verify_user(self, username, password):
        return any(u['username'] == username and u['password'] == password for u in self.users)

    def request_book(self, username, book_title):
        if username not in self.user_books:
            self.user_books[username] = []

        for book in self.books:
            if book["title"] == book_title and book_title not in self.user_books[username]:
                self.user_books[username].append(book_title)
                self.save_user_books()
                return True
        return False

    def get_user_books(self, username):
        return self.user_books.get(username, [])

    def return_book(self, username, book_title):
        if username in self.user_books and book_title in self.user_books[username]:
            self.user_books[username].remove(book_title)
            self.save_user_books()
            return True
        return False
