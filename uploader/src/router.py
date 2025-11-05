from http import HTTPMethod, HTTPStatus
from wsgiref import headers

import image
import preset
import logging

from workers import Request, Response, Headers

from uploader.src.response import create_bad_request

logger = logging.getLogger(__name__)

__valid_routes = ["image", "preset"]

async def handle_request(request: Request, valid_uploader_token: str) -> Response:
    # First get form data
    form_data = await request.form_data()

    # Then get headers
    headers = request.headers

    # Check Headers
    flag, route = __check_headers(headers, valid_uploader_token)

    if flag is not None:
        return flag

    # We need to route between image and preset and move the below from here to image.py
    # Take the routing information in the headers so it's easiers, the uploaders is internal use only

    # Get Data
    if (route == "image") return image.handle(form_data)
    elif (route == "preset") return preset.handle(form_data)
    metadata = form_data.get("metadata", None)
    image = form_data.get("image", None)

    if metadata is None or image is None:
        return create_bad_request(
            "Either 'metadata' or 'image' field was not provided.\n"
        )

    request_data = {"metadata": metadata, "image": image, "headers": headers}


def __check_headers(
    headers: dict[str, str], valid_uploader_token: str
) -> tuple[Response | None, str]:
    """
    Checks if the headers contain a valid Uploader-Token, and valid Routing information

    :param headers: the headers provided with the request
    :param valid_uploader_token: the valid uploader token present in the environment
    :return: A tuple with response and the routing information. If a response is provided, then the routing information is empty. Otherwise, if all checks pass then Response is None and the routing information is provided.
    """

    if "Uploader-Token" not in headers:
        return (
            create_bad_request(
                "Field 'Uploader-Token' must be present in the headers.\n"
            ),
            "",
        )

    if headers.get("Uploader-Token") != valid_uploader_token:
        return create_bad_request("Valid 'Uploader-Token' was not passed.\n"), ""

    if "Routing" not in headers:
        return (
            create_bad_request("Field 'Routing' must be present in the headers.\n"),
            "",
        )

    route_info = headers.get("Routing").lower()
    if route_info not in __valid_routes:
        return create_bad_request("Field 'Routing' must be 'image' or 'preset'.\n"), ""

    return None, route_info
