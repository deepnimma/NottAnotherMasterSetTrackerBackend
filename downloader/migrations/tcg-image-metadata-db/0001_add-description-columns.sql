-- Migration number: 0001 	 2025-11-14T22:18:10.133Z
ALTER TABLE image_metadata
ADD COLUMN additionalInfo TEXT;

ALTER TABLE image_metadata
ADD COLUMN flavorText TEXT;

ALTER TABLE image_metadata
ADD COLUMN infoButton TEXT;