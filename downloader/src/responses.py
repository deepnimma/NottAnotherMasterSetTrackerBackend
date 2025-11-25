def build_response_dict(
    pokemon_names: list[str],
    rows: list[dict],
    cameo_flag: bool = False,
    trainer_flag: bool = False,
    illustrator_flag: bool = False,
    descending_flag: bool = False,
    set_flag: bool = False,
) -> dict:
    image_keys = []
    for row in rows:
        image_keys.append(row.get("imageKey"))

    return {
        "requested_pokemon_num": len(pokemon_names),
        "requested_pokemon": pokemon_names,
        "parsed_pkmn_names": ", ".join(pokemon_names),
        "cameo_flag": cameo_flag,
        "trainer_flag": trainer_flag,
        "illustrator_flag": illustrator_flag,
        "descending_flag": descending_flag,
        "set_flag": set_flag,
        "num_found": len(image_keys),
        "image_keys": image_keys,
        "image_rows": rows,
    }
