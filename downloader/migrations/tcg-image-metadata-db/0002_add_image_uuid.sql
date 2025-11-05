-- Migration number: 0002 2025-11-05T20:40:15.123Z
ALTER TABLE image_metadata
ADD COLUMN image_uuid TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS idx_image_metadata_image_uuid ON image_metadata(image_uuid);