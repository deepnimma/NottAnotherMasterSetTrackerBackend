import responses
from util import Languages
import util


async def search_set(db, search_query: str, lang: Languages) -> dict:
    # Set table name based on language
    table_name = "image_metadata"
    if lang == Languages.EN:
        table_name = "image_metadata"

    sets = util.get_pokemon_names(search_query)
    search_query, search_params = build_set_query(table_name, sets)

    # Create STMT
    print(f"(EN) Making query: {search_query} with params: {search_params}")
    stmt = db.prepare(search_query)

    # Run Stmt
    response = await stmt.bind(*search_params).all()

    rows = response.results.to_py()

    return responses.build_response_dict(
        sets,
        rows,
        False,
        False,
        False,
        False,
        True,
    )


def build_set_query(table_name: str, sets: list[str]) -> tuple[str, list[str]]:
    base_query = f"SELECT * FROM {table_name} WHERE"

    new_sets = [sanitize_set_name(set) for set in sets]
    query_strs = [base_query]
    params = []

    for i, name in enumerate(new_sets):
        new_str = "OR " if i > 0 else ""
        new_str += f"setName LIKE ?"
        params.append(f"{name}")
        query_strs.append(new_str)

    # Add ordering string
    query_strs.append("ORDER BY releaseDate ASC, cardNumber ASC;")

    joined_query = " ".join(query_strs)

    return joined_query, params


def sanitize_set_name(set_name: str) -> str:
    set_name = set_name.lower()
    set_name = set_name.replace(" ", "-")

    return set_name
