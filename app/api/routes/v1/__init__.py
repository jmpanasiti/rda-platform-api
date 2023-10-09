from fastapi import APIRouter

from .auth_routes import router as auth_router
from .branch_routes import router as branch_router
from .budget_routes import router as budget_router
from .my_bills_routes import router as my_bills_router
from .my_fleet_routes import router as my_fleet_router
from .my_report_routes import router as my_report_router
from .notification_routes import router as notifications_router
from .operations_routes import router as operations_router
from .organization_routes import router as organization_router
from .purchase_order_routes import router as purchase_order_router
from .request_routes import router as request_router
from .sinister_routes import router as sinister_router
from .user_routes import router as user_router
from .vehicle_routes import router as vehicle_router
from .work_order_routes import router as work_order_router

router_v1 = APIRouter(prefix='/v1')

router_v1.include_router(user_router, tags=['user'])
router_v1.include_router(auth_router, tags=['auth'])
router_v1.include_router(organization_router, tags=['organization'])
router_v1.include_router(branch_router, tags=['branch'])
router_v1.include_router(vehicle_router, tags=['vehicle'])
router_v1.include_router(my_fleet_router, tags=['my fleet'])
router_v1.include_router(work_order_router, tags=['work orders'])
router_v1.include_router(request_router, tags=['requests'])
router_v1.include_router(budget_router, tags=['budgets'])
router_v1.include_router(sinister_router, tags=['sinisters'])
router_v1.include_router(purchase_order_router, tags=['purchase orders'])
router_v1.include_router(my_bills_router, tags=['my bills'])
router_v1.include_router(operations_router, tags=['operations'])
router_v1.include_router(notifications_router, tags=['notifications'])
router_v1.include_router(my_report_router, tags=['my report'])
