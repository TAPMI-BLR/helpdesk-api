from uuid import UUID

from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic import Request, json
from sanic.log import logger
from sanic.request import File
from sanic.views import HTTPMethodView
from sanic_ext import validate
from io import BytesIO

from api.app import HelpDesk
from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.file_executor import FileExecutor
from api.mayim.message_executor import MessageExecutor
from api.mayim.ticket_executor import TicketExecutor
from api.models.enums import FileStorageType, MessageType
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.message_form import MessageForm
from api.models.requests.message_query_params import MessageQueryParams


class TicketMessages(HTTPMethodView):
    @validate(query=MessageQueryParams)
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(
        self,
        request: Request,
        jwt_data: JWT_Data,
        ticket_id: UUID,
        query: MessageQueryParams,
    ):
        # Get query params
        limit = query.limit
        page = query.page

        # Ensure that both numbers are positive and in range
        try:
            assert limit > 0
            assert limit <= 50
            assert page >= 0
        except AssertionError:
            return json(
                {
                    "error": "Invalid parameters",
                    "message": (
                        "Limit must be a positive integer less than or equal to 50,"
                        " and page must be a non-negative integer."
                    ),
                },
                400,
            )

        # Get executors
        ticket_executor = Mayim.get(TicketExecutor)
        message_executor = Mayim.get(MessageExecutor)

        # Get Ticket by ID
        try:
            ticket = await ticket_executor.get_ticket_by_id(ticket_id)
        except RecordNotFound:
            return json(
                {
                    "error": "Ticket not found",
                    "message": "The requested ticket does not exist.",
                },
                404,
            )

        # Get Messages by Ticket ID
        offset = limit * page
        messages = await message_executor.get_messages(
            ticket_id, limit=limit, offset=offset
        )

        message = [msg.to_dict() for msg in messages]

        # If user owns the ticket
        if str(ticket.user_id) == jwt_data.uuid:
            return json({"status": "success", "messages": message}, 200)

        # If user is an admin
        elif jwt_data.is_admin():
            return json({"status": "success", "messages": message}, 200)

        # If user is assigned to the ticket
        elif ticket.assignee_id == jwt_data.uuid:
            return json({"status": "success", "messages": message}, 200)

        # If user is a team member
        elif jwt_data.is_support():
            return json({"status": "success", "messages": message}, 200)

        else:
            return json({"error": "Unauthorized"}, 403)

    @validate(form=MessageForm, body_argument="form")
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def post(
        self,
        request: Request,
        jwt_data: JWT_Data,
        ticket_id: UUID,
        form: MessageForm,
    ):
        # Get executors
        ticket_executor = Mayim.get(TicketExecutor)
        message_executor = Mayim.get(MessageExecutor)
        file_executor = Mayim.get(FileExecutor)

        # Get Ticket by ID
        try:
            ticket = await ticket_executor.get_ticket_by_id(ticket_id)
        except RecordNotFound:
            return json(
                {
                    "error": "Ticket not found",
                    "message": "The requested ticket does not exist.",
                },
                404,
            )

        # Check if user is allowed to post a message and set message type
        if str(ticket.user_id) == jwt_data.uuid:
            message_type = MessageType.USER
        elif jwt_data.is_admin() or jwt_data.is_support():
            message_type = MessageType.SUPPORT
        else:
            return json(
                {
                    "error": "Unauthorized",
                    "message": "You do not have permission to post a message on this ticket.",
                },
                403,
            )

        # Get message data
        message = form.content
        files = request.files.getlist("files")

        # Get the App instance
        app: HelpDesk = request.app

        # Ensure that either a message or a file is provided
        if not message and not files:
            return json(
                {
                    "error": "Invalid parameters",
                    "message": "Either a message or a file must be provided.",
                },
                400,
            )

        # Create a text message
        if message:
            try:
                await message_executor.create_text_message(
                    ticket_id=ticket_id,
                    user_id=jwt_data.uuid,
                    message=message,
                    message_type=message_type,
                )
            except Exception as e:
                logger.error(e)
                return json(
                    {
                        "error": "Internal Server Error",
                        "message": "An unexpected error occurred while creating the message.",
                    },
                    500,
                )

        # Upload the file and create a message with the file
        if files:
            # Check if all files are under a fixed size
            limit = app.config["MAX_FILE_SIZE"]

            if any(len(file.body) > limit for file in files):
                return json(
                    {
                        "error": "File too large",
                        "message": f"Files must be less than {limit} bytes.",
                    },
                    400,
                )

            for file in files:
                file: File
                # Extract file name and extension
                _, file_ext = file.name.rsplit(".", 1)

                file_id = await file_executor.add_file(
                    file_name=file.name,
                    storage_type=FileStorageType.MINIO,
                    file_type=file.type,
                )

                # Get MinIO Client
                minio_client = app.get_minio_client()
                inject = app.get_minio_inject()

                # Convert file to an in memory file cause of MinIO client
                file_body = BytesIO(file.body)

                # Upload file to MinIO
                try:
                    _ = await minio_client.put_object(
                        object_name=f"tickets/{ticket_id}/{file_id}.{file_ext}",
                        data=file_body,
                        length=len(file.body),
                        content_type=file.type,
                        **inject,
                    )
                except Exception as e:
                    logger.error(e)
                    await file_executor.delete_file(file_id)
                    return json(
                        {
                            "error": "Internal Server Error",
                            "message": "An unexpected error occurred while uploading the file.",
                        },
                        500,
                    )
                # Create message with file
                await message_executor.create_message_with_file_id(
                    ticket_id=ticket_id,
                    user_id=jwt_data.uuid,
                    file_id=file_id,
                    message_type=message_type,
                )

        return json({"status": "success"}, 200)
