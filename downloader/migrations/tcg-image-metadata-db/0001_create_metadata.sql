-- Migration number: 0001 	 2025-11-03T21:29:42.203Z
CREATE TABLE image_metadata (
    -- Synthetic primary key. Doesn't really matter much to us.
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Flattened from 'masterSetData'
    setName TEXT NOT NULL CHECK(setName IN (
        -- WOTC Base Era
        'base',
        'fossil',
        'jungle',
        'base-set-2',
        'team-rocket'
    )),
    cardNumber INTEGER NOT NULL,

    version INTEGER NOT NULL CHECK(version = 1),
    cardTitle TEXT NOT NULL,
    mainPokemon TEXT NOT NULL,
    hasReverseHolo INTEGER NOT NULL CHECK(hasReverseHolo IN (0, 1)),
    illustrator TEXT NOT NULL,

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
            'trainer'
        )
    ),
    secondaryEnergy TEXT CHECK(
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
            'trainer'
        )
    ),

    releaseDate TEXT NOT NULL CHECK(date(releaseDate) NOT NULL),

    cameoPokemon TEXT,
    trainerInfo TEXT,
    tags TEXT,

    UNIQUE (setName, cardNumber)
);