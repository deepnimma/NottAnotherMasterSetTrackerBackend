-- Migration number: 0005
ALTER TABLE image_metadata
RENAME COLUMN image_key to imageKey;