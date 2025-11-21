from workers import Response, WorkerEntrypoint

from database import handle_request

"""
Example query uRL

https://downloader.com/pokemon?name=charizard,pikachu&cameo&reverse&trainer
"""


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await handle_request(request, self.env.tcg_image_metadata_db)
