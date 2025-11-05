from workers import Response, WorkerEntrypoint, Request
from router import handle_request
import logging

logger = logging.getLogger(__name__)


class Default(WorkerEntrypoint):
    async def fetch(self, request: Request):
        print("Received request.")
        return await handle_request(request, self.env)
