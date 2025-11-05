import pyodide.ffi
from workers import Response
import json
import uuid

from workers import File

import responses
import logging

logger = logging.getLogger(__name__)


async def handle(form_data, r2_bucket, metadata_db) -> Response:
    # Get Metadata
    metadata: File = form_data.get("metadata")
    image_data = form_data.get("image")

    if metadata is None or image_data is None:
        return responses.create_bad_request_response(
            "Either 'metadata' or 'image' is required.\n"
        )

    image_bytes = await image_data.bytes()
    image_uuid = str(uuid.uuid4())

    print(f"Generated Image UUID: {image_uuid}")

    image_js_buffer = pyodide.ffi.to_js(image_bytes)

    await r2_bucket.put(
        image_uuid,
        image_js_buffer,
        http_metadata={"contentType": "image/png"}
    )

    return responses.create_ok_response("Temp Image Response.")
