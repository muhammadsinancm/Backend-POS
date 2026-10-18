from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CurrentUserView, POSLoginView

urlpatterns = [
    path('login/', POSLoginView.as_view(), name='pos-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', CurrentUserView.as_view(), name='current-user')
]
