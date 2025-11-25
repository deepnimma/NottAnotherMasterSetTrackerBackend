from http import HTTPStatus
import re
import json

from workers import Request, Response
from urllib.parse import urlparse, parse_qs

from pkmn import handle_en_pkmn_request

# Example flag
"""
curl -X GET "http://localhost:8787?q=pikachu&cameo=1"
curl -X GET "http://localhost:8787?q=ken-sugimori&illustrator=1&descending=1"
curl -X GET "http://localhost:8787?q=jessie&trainer=1&descending=1&cameo=1"
"""


async def handle_request(request: Request, env) -> Response:
    url_string = request.url
    parsed_url = urlparse(url_string)
    og_query_params = parse_qs(parsed_url.query)

    # Ensure lowercase
    query_params = {}
    for key, value in og_query_params.items():
        lower_key = key.lower()
        lower_values = [v.lower() for v in value]
        query_params[lower_key] = lower_values

    # Sanitize Search Query
    raw_search_query: str | None = query_params.get("q", [None])[0]

    if raw_search_query is None:
        return Response(
            "No query parameters. Must contain 'q' with at least one pokemon.\n",
            HTTPStatus.BAD_REQUEST,
        )

    secured_search_query_string = sanitize_sql_input(raw_search_query)

    if "set" in query_params:
        return Response("Not implemented.", HTTPStatus.NOT_IMPLEMENTED)
    else:
        english_response = await handle_en_pkmn_request(
            env.tcg_image_metadata_db,
            secured_search_query_string,
            query_params,
        )

    response_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    return Response(
        json.dumps(english_response),
        HTTPStatus.OK,
        headers=response_headers,
    )


def sanitize_sql_input(input_str: str) -> str | None:
    if input_str is None:
        return None

    sanitized = input_str.strip()
    sanitized = sanitized.replace("'", "").replace('"', "").replace(";", "")
    sanitized = re.sub(r"[^\w\s\-,]", "", sanitized)

    return sanitized
