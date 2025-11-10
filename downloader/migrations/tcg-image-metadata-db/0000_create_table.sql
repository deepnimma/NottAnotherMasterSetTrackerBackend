-- Migration number: 0000
CREATE TABLE image_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setName TEXT NOT NULL,
    cardNumber TEXT NOT NULL,
    version INTEGER NOT NULL,
    cardTitle TEXT NOT NULL,
    mainPokemon TEXT NOT NULL,
    hasReverseHolo INTEGER NOT NULL CHECK(hasReverseHolo IN (0, 1)),
    illustrator TEXT NOT NULL,
    releaseDate TEXT NOT NULL CHECK(date(releaseDate) NOT NULL),
    cameoPokemon TEXT,
    tags TEXT,
    imageKey TEXT,

    item INTEGER CHECK(item IN (0, 1)),
    trainerOwned INTEGER CHECK(trainerOwned IN (0, 1)),
    soleTrainer INTEGER CHECK(soleTrainer IN (0, 1)),
    trainer TEXT,

    mainEnergy TEXT NOT NULL CHECK(
        mainEnergy IN (
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
    ),

    -- From 0001, modified by 0006 to be NOT NULL and include new types
    secondaryEnergy TEXT NOT NULL CHECK(
        secondaryEnergy IN (
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
    ),

    UNIQUE(setName, cardNumber)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_image_metadata_imageKey ON image_metadata(imageKey);