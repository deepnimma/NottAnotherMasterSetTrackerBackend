-- Migration number: 0004 2025-11-05T22:00:00.00Z
ALTER TABLE image_metadata
RENAME COLUMN image_uuid TO image_key;