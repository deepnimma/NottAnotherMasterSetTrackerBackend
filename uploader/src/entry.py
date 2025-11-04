from workers import Response, WorkerEntrypoint
from submodule import get_hello_message

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response(self.env.UPLOADER_SECRET)
