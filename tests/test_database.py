import json
import os
import tempfile
import unittest

from database import HASH_PREFIX, Database


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        books = [{"title": "Don Quijote de la Mancha", "author": "Miguel de Cervantes", "stock": 20}]
        with open(os.path.join(self.tmp.name, "books.json"), "w", encoding="utf-8") as f:
            json.dump(books, f)
        self.db = Database(data_dir=self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_defaults_when_files_are_missing(self):
        self.assertEqual(self.db.get_user_books("user"), [])
        self.assertTrue(self.db.verify_user("user", "user"))

    def test_request_and_return_book(self):
        self.assertTrue(self.db.request_book("ana", "Don Quijote de la Mancha"))
        self.assertEqual(self.db.get_user_books("ana"), ["Don Quijote de la Mancha"])
        self.assertTrue(self.db.return_book("ana", "Don Quijote de la Mancha"))
        self.assertEqual(self.db.get_user_books("ana"), [])

    def test_cannot_request_same_book_twice_or_unknown_book(self):
        self.assertTrue(self.db.request_book("ana", "Don Quijote de la Mancha"))
        self.assertFalse(self.db.request_book("ana", "Don Quijote de la Mancha"))
        self.assertFalse(self.db.request_book("ana", "Libro inexistente"))

    def test_user_books_are_persisted(self):
        self.db.request_book("ana", "Don Quijote de la Mancha")
        reloaded = Database(data_dir=self.tmp.name)
        self.assertEqual(reloaded.get_user_books("ana"), ["Don Quijote de la Mancha"])

    def test_add_user_rejects_duplicates(self):
        self.assertTrue(self.db.add_user({"username": "ana", "password": "x"}))
        self.assertFalse(self.db.add_user({"username": "ana", "password": "y"}))
        self.assertTrue(self.db.verify_user("ana", "x"))

    def test_delete_book_ignores_invalid_index(self):
        self.db.delete_book(5)
        self.assertEqual(len(self.db.get_books()), 1)
        self.db.delete_book(0)
        self.assertEqual(self.db.get_books(), [])

    def test_passwords_are_stored_hashed(self):
        self.db.add_user({"username": "ana", "password": "secreta"})
        stored = next(u for u in self.db.get_users() if u["username"] == "ana")["password"]
        self.assertTrue(stored.startswith(HASH_PREFIX + "$"))
        self.assertNotIn("secreta", stored)
        self.assertFalse(self.db.verify_user("ana", "otra"))

    def test_legacy_plaintext_password_is_upgraded_on_login(self):
        with open(os.path.join(self.tmp.name, "users.json"), "w", encoding="utf-8") as f:
            json.dump([{"username": "old", "password": "1234"}], f)
        db = Database(data_dir=self.tmp.name)
        self.assertFalse(db.verify_user("old", "nope"))
        self.assertTrue(db.verify_user("old", "1234"))
        reloaded = Database(data_dir=self.tmp.name)
        self.assertTrue(reloaded.get_users()[0]["password"].startswith(HASH_PREFIX + "$"))
        self.assertTrue(reloaded.verify_user("old", "1234"))

    def test_admin_role(self):
        self.assertTrue(self.db.verify_user("adm", "12"))
        self.assertTrue(self.db.is_admin("adm"))
        self.assertFalse(self.db.is_admin("user"))
        self.assertFalse(self.db.is_admin("missing"))


if __name__ == "__main__":
    unittest.main()
