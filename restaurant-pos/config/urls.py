from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/menu/", include("apps.menu.urls")),
    path("api/tables/", include("apps.tables.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/billing/", include("apps.billing.urls")),
    path("api/dashboard/", include("apps.dashboard.urls"))
]
