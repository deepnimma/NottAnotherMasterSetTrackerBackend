import responses
from workers import Response


def validate_image_metadata(metadata: dict) -> Response | None:
    """
    Validate the image metadata against the schema.
    :param metadata: The metadata to validate.
    :return: Response if failed, None otherwise.
    """
    import jsonschema
    from jsonschema import ValidationError

    # Open schema
    try:
        jsonschema.validate(metadata, _schema)

        print("Metadata validates against the schema.")
        return None
    except ValidationError as err:
        print(f"Error: {err.message}")
        return responses.create_ok_response(
            f"Metadata failed against the schema. Error Message: {err.message}"
        )


_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/product.schema.json",
    "title": "Image Metadata",
    "description": "Describes an image in the database",
    "type": "object",
    "properties": {
        "version": {
            "description": "Schema Version to be applied.",
            "type": "number",
            "enum": [1],
        },
        "cardTitle": {
            "description": "The text at the very top of the card explaining what it is.",
            "type": "string",
        },
        "mainPokemon": {
            "description": "The main pokemon featured in the illustration.",
            "type": "string",
        },
        "cameoPokemon": {
            "description": "Which cameo pokemon this card contains, if any",
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
        },
        "trainerInfo": {
            "type": "object",
            "properties": {
                "item": {
                    "description": "Whether this card is just an item. For example, Antique Cover Fossil.",
                    "type": "boolean",
                },
                "trainerOwned": {
                    "description": "Whether this pokemon is owned by a trainer. For example, Cynthia's Garchomp EX is owned by Cynthia",
                    "type": "boolean",
                },
                "soleTrainer": {
                    "description": "If the card is just a single trainer. Like Lillie's Determination => Lillie",
                    "type": "boolean",
                },
                "trainer": {
                    "description": "Who the trainer owner is",
                    "type": "string",
                },
            },
            "required": ["item"],
            "if": {
                "properties": {"trainerOwned": {"const": True}},
                "anyOf": [
                    {
                        "properties": {"trainerOwned": {"const": True}},
                        "required": ["trainerOwned"],
                    },
                    {
                        "properties": {"soleTrainer": {"const": True}},
                        "required": ["soleTrainer"],
                    },
                ],
            },
            "then": {
                "properties": {"trainer": {"pattern": "\\S"}},
                "required": ["trainer"],
            },
        },
        "hasReverseHolo": {
            "description": "Whether this particular card has a reverse holo variant.",
            "type": "boolean",
        },
        "mainEnergy": {
            "description": "The main/first energy type of this particular pokemon card. This field is required.",
            "type": "string",
            "enum": [
                "grass",
                "fire",
                "water",
                "electric",
                "psychic",
                "dark",
                "fighting",
                "metal",
                "dragon",
                "normal",
                "trainer",
            ],
        },
        "secondaryEnergy": {
            "description": "The secondary energy type of this particular pokemon card. This field is optional and is required on very few cards.",
            "type": "string",
            "enum": [
                "grass",
                "fire",
                "water",
                "electric",
                "psychic",
                "dark",
                "fighting",
                "metal",
                "dragon",
                "normal",
                "trainer",
            ],
        },
        "illustrator": {
            "description": "The illustrator of this particular card.",
            "type": "string",
            "pattern": "\\S",
        },
        "masterSetData": {
            "type": "object",
            "properties": {
                "setName": {
                    "description": "The name of the set this card belongs to.",
                    "type": "string",
                    "enum": ["Base", "Fossil", "Jungle", "Base Set 2", "Team Rocket"],
                },
                "cardNumber": {
                    "description": "The number of the card in the set",
                    "type": "number",
                },
            },
        },
        "release": {
            "type": "object",
            "properties": {
                "releaseYear": {
                    "description": "Which year this card released.",
                    "type": "number",
                    "minimum": 1999,
                },
                "releaseMonth": {
                    "description": "Which month this card released.",
                    "type": "number",
                    "minimum": 1,
                    "maximum": 12,
                },
                "releaseDay": {
                    "description": "Which day this card released.",
                    "type": "number",
                    "minimum": 1,
                },
            },
            "required": ["releaseYear", "releaseMonth", "releaseDay"],
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "releaseMonth": {"enum": [1, 3, 5, 7, 8, 10, 12]}
                        }
                    },
                    "then": {"properties": {"releaseDay": {"maximum": 31}}},
                },
                {
                    "if": {"properties": {"releaseMonth": {"enum": [4, 6, 9, 11]}}},
                    "then": {"properties": {"releaseDay": {"maximum": 30}}},
                },
                {
                    "if": {
                        "properties": {
                            "releaseMonth": {"const": 2},
                            "releaseYear": {"not": {"multipleOf": 4}},
                        }
                    },
                    "then": {"properties": {"releaseDay": {"maximum": 28}}},
                },
                {
                    "if": {
                        "properties": {
                            "releaseMonth": {"const": 2},
                            "releaseYear": {"multipleOf": 4},
                        }
                    },
                    "then": {"properties": {"releaseDay": {"maximum": 29}}},
                },
            ],
        },
        "tags": {
            "description": "Tags describing the card.",
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "unnotable",
                    "1st-edition",
                    "holofoil",
                    "energy",
                    "dark",
                    "containsCameo",
                ],
                "minItems": 1,
            },
        },
    },
    "required": [
        "version",
        "cardTitle",
        "mainPokemon",
        "hasReverseHolo",
        "mainEnergy",
        "illustrator",
        "masterSetData",
        "release",
    ],
}
