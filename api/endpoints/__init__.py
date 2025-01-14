from api.app import appserver

from .api.admin.categories.manage import CategoriesManage
from .api.admin.categories.root import CategoriesRoot
from .api.admin.sla.manage import SLAManage
from .api.admin.sla.root import SLARoot
from .api.admin.staff import StaffRoot
from .api.admin.teams.manage import TeamManage
from .api.admin.teams.root import TeamRoot
from .api.auth.callback import AuthCallback
from .api.auth.entra import AuthEntra
from .api.me.create import MeCreate
from .api.me.register import MeRegister
from .api.me.root import MeRoot
from .api.options.category import CategoryOptions
from .api.options.severity import SeverityOptions
from .api.options.sla import SLAOptions
from .api.options.staff import StaffOptions
from .api.ping import Ping
from .api.tickets.info import TicketInfo
from .api.tickets.messages import TicketMessages
from .api.tickets.root import TicketRoot
from .api.tickets.status import TicketStatus

appserver.add_route(
    CategoriesManage.as_view(), "/api/admin/categories/<category_id:uuid>/manage"
)
appserver.add_route(CategoriesRoot.as_view(), "/api/admin/categories")
appserver.add_route(SLARoot.as_view(), "/api/admin/sla")
appserver.add_route(SLAManage.as_view(), "/api/admin/sla/<sla_id:uuid>/manage")
appserver.add_route(TeamRoot.as_view(), "/api/admin/teams")
appserver.add_route(TeamManage.as_view(), "/api/admin/teams/<team_id:uuid>/manage")
appserver.add_route(AuthCallback.as_view(), "/api/auth/callback")
appserver.add_route(AuthEntra.as_view(), "/api/auth/entra")
appserver.add_route(MeCreate.as_view(), "/api/me/create")
appserver.add_route(MeRegister.as_view(), "/api/me/register")
appserver.add_route(MeRoot.as_view(), "/api/me")
appserver.add_route(CategoryOptions.as_view(), "/api/options/category")
appserver.add_route(SeverityOptions.as_view(), "/api/options/severity")
appserver.add_route(SLAOptions.as_view(), "/api/options/sla")
appserver.add_route(Ping.as_view(), "/api/ping")
appserver.add_route(TicketInfo.as_view(), "/api/tickets/<ticket_id:uuid>")
appserver.add_route(TicketRoot.as_view(), "/api/tickets")
appserver.add_route(TicketMessages.as_view(), "/api/tickets/<ticket_id:uuid>/messages")
appserver.add_route(TicketStatus.as_view(), "/api/tickets/<ticket_id:uuid>/status")
appserver.add_route(StaffRoot.as_view(), "/api/admin/staff")
appserver.add_route(StaffOptions.as_view(), "/api/options/staff")
