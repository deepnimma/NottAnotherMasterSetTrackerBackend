from http import HTTPStatus
import re

from workers import Request, Response
from urllib.parse import urlparse, parse_qs

async def handle_request(request: Request, env) -> Response:
    url_string = request.url
    parsed_url = urlparse(url_string)
    og_query_params = parse_qs(parsed_url.query)

    cameo_flag = False
    trainer_flag = False

    # Ensure lowercase
    query_params = {}
    for key, value in og_query_params.items():
        lower_key = key.lower()
        lower_values = [v.lower() for v in value]
        query_params[lower_key] = lower_values

    # Sanitize Search Query
    raw_search_query = query_params.get('q', [None])[0]

    if raw_search_query is None:
        return Response("No query parameters. Must contain 'q' with at least one pokemon.\n", HTTPStatus.BAD_REQUEST)

    secured_search_query_string = sanitize_sql_input(raw_search_query)
    pokemon_names = get_pokemon_names(secured_search_query_string)

    if "cameo" in query_params:
        cameo_flag = True
    if "trainer" in query_params:
        trainer_flag = True

    # -- Response --
    response_lines = []
    response_lines.append(f"Found {len(pokemon_names)} Pokemon names.")
    response_lines.append(f"Parsed Pokemon Names: " + ", ".join(pokemon_names))
    response_lines.append(f"Cameo: {cameo_flag}")
    response_lines.append(f"Trainer: {trainer_flag}")
    response_lines.append(build_image_db_query(pokemon_names, cameo_flag, trainer_flag))

    response_text = "\n".join(response_lines) + "\n"

    return Response(response_text, HTTPStatus.OK)

def sanitize_sql_input(input_str: str) -> str | None:
    if input_str is None:
        return None

    sanitized = input_str.strip()
    sanitized = sanitized.replace("'", "").replace('"', '').replace(';', "")
    sanitized = re.sub(r'[^\w\s\-,]', '', sanitized)

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

def build_image_db_query(pokemon_names: list[str], cameo: bool, trainer: bool) -> str:
    base_query = "SELECT * FROM image_metadata WHERE"
    ordering_string = "ORDER BY releaseDate ASC, cardNumber ASC;"
    query_strs = [base_query]

    for i, name in enumerate(pokemon_names):
        new_str = "OR " if i > 0 else ""
        new_str += f"mainPokemon LIKE '{name}' OR illustrator LIKE '{name}'"
        query_strs.append(new_str)

    query_strs.append(ordering_string)

    joined_query = " ".join(query_strs)

    return joined_query
