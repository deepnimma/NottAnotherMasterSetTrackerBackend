from workers import Response, WorkerEntrypoint

from downloader.src.database import handle_request
from submodule import get_hello_message


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await handle_request(request, self.env)
