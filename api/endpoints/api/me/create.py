from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from api.decorators.require_role import require_role
from api.decorators.require_login import require_login
from api.mayim.message_executor import MessageExecutor
from api.mayim.system_executor import SystemExecutor
from api.mayim.ticket_executor import TicketExecutor
from api.models.enums import MessageType
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.ticket_form import TicketForm


class MeCreate(HTTPMethodView):
    # TODO
    @validate(form=TicketForm)
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def post(self, request: Request, jwt_data: JWT_Data):
        # Get Ticket and Message Executors
        ticket_executor = Mayim.get(TicketExecutor)
        message_executor = Mayim.get(MessageExecutor)
        system_executor = Mayim.get(SystemExecutor)

        # Get the data from the request
        subcategory_id = request.form.get("subcategory_id")
        inital_msg = request.form.get("inital_message")
        title = request.form.get("title")

        # Ensure Data is not Empty
        if not subcategory_id:
            return json({"error": "Category ID cannot be empty"}, 400)
        if not title:
            return json({"error": "Title cannot be empty"}, 400)
        if not inital_msg:
            return json({"error": "Inital Message cannot be empty"}, 400)

        # Get the default config
        default_config = await system_executor.get_default_ticket_config()

        # Create the Ticket
        ticket = await ticket_executor.create_ticket(
            user_id=jwt_data.uuid,
            subcategory_id=subcategory_id,
            title=title,
            config=default_config,
        )

        # Create the Messages
        # System Notification of User created ticket
        await message_executor.create_text_message(
            ticket_id=ticket.id,
            user_id=jwt_data.uuid,
            message=f"Ticket Created by {jwt_data.name}",
            message_type=MessageType.SYSTEM,
        )
        # Inital Message (provided by user)
        await message_executor.create_text_message(
            ticket_id=ticket.id,
            user_id=jwt_data.uuid,
            message=inital_msg,
            message_type=MessageType.USER,
        )
        # Message that assigns the ticket to the sys_admin
        await message_executor.create_text_message(
            ticket_id=ticket.id,
            user_id=jwt_data.uuid,
            message="Ticket Assigned to Admin",
            message_type=MessageType.SYSTEM,
        )

        # Return the Ticket
        return json({"status": "success", "data": ticket.to_dict()})
