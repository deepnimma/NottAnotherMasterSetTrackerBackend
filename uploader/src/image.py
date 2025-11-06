import pyodide.ffi
from workers import Response
import json

import schema
from workers import File

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

    # Check Image
    image_bytes = await image_data.bytes()

    # Build Image Key
    set_name = metadata_json.get("masterSetData").get("setName")
    card_number = metadata_json.get("masterSetData").get("cardNumber")
    card_title = metadata_json.get("cardTitle")
    illustrator = metadata_json.get("illustrator")
    image_key = f"{set_name}-{card_number}-{card_title}-{illustrator}"

    # Add image key to metadata
    metadata_json["imageKey"] = image_key

    image_js_buffer = pyodide.ffi.to_js(image_bytes)

    await r2_bucket.put(
        image_key, image_js_buffer, http_metadata={"contentType": "image/png"}
    )

    return responses.create_ok_response("Temp Image Response.")
