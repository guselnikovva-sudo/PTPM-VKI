"""SQLite repository for forum comments."""
import sqlite3


class DatabaseRepository:
    def __init__(self, db_path: str):
        if not isinstance(db_path, str) or not db_path:
            raise ValueError("db_path must be a nonempty string")
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("""CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL CHECK(length(name) BETWEEN 1 AND 256),
            message TEXT NOT NULL CHECK(length(message) BETWEEN 1 AND 8096)
        )""")
        self.connection.commit()

    @staticmethod
    def _id(comment_id):
        if type(comment_id) is not int or comment_id < 1 or comment_id > 9223372036854775807:
            raise ValueError("comment_id must be a positive 64-bit integer")

    @staticmethod
    def _string(value, field, maximum):
        if not isinstance(value, str) or not 1 <= len(value) <= maximum:
            raise ValueError(f"{field} must contain 1..{maximum} characters")

    def get_by_id(self, comment_id: int):
        self._id(comment_id)
        row = self.connection.execute("SELECT id, name, message FROM comments WHERE id=?", (comment_id,)).fetchone()
        return dict(row) if row else None

    def get_by_name(self, username: str):
        self._string(username, "username", 256)
        rows = self.connection.execute("SELECT id, name, message FROM comments WHERE name=? ORDER BY id", (username,)).fetchall()
        return [dict(row) for row in rows]

    def add(self, comment_id: int, username: str, message: str) -> bool:
        self._id(comment_id)
        self._string(username, "username", 256)
        self._string(message, "message", 8096)
        with self.connection:
            self.connection.execute("INSERT INTO comments (id, name, message) VALUES (?, ?, ?)", (comment_id, username, message))
        return True

    def update(self, comment_id: int, new_message: str) -> bool:
        self._id(comment_id)
        self._string(new_message, "new_message", 8096)
        with self.connection:
            cursor = self.connection.execute("UPDATE comments SET message=? WHERE id=?", (new_message, comment_id))
        return cursor.rowcount > 0

    def delete(self, comment_id: int) -> bool:
        self._id(comment_id)
        with self.connection:
            cursor = self.connection.execute("DELETE FROM comments WHERE id=?", (comment_id,))
        return cursor.rowcount > 0

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
