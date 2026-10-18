from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/menu/", include("apps.menu.urls")),
    path("api/tables/", include("apps.tables.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/billing/", include("apps.billing.urls")),
    path("api/dashboard/", include("apps.dashboard.urls"))
]
