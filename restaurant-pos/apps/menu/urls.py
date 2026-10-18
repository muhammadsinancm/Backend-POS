from django.urls import path
from .views import MenuPermissionTestView
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet

urlpatterns = [
    path('permission-test/', MenuPermissionTestView.as_view(), name='menu-permission-test'),
]

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('items', MenuItemViewSet, basename='menu-item')

urlpatterns = router.urls