import sqlite3
import unittest
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseRepository(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_success(self):
        self.assertTrue(self.db.add(1, "alice", "<p>Hi</p>"))
        self.assertEqual(self.db.get_by_id(1)["name"], "alice")

    def test_add_duplicate_id(self):
        self.db.add(1, "alice", "Hi")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.add(1, "bob", "Hello")

    def test_add_invalid_length(self):
        with self.assertRaises(ValueError):
            self.db.add(1, "a" * 257, "Hello")
        with self.assertRaises(ValueError):
            self.db.add(1, "a", "m" * 8097)

    def test_add_invalid_types(self):
        for args in [(True, "a", "b"), (1, 5, "b"), (1, "a", None)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.db.add(*args)

    def test_add_boundary_lengths(self):
        self.assertTrue(self.db.add(1, "a" * 256, "b" * 8096))

    def test_get_by_id_existing(self):
        self.db.add(7, "alice", "Hello")
        self.assertEqual(self.db.get_by_id(7), {"id": 7, "name": "alice", "message": "Hello"})

    def test_get_by_id_missing(self):
        self.assertIsNone(self.db.get_by_id(999))

    def test_get_by_name_existing(self):
        self.db.add(1, "alice", "One")
        self.db.add(2, "bob", "Two")
        self.db.add(3, "alice", "Three")
        self.assertEqual([x["id"] for x in self.db.get_by_name("alice")], [1, 3])

    def test_get_by_name_missing(self):
        self.assertEqual(self.db.get_by_name("nobody"), [])

    def test_update_existing(self):
        self.db.add(1, "alice", "Old")
        self.assertTrue(self.db.update(1, "New"))
        self.assertEqual(self.db.get_by_id(1)["message"], "New")

    def test_update_missing(self):
        self.assertFalse(self.db.update(100, "New"))

    def test_update_invalid_length(self):
        self.db.add(1, "alice", "Old")
        with self.assertRaises(ValueError):
            self.db.update(1, "x" * 8097)
        self.assertEqual(self.db.get_by_id(1)["message"], "Old")

    def test_delete_existing(self):
        self.db.add(1, "alice", "Hi")
        self.assertTrue(self.db.delete(1))
        self.assertIsNone(self.db.get_by_id(1))

    def test_delete_missing(self):
        self.assertFalse(self.db.delete(999))

    def test_invalid_id(self):
        for method in (self.db.get_by_id, self.db.delete):
            with self.subTest(method=method), self.assertRaises(ValueError):
                method(-1)


if __name__ == "__main__":
    unittest.main()
