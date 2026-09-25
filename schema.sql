PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    genre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS votes (
    profile TEXT NOT NULL CHECK (profile IN ('A', 'B')),
    movie_id INTEGER NOT NULL REFERENCES movies(id),
    liked INTEGER NOT NULL CHECK (liked IN (0, 1)),
    PRIMARY KEY (profile, movie_id)
);

CREATE TABLE IF NOT EXISTS watched (
    movie_id INTEGER PRIMARY KEY REFERENCES movies(id),
    watched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Fictional titles for the public demo. The original movie catalogue is not included.
INSERT OR IGNORE INTO movies (id, title, genre) VALUES
    (1, 'Die letzte Sternwarte', 'Science-Fiction'),
    (2, 'Sommer auf dem Dach', 'Komödie'),
    (3, 'Im Schatten der Berge', 'Drama'),
    (4, 'Nachtzug nach Norden', 'Thriller'),
    (5, 'Der Garten am Meer', 'Drama'),
    (6, 'Morgen beginnt heute', 'Science-Fiction');
