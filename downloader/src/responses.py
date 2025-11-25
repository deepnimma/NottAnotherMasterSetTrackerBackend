def build_response_dict(
    pokemon_names: list[str],
    rows: list[dict],
    cameo_flag: bool,
    trainer_flag: bool,
    illustrator_flag: bool,
    descending_flag: bool,
    pokemon_rows: list[dict],
) -> dict:
    image_keys = []
    for row in pokemon_rows:
        image_keys.append(row.get("imageKey"))

    return {
        "requested_pokemon_num": len(pokemon_names),
        "requested_pokemon": pokemon_names,
        "parsed_pkmn_names": ", ".join(pokemon_names),
        "cameo_flag": cameo_flag,
        "trainer_flag": trainer_flag,
        "illustrator_flag": illustrator_flag,
        "descending_flag": descending_flag,
        "num_found": len(image_keys),
        "image_keys": image_keys,
        "image_rows": rows,
    }
