from workers import Response


async def handle(form_data, presets_db) -> Response:
    return Response("Temp Preset Response.")
