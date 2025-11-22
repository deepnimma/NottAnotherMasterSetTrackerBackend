from http import HTTPStatus
import re
import json

from workers import Request, Response
from urllib.parse import urlparse, parse_qs

# Example flag
"""
curl -X GET "http://localhost:8787?q=pikachu&cameo=1"
curl -X GET "http://localhost:8787?q=ken-sugimori&illustrator=1&descending=1"
curl -X GET "http://localhost:8787?q=jessie&trainer=1&descending=1&cameo=1"
"""


async def handle_request(request: Request, db) -> Response:
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
    raw_search_query = query_params.get("q", [None])[0]

    if raw_search_query is None:
        return Response(
            "No query parameters. Must contain 'q' with at least one pokemon.\n",
            HTTPStatus.BAD_REQUEST,
        )

    secured_search_query_string = sanitize_sql_input(raw_search_query)
    pokemon_names = get_pokemon_names(secured_search_query_string)

    # DB Query Flags
    cameo_flag = True if "cameo" in query_params else False
    trainer_flag = True if "trainer" in query_params else False
    illustrator_flag = True if "illustrator" in query_params else False
    descending = True if "descending" in query_params else False

    # Create db query
    db_query, params = build_image_db_query(
        pokemon_names, illustrator_flag, cameo_flag, trainer_flag, descending
    )

    # Create stmt
    print(f"Making query: {db_query} with params: {params}")
    stmt = db.prepare(db_query)

    # Run stmt
    response = await stmt.bind(*params).all()

    # Get all image keys
    image_keys = []
    rows = response.results.to_py()
    for row in response.results.to_py():
        image_keys.append(row.get("imageKey"))

    # -- Response --
    response_dict = {
        "requested_pokemon_num": len(pokemon_names),
        "requested_pokemon": pokemon_names,
        "parsed_pkmn_names": ", ".join(pokemon_names),
        "cameo_flag": cameo_flag,
        "trainer_flag": trainer_flag,
        "illustrator_flag": illustrator_flag,
        "descending_flag": descending,
        "num_found": len(image_keys),
        "image_keys": image_keys,
        "image_rows": rows,
    }

    response_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    return Response(
        json.dumps(response_dict),
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


def get_pokemon_names(secured_query_string: str) -> list[str]:
    pokemon_names = []
    if secured_query_string:
        new_name = secured_query_string.split(",")

        for name in new_name:
            stripped_name = name.strip()
            if stripped_name not in pokemon_names:
                pokemon_names.append(stripped_name)

            joined_name = " ".join(stripped_name.split("-"))
            if joined_name not in pokemon_names:
                pokemon_names.append(joined_name)

    return pokemon_names


def build_image_db_query(
    pokemon_names: list[str],
    illustrator: bool = False,
    cameo: bool = False,
    trainer: bool = False,
    descending: bool = False,
) -> tuple[str, list[str]]:
    base_query = "SELECT * FROM image_metadata WHERE"

    # Set order
    if descending:
        ordering_string = "ORDER BY releaseDate DESC, cardNumber DESC;"
    else:
        ordering_string = "ORDER BY releaseDate ASC, cardNumber ASC;"

    query_strs = [base_query]
    params = []

    if illustrator:
        column_name = "illustrator"
    elif trainer:
        column_name = "trainer"
    else:
        column_name = "mainPokemon"

    for i, name in enumerate(pokemon_names):
        new_str = "OR " if i > 0 else ""
        new_str += f"{column_name} LIKE ?"
        params.append(f"{name}")
        query_strs.append(new_str)

    if cameo and not illustrator:
        for i, name in enumerate(pokemon_names):
            new_str = f"OR cameoPokemon LIKE ?"
            params.append(f"%{name}%")
            query_strs.append(new_str)

    # Add ordering string
    query_strs.append(ordering_string)

    joined_query = " ".join(query_strs)

    return joined_query, params
