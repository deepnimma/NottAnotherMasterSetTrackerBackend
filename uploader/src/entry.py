from workers import Response, WorkerEntrypoint, Request
from router import handle_request
import logging

logger = logging.getLogger(__name__)


class Default(WorkerEntrypoint):
    async def fetch(self, request: Request):
        logger.info("Received request.")
        return await handle_request(request, self.env.UPLOADER_TOKEN)
