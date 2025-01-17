
import json

class Database:
    BOOKS_FILE = "books.json"
    USERS_FILE = "users.json"

    def __init__(self):
        self.books = self.load_books()
        self.users = self.load_users()

    def load_books(self):
        try:
            with open(self.BOOKS_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def load_users(self):
        try:
            with open(self.USERS_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return [{"username": "user", "password": "user"}]

    def save_books(self):
        with open(self.BOOKS_FILE, "w") as f:
            json.dump(self.books, f)

    def save_users(self):
        with open(self.USERS_FILE, "w") as f:
            json.dump(self.users, f)

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

        try:
            with open(self.USER_BOOKS_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_books(self):
        with open(self.BOOKS_FILE, "w") as f:
            json.dump(self.books, f)

    def save_users(self):
        with open(self.USERS_FILE, "w") as f:
            json.dump(self.users, f)

    def save_user_books(self):
        with open(self.USER_BOOKS_FILE, "w") as f:
            json.dump(self.user_books, f)

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
