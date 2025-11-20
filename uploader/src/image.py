import pyodide.ffi
from workers import Response
import json

import schema

import responses
import logging

logger = logging.getLogger(__name__)


async def handle(form_data, r2_bucket, metadata_db) -> Response:
    # Get Metadata
    metadata = form_data.get("metadata")
    image_data = form_data.get("image")

    if metadata is None or image_data is None:
        return responses.create_bad_request_response(
            "Either 'metadata' or 'image' is required.\n"
        )

    # Get Metadata
    metadata_json = json.loads(await metadata.text())
    res = schema.validate_image_metadata(metadata_json)

    if res is not None:
        return res

    # Add image key to metadata
    image_key = _create_image_key(metadata_json)
    metadata_json["imageKey"] = image_key

    # Get image ready for upload
    image_bytes = await image_data.bytes()
    image_js_buffer = pyodide.ffi.to_js(image_bytes)

    # Put image in bucket
    await r2_bucket.put(
        image_key, image_js_buffer, http_metadata={"contentType": "image/png"}
    )

    # Transform Data for SQL
    # - Format release date (YYYY-MM-DD)
    release_obj = metadata_json.get("release")
    release_date_str = (
        f"{release_obj['releaseYear']}-"
        f"{release_obj['releaseMonth']:02d}-"
        f"{release_obj['releaseDay']:02d}"
    )

    # - Convert boolean to integer
    has_reverse_int = 1 if metadata_json["hasReverseHolo"] else 0
    is_reverse_int = 1 if metadata_json.get("isReverseHolo", False) else 0

    # - Serialize JSON Objects to strings for TEXT columns
    cameo_str = json.dumps(metadata_json.get("cameoPokemon", list()))
    tags_str = json.dumps(metadata_json.get("tags", list()))

    # Prepare and Execute D1 Statement
    stmt = metadata_db.prepare(
        """
        INSERT INTO image_metadata (
            setName, cardNumber, version, cardTitle,
            mainPokemon, hasReverseHolo, illustrator, mainEnergy,
            secondaryEnergy, releaseDate, cameoPokemon,
            tags, imageKey, item, trainerOwned, soleTrainer, trainer,
            additionalInfo, flavorText, infoButton, isReverseHolo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    )

    # Description columns
    additional_info = metadata_json.get("additionalInfo", "")
    flavor_text = metadata_json.get("flavorText", "")
    info_button = metadata_json.get("infoButton", "")

    set_name = metadata_json.get("masterSetData").get("setName").lower()
    card_number = metadata_json.get("masterSetData").get("cardNumber")
    version = metadata_json.get("version")
    card_title = metadata_json.get("cardTitle").lower()
    main_pokemon = metadata_json.get("mainPokemon").lower()
    illustrator = metadata_json.get("illustrator").lower()
    main_energy = metadata_json.get("mainEnergy").lower()
    secondary_energy = metadata_json.get("secondaryEnergy", "none").lower()

    # Trainer
    trainer_data = metadata_json.get("trainerInfo", dict())
    item_bool = 0 if trainer_data.get("item", False) is False else 1
    trainer_owned = 0 if trainer_data.get("trainerOwned", False) is False else 1
    sole_trainer = 0 if trainer_data.get("soleTrainer", False) is False else 1
    trainer = trainer_data.get("trainer", "").lower()

    args = [
        set_name,
        card_number,
        version,
        card_title,
        main_pokemon,
        has_reverse_int,  # hasReverseHolo
        illustrator,
        main_energy,
        secondary_energy,
        release_date_str,  # releaseDate
        cameo_str,  # cameoPokemon
        tags_str,  # tags
        image_key,
        item_bool,
        trainer_owned,
        sole_trainer,
        trainer,
        additional_info,
        flavor_text,
        info_button,
        is_reverse_int,
    ]

    print(f"Pushing the following values: {args}")

    await stmt.bind(
        set_name,
        card_number,
        version,
        card_title,
        main_pokemon,
        has_reverse_int,  # hasReverseHolo
        illustrator,
        main_energy,
        secondary_energy,
        release_date_str,  # releaseDate
        cameo_str,  # cameoPokemon
        tags_str,  # tags
        image_key,
        item_bool,
        trainer_owned,
        sole_trainer,
        trainer,
        additional_info,
        flavor_text,
        info_button,
        is_reverse_int,
    ).run()

    return responses.create_ok_response(
        f"Image with key: {image_key} released on {release_date_str} has been pushed to the database.\n\n"
    )


def _create_image_key(image_metadata: dict) -> str:
    # Build Image Key
    set_name = image_metadata.get("masterSetData").get("setName")
    card_number = image_metadata.get("masterSetData").get("cardNumber")
    card_title = image_metadata.get("cardTitle")
    illustrator = image_metadata.get("illustrator")
    image_key = f"{set_name}-{card_number}-{card_title}-{illustrator}"

    return _image_keyify(image_key)


def _image_keyify(image_key: str) -> str:
    image_key = image_key.replace(" ", "-")
    image_key = image_key.lower()

    return image_key
