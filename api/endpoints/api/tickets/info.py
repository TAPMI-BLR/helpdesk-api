from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic import Request, json
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.ticket_executor import TicketExecutor
from api.models.internal.jwt_data import JWT_Data


class TicketInfo(HTTPMethodView):
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, ticket_id: int):
        executor = Mayim.get(TicketExecutor)
        try:
            ticket = await executor.get_full_ticket_by_id(ticket_id)
        except RecordNotFound:
            return json(
                {"error": "Not Found", "message": "The requested ticket was not found"},
                status=404,
            )

        if (
            str(ticket.user.id) == jwt_data.uuid
            or jwt_data.is_support()
            or jwt_data.is_admin()
        ):
            return json({"status": "success", "ticket": ticket.to_dict()})

        return json(
            {
                "error": "Forbidden",
                "message": "You do not have permission to view this ticket",
            },
            status=403,
        )

    @require_login()
    @require_role(required_role="user", allow_higher=True)
    # TODO - Validate via class
    async def post(self, request: Request, jwt_data: JWT_Data, ticket_id: int):
        # executor = Mayim.get(TicketExecutor)
        # try:
        #     ticket = await executor.get_ticket_by_id(ticket_id)
        # except RecordNotFound:
        #     return json(
        #         {"error": "Not Found", "message": "The requested ticket was not found"},
        #         status=404,
        #     )
        # if (
        #     ticket.user_id == jwt_data.uuid
        #     or jwt_data.is_support()
        #     or jwt_data.is_admin()
        # ):
        #     # TODO - Carry out the updates
        #     return json({"status": "success"})

        # return json(
        #     {
        #         "error": "Forbidden",
        #         "message": "You do not have permission to update this ticket",
        #     },
        #     status=403,
        # )

        return json({"error": "Not Implemented"}, status=501)
