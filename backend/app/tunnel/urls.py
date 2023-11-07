"""
URL routings for the tunnel app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from tunnel import views


router = DefaultRouter()
# Creates /api/tunnels/
router.register('tunnels', views.TunnelViewSet)

app_name = 'tunnel'

urlpatterns = [
    path('', include(router.urls)),
]
