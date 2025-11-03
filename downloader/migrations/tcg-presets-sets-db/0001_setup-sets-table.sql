-- Migration number: 0001 	 2025-11-03T21:55:46.178Z
CREATE TABLE presets_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    presetName TEXT NOT NULL,
    images TEXT, -- JSON List of image links goes here

    UNIQUE (presetName)
);