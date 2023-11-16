"""
URL mappings for the asset app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from asset import views


router = DefaultRouter()
# Creates /api/assets/
router.register('assets', views.AssetViewSet)

app_name = 'asset'

urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.ListAPIView.as_view(), name='list'),
]
