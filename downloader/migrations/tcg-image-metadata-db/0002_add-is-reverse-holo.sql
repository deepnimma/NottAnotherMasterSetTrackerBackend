-- Migration number: 0002 	 2025-11-20T17:41:09.908Z
ALTER TABLE image_metadata
ADD COLUMN isReverseHolo INTEGER NOT NULL DEFAULT 0 CHECK(isReverseHolo IN (0, 1));