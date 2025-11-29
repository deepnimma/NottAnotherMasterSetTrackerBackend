import responses
from util import Languages
import util


async def handle_pkmn_request(
    en_db,
    search_query: str,
    params: dict,
    lang: Languages,
) -> dict:
    """
    Handles a Pokemon request, for now it only handles English requests and is made with
    expansion to other languages in mind.
    :param lang: The language determines which table to make the request in.
    :param en_db: The ENGLISH DB to make the query to.
    :param search_query: The search query inputted by the user.
    :param params: The query params
    :return:
    """
    table_name = "image_metadata"
    if lang == Languages.EN:
        table_name = "image_metadata"

    pokemon_names = util.get_pokemon_names(search_query)

    # DB Query Flags
    cameo_flag = True if "cameo" in params else False
    trainer_flag = True if "trainer" in params else False
    illustrator_flag = True if "illustrator" in params else False
    descending = True if "descending" in params else False

    # Create en_db query
    db_query, db_params = build_image_db_query(
        table_name,
        pokemon_names,
        illustrator_flag,
        cameo_flag,
        trainer_flag,
        descending,
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
    )


def build_image_db_query(
    table_name: str,
    pokemon_names: list[str],
    illustrator: bool = False,
    cameo: bool = False,
    trainer: bool = False,
    descending: bool = False,
) -> tuple[str, list[str]]:
    base_query = f"SELECT * FROM {table_name} WHERE"

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
        params.append(f"%{name}%")
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
