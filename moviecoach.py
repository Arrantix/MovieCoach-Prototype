"""Small, privacy-safe CLI demo of the MovieCoach course prototype."""

import argparse
from contextlib import closing
from pathlib import Path
import sqlite3


DEFAULT_DB = Path(__file__).with_name("moviecoach.db")
SCHEMA = Path(__file__).with_name("schema.sql")
PROFILES = ("A", "B")


def connect(db_path):
    db = sqlite3.connect(db_path)
    db.execute("PRAGMA foreign_keys = ON")
    return db


def initialize(db_path):
    with closing(connect(db_path)) as db:
        db.executescript(SCHEMA.read_text(encoding="utf-8"))
        db.commit()


def list_movies(db_path):
    with closing(connect(db_path)) as db:
        return db.execute("SELECT id, title, genre FROM movies ORDER BY id").fetchall()


def vote(db_path, profile, movie_id, liked):
    if profile not in PROFILES:
        raise ValueError("profile must be A or B")
    if not isinstance(movie_id, int) or movie_id < 1:
        raise ValueError("movie_id must be a positive integer")
    if liked not in (True, False):
        raise ValueError("liked must be a boolean")
    with closing(connect(db_path)) as db:
        if db.execute("SELECT 1 FROM movies WHERE id = ?", (movie_id,)).fetchone() is None:
            raise ValueError("movie does not exist")
        db.execute(
            "INSERT INTO votes (profile, movie_id, liked) VALUES (?, ?, ?) "
            "ON CONFLICT(profile, movie_id) DO UPDATE SET liked = excluded.liked",
            (profile, movie_id, int(liked)),
        )
        db.commit()


def matches(db_path):
    with closing(connect(db_path)) as db:
        return db.execute(
            "SELECT movies.id, movies.title FROM movies "
            "JOIN votes ON votes.movie_id = movies.id "
            "LEFT JOIN watched ON watched.movie_id = movies.id "
            "WHERE watched.movie_id IS NULL "
            "GROUP BY movies.id, movies.title "
            "HAVING COUNT(DISTINCT votes.profile) = 2 AND MIN(votes.liked) = 1 "
            "ORDER BY movies.id"
        ).fetchall()


def mark_watched(db_path, movie_id):
    if movie_id not in {match_id for match_id, _ in matches(db_path)}:
        raise ValueError("movie is not an available match")
    with closing(connect(db_path)) as db:
        db.execute("INSERT INTO watched (movie_id) VALUES (?)", (movie_id,))
        db.commit()


def main():
    parser = argparse.ArgumentParser(description="MovieCoach course prototype demo")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="local SQLite file")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="create the demo database with fictional films")
    commands.add_parser("movies", help="list demo films")
    vote_parser = commands.add_parser("vote", help="record a like or dislike")
    vote_parser.add_argument("profile", choices=PROFILES)
    vote_parser.add_argument("movie_id", type=int)
    vote_parser.add_argument("choice", choices=("like", "dislike"))
    commands.add_parser("matches", help="show films liked by both profiles")
    watched_parser = commands.add_parser("watched", help="remove a match from the list")
    watched_parser.add_argument("movie_id", type=int)
    args = parser.parse_args()

    if args.command == "init":
        initialize(args.db)
        print(f"Demo database ready: {args.db}")
        return
    if not args.db.is_file():
        parser.error("database missing; run 'init' first")
    try:
        if args.command == "movies":
            for movie_id, title, genre in list_movies(args.db):
                print(f"{movie_id}: {title} ({genre})")
        elif args.command == "vote":
            vote(args.db, args.profile, args.movie_id, args.choice == "like")
            print("Vote saved.")
        elif args.command == "matches":
            available = matches(args.db)
            for movie_id, title in available:
                print(f"{movie_id}: {title}")
            if not available:
                print("No shared matches yet.")
        elif args.command == "watched":
            mark_watched(args.db, args.movie_id)
            print("Match marked as watched.")
    except (ValueError, sqlite3.Error) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
