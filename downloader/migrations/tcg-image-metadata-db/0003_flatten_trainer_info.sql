-- Migration number: 0003    2025-11-05T22:00:00.000Z
-- Purpose: Replaces the 'trainerInfo' JSON column with flattened, specific columns.

-- 1. Add the new columns
ALTER TABLE image_metadata ADD COLUMN item INTEGER CHECK(item IN (0, 1));
ALTER TABLE image_metadata ADD COLUMN trainerOwned INTEGER CHECK(trainerOwned IN (0, 1));
ALTER TABLE image_metadata ADD COLUMN soleTrainer INTEGER CHECK(soleTrainer IN (0, 1));
ALTER TABLE image_metadata ADD COLUMN trainer TEXT;

-- 2. Populate the new columns by parsing the old JSON column
-- We use COALESCE to provide a default of '0' (false) if the key is missing from the JSON.
UPDATE image_metadata
SET
    item = COALESCE(json_extract(trainerInfo, '$.item'), 0),
    trainerOwned = COALESCE(json_extract(trainerInfo, '$.trainerOwned'), 0),
    soleTrainer = COALESCE(json_extract(trainerInfo, '$.soleTrainer'), 0),
    trainer = json_extract(trainerInfo, '$.trainer')
WHERE trainerInfo IS NOT NULL;

-- 3. Drop the old JSON column
ALTER TABLE image_metadata DROP COLUMN trainerInfo;