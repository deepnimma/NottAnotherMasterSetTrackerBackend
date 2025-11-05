import logging

from workers import Request, Response, Headers

import image as image_handler
import preset as preset_handler
import responses

logger = logging.getLogger(__name__)

__valid_routes = ["image", "preset"]

async def handle_request(request: Request, env) -> Response:
    # First get form data
    form_data = await request.form_data()

    # Check Headers
    flag, route = __check_headers(request.headers, env.UPLOADER_TOKEN)

    if flag is not None:
        return flag

    # We need to route between image and preset and move the below from here to image.py
    # Take the routing information in the headers so it's easiers, the uploaders is internal use only

    # Get Data
    if route == "image":
        return await image_handler.handle(form_data, env.image_bucket, env.tcg_image_metadata_db)
    else:
        return await preset_handler.handle(form_data, env.tcg_preset_sets_db)


def __check_headers(
    headers: Headers, valid_uploader_token: str
) -> tuple[Response | None, str]:
    """
    Checks if the headers contain a valid Uploader-Token, and valid Routing information

    :param headers: the headers provided with the request
    :param valid_uploader_token: the valid uploader token present in the environment
    :return: A tuple with response and the routing information. If a response is provided, then the routing information is empty. Otherwise, if all checks pass then Response is None and the routing information is provided.
    """

    if "Uploader-Token" not in headers:
        return (
            responses.create_bad_request_response(
                "Field 'Uploader-Token' must be present in the headers.\n"
            ),
            "",
        )

    if headers.get("Uploader-Token") != valid_uploader_token:
        return responses.create_bad_request_response("Valid 'Uploader-Token' was not passed.\n"), ""

    if "Routing" not in headers:
        return (
            responses.create_bad_request_response("Field 'Routing' must be present in the headers.\n"),
            "",
        )

    route_info = headers.get("Routing").lower()
    if route_info not in __valid_routes:
        return responses.create_bad_request_response("Field 'Routing' must be 'image' or 'preset'.\n"), ""

    return None, route_info
