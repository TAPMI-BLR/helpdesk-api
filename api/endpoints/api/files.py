from datetime import timedelta
from uuid import UUID

from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic import Request, json
from sanic.views import HTTPMethodView

from api.app import HelpDesk
from api.decorators.require_login import require_login
from api.mayim.file_executor import FileExecutor
from api.mayim.ticket_executor import TicketExecutor
from api.models.enums import FileStorageType
from api.models.internal.jwt_data import JWT_Data


class Files(HTTPMethodView):
    @require_login()
    async def get(
        self, request: Request, jwt_data: JWT_Data, ticket_id: UUID, file_id: UUID
    ):
        file_executor = Mayim.get(FileExecutor)
        ticket_executor = Mayim.get(TicketExecutor)
        app: HelpDesk = request.app

        # Get Ticket by ID
        try:
            ticket = await ticket_executor.get_ticket_by_id(
                ticket_id, require_full=True
            )
        except RecordNotFound:
            return json(
                {
                    "error": "Ticket not found",
                    "message": "The requested ticket does not exist.",
                },
                404,
            )

        # Get File by ID
        try:
            file = await file_executor.get_file_by_id(ticket_id, file_id)
        except RecordNotFound:
            return json(
                {
                    "error": "File not found",
                    "message": "The requested file does not exist.",
                },
                404,
            )

        _, file_ext = file.file_name.rsplit(".", 1)

        path = f"tickets/{ticket_id}/{file_id}.{file_ext}"

        # Generate download link
        if file.storage_type == FileStorageType.MINIO:
            minio_client = app.get_minio_client()
            minio_inject = app.get_minio_inject(skip_host=False)

            # Generate download link
            download_link = await minio_client.presigned_get_object(
                object_name=path, expires=timedelta(minutes=5), **minio_inject
            )

            rsp = json(
                {
                    "status": "success",
                    "download_link": download_link,
                    "storage_type": "minio",
                },
                200,
            )

        elif file.storage_type == FileStorageType.ONEDRIVE:
            rsp = json(
                {"status": "error", "message": "OneDrive is not implemented"}, 500
            )

        else:
            rsp = json(
                {"status": "error", "message": "File storage type not supported"}, 500
            )

        # If user owns the ticket
        if str(ticket.user.id) == jwt_data.uuid:
            return rsp

        # If user is an admin
        elif jwt_data.is_admin():
            return rsp

        # If user is assigned to the ticket
        elif ticket.assignee.id == jwt_data.uuid:
            return rsp

        # If user is a team member
        elif jwt_data.is_support():
            return rsp

        else:
            return json(
                {
                    "error": "Unauthorized",
                    "message": "You are not authorized to access this file.",
                },
                403,
            )
