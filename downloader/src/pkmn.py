from enum import Enum

from workers import Request, Response
import responses


class Languages(Enum):
    EN = ("English",)
    JP = "Japanese"


async def handle_en_pkmn_request(
    en_db,
    search_query: str,
    params: dict,
) -> dict:
    """
    Handles a Pokemon request, for now it only handles English requests and is made with
    expansion to other languages in mind.
    :param en_db: The ENGLISH DB to make the query to.
    :param search_query: The search query inputted by the user.
    :param params: The query params
    :return:
    """

    pokemon_names = get_pokemon_names(search_query)

    # DB Query Flags
    cameo_flag = True if "cameo" in params else False
    trainer_flag = True if "trainer" in params else False
    illustrator_flag = True if "illustrator" in params else False
    descending = True if "descending" in params else False

    # Create en_db query
    db_query, db_params = build_en_image_db_query(
        pokemon_names, illustrator_flag, cameo_flag, trainer_flag, descending
    )

    # Create stmt
    print(f"(EN) Making query: {db_query} with params: {db_params}")
    stmt = en_db.prepare(db_query)

    # Run stmt
    response = await stmt.bind(*db_params).all()

    rows = response.results.to_py()

    return responses.build_response_dict(
        pokemon_names,
        rows,
        cameo_flag,
        trainer_flag,
        illustrator_flag,
        descending,
        rows,
    )


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


def build_en_image_db_query(
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
