from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic import Request, json
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.ticket_executor import TicketExecutor
from api.models.internal.jwt_data import JWT_Data


class TicketRef(HTTPMethodView):

    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, ref_id: int):
        ticket_executor = Mayim.get(TicketExecutor)

        try:
            ticket = await ticket_executor.get_ticket_by_refno(
                ref_id=ref_id, require_full=True
            )
        except RecordNotFound:
            if jwt_data.is_support() or jwt_data.is_admin():
                return json(
                    {
                        "error": "Not Found",
                        "message": "The requested ticket was not found",
                    },
                    status=404,
                )
            else:
                return json(
                    {
                        "error": "Forbidden",
                        "message": "You do not have permission to view this ticket",
                    },
                    status=403,
                )

        if (
            str(ticket.user.id) == jwt_data.uuid
            or jwt_data.is_support()
            or jwt_data.is_admin()
        ):
            return json(
                {
                    "status": "success",
                    **ticket.to_dict(),
                }
            )

        return json(
            {
                "error": "Forbidden",
                "message": "You do not have permission to view this ticket",
            },
            status=403,
        )
