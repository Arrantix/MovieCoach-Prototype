import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from moviecoach import initialize, list_movies, mark_watched, matches, vote


class MovieCoachTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "demo.db"
        initialize(self.db)

    def tearDown(self):
        self.temp.cleanup()

    def test_demo_has_fictional_movies_and_no_account_table(self):
        self.assertEqual(len(list_movies(self.db)), 6)
        with closing(sqlite3.connect(self.db)) as db:
            tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        self.assertEqual(tables, {"movies", "votes", "watched"})

    def test_match_requires_two_likes_and_disappears_when_watched(self):
        vote(self.db, "A", 1, True)
        vote(self.db, "B", 1, False)
        self.assertEqual(matches(self.db), [])
        vote(self.db, "B", 1, True)
        self.assertEqual(matches(self.db), [(1, "Die letzte Sternwarte")])
        mark_watched(self.db, 1)
        self.assertEqual(matches(self.db), [])

    def test_invalid_input_cannot_create_tables_or_votes(self):
        with self.assertRaises(ValueError):
            vote(self.db, "A; DROP TABLE movies", 1, True)
        with self.assertRaises(ValueError):
            vote(self.db, "A", 999, True)
        with self.assertRaises(ValueError):
            mark_watched(self.db, 2)
        self.assertEqual(list_movies(self.db)[0][1], "Die letzte Sternwarte")


if __name__ == "__main__":
    unittest.main()
