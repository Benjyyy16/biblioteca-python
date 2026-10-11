
import hashlib
import hmac
import json
import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HASH_PREFIX = "pbkdf2_sha256"
HASH_ITERATIONS = 200_000


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), HASH_ITERATIONS)
    return f"{HASH_PREFIX}${HASH_ITERATIONS}${salt}${digest.hex()}"


def check_password(password, stored):
    if not stored.startswith(HASH_PREFIX + "$"):
        # Legacy plaintext entry.
        return hmac.compare_digest(password.encode("utf-8"), stored.encode("utf-8"))
    _, iterations, salt, expected = stored.split("$")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), int(iterations))
    return hmac.compare_digest(digest.hex(), expected)


class Database:
    BOOKS_FILE = "books.json"
    USERS_FILE = "users.json"
    USER_BOOKS_FILE = "user_books.json"

    def __init__(self, data_dir=BASE_DIR):
        self.data_dir = data_dir
        self.books = self._load(self.BOOKS_FILE, [])
        self.users = self._load(self.USERS_FILE, [
            {"username": "adm", "password": hash_password("12"), "role": "admin"},
            {"username": "user", "password": hash_password("user"), "role": "user"},
        ])
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
        self.users.append({
            "username": user["username"],
            "password": hash_password(user["password"]),
            "role": user.get("role", "user"),
        })
        self.save_users()
        return True

    def delete_user(self, username):
        self.users = [u for u in self.users if u['username'] != username]
        self.save_users()

    def _find_user(self, username):
        return next((u for u in self.users if u['username'] == username), None)

    def verify_user(self, username, password):
        user = self._find_user(username)
        if user is None or not check_password(password, user['password']):
            return False
        if not user['password'].startswith(HASH_PREFIX + "$"):
            # Upgrade legacy plaintext password on successful login.
            user['password'] = hash_password(password)
            self.save_users()
        return True

    def is_admin(self, username):
        user = self._find_user(username)
        return bool(user) and user.get("role") == "admin"

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
