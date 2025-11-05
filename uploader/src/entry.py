from workers import Response, WorkerEntrypoint, Request
from router import handle_request
import logging

logger = logging.getLogger(__name__)


class Default(WorkerEntrypoint):
    async def fetch(self, request: Request):
        # logger.info("Received request.")
        # return await handle_request(request, self.env.UPLOADER_TOKEN)
        print("Received request.")

        form_data = await request.form_data()
        image_file = form_data.get("image")
        metadata_file = form_data.get("metadata")
        return await handle_request(request, self.env.UPLOADER_TOKEN)

        return Response("temp response.\n")
