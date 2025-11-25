from enum import Enum


class Languages(Enum):
    EN = ("English",)
    JP = "Japanese"


def get_pokemon_names(secured_query_string: str) -> list[str]:
    pokemon_names = []
    if secured_query_string:
        new_name = secured_query_string.split(",")

        for name in new_name:
            stripped_name = name.strip()

            if stripped_name.endswith("-bsp"):
                stripped_name = stripped_name[:-4]
                stripped_name += "-black-star-promos"

            if stripped_name not in pokemon_names:
                pokemon_names.append(stripped_name)

            joined_name = " ".join(stripped_name.split("-"))
            if joined_name not in pokemon_names:
                pokemon_names.append(joined_name)

    return pokemon_names
