-- Migration number: 0006

ALTER TABLE image_metadata
ADD COLUMN mainEnergyReal TEXT NOT NULL CHECK(
    mainEnergyReal IN (
        'grass',
        'fire',
        'water',
        'electric',
        'psychic',
        'dark',
        'fighting',
        'metal',
        'dragon',
        'normal',
        'trainer',
        'fairy',
        'colorless',
        'none'
    )
);

ALTER TABLE image_metadata
ADD COLUMN secondaryEnergyReal TEXT NOT NULL CHECK(
    secondaryEnergyReal IN (
    'grass',
    'fire',
    'water',
    'electric',
    'psychic',
    'dark',
    'fighting',
    'metal',
    'dragon',
    'normal',
    'trainer',
    'fairy',
    'colorless',
    'none'
   )
);

UPDATE image_metadata
SET mainEnergyReal = mainEnergy;

UPDATE image_metadata
SET secondaryEnergyReal = secondaryEnergy;

ALTER TABLE image_metadata
DROP COLUMN mainEnergy;

ALTER TABLE image_metadata
DROP COLUMN secondaryEnergy;

ALTER TABLE image_metadata
RENAME COLUMN mainEnergyReal TO mainEnergy;

ALTER TABLE image_metadata
RENAME COLUMN secondaryEnergyReal TO secondaryEnergy;