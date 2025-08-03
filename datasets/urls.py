from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, ColumnMetadataViewSet
router = DefaultRouter()
router.register('datasets', DatasetViewSet, basename='dataset')
router.register('columns', ColumnMetadataViewSet, basename='columnmetadata')

from .views import DatasetViewSet
from django.urls import path, include

from .views import DatasetViewSet, ColumnMetadataViewSet

router = DefaultRouter()
router.register('datasets', DatasetViewSet, basename='dataset')
router.register('columns', ColumnMetadataViewSet, basename='columnmetadata')

urlpatterns = [
    path('', include(router.urls)),
]
