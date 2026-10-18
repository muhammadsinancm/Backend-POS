from django.urls import path
from .views import MenuPermissionTestView

urlpatterns = [
    path('permission-test/', MenuPermissionTestView.as_view(), name='menu-permission-test')
]
