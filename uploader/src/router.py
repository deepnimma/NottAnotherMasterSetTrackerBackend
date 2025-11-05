from http import HTTPMethod, HTTPStatus

import image
import preset
import logging

from workers import Request, Response, Headers

logger = logging.getLogger(__name__)


async def handle_request(request: Request, valid_uploader_token: str) -> Response:
    request_data = await _parse_request(request)

    if "error" in request_data:
        return Response(
            f"An error occurred. Message: {str(request_data["error"])}",
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    field_check_flag = _check_request_fields(request_data, valid_uploader_token)

    if field_check_flag is not None:
        return field_check_flag

    return await _route_request(request_data)

def _check_request_fields(request_data: dict, valid_uploader_token: str) -> Response | None:
    missing_list = []
    request_body = request_data.get("body", dict())
    valid_routes = ["image", "preset"]

    # Check Body
    if "image" not in request_body:
        missing_list.append("image")
    if "routing" not in request_body:
        missing_list.append("routing")
    if "image_metadata" not in request_body:
        missing_list.append("image_metadata")

    if len(missing_list) > 0:
        return __create_bad_request_response(f"The following fields are missing in the body of the request: {str(missing_list)}\n")

    # Check Routing
    if request_body.get("routing") not in valid_routes:
        return __create_bad_request_response(f"Routes has to be in the following list of values: {str(valid_routes)}\n")

    # Check Request Method
    request_method = request_data.get("method", HTTPMethod.GET)
    if request_method is not HTTPMethod.POST:
        return Response(
            f"This HTTP Method '{request_method}' is currently unsupported.\n", HTTPStatus.METHOD_NOT_ALLOWED
        )

    # Check Headers
    request_headers = request_data.get("headers", dict())

    logger.info(request_headers)
    print(request_headers)
    if "Uploader-Token" not in request_headers:
        return __create_bad_request_response(f"The following fields are missing in the headers of the request: Uploader-Token\n")

    if request_headers.get("Uploader-Token") != valid_uploader_token:
        return Response("Your uploader token is not valid.\n", HTTPStatus.FORBIDDEN)

    return None

def __create_bad_request_response(msg: str) -> Response:
    return Response(msg, HTTPStatus.BAD_REQUEST)

async def _parse_request(
    request: Request,
) -> dict[str, dict | Headers | HTTPMethod | Exception]:
    """
    Parses the incoming request into an easier to access dict

    :param request: Incoming, unparsed request straight from the user.
    :return: A parsed request with body, headers, and a method field
    """
    try:
        request_data = await request.json()
    except Exception as e:
        return {"error": e}

    request_data = {
        "body": request_data,
        "headers": request.headers,
        "method": request.method,
    }

    return request_data


async def _route_request(
    request_data: dict[str, dict | Headers | HTTPMethod | Exception],
) -> Response:
    # First check uploader token
    # - Parse uploader token from headers

    # Finally check body field
    # If it says "preset", send to preset.py
    # Otherwise, send to image.py
    routing_info = request_data["body"]["routing"]
    if routing_info is None:
        return Response(
            "Body must contain routing info: image,preset.", HTTPStatus.BAD_REQUEST
        )

    if routing_info.lower() == "image":
        logger.info("Routing to image.")
        return Response("Test response.\n", HTTPStatus.OK)
        return await image.handle(request_data)
    elif routing_info.lower() == "preset":
        logger.info("Routing to preset.")
        return await preset.handle(request_data)
    else:
        return Response(
            "Body routing info must be either: image,preset", HTTPStatus.BAD_REQUEST
        )