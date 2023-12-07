"""
URL mappings for the asset app.
"""

from django.urls import (
    path,
    # include,
)

# from rest_framework.routers import DefaultRouter

from asset import views

# router = DefaultRouter()
# # Creates /api/assets/
# router.register('assets', views.RetrieveAssetView)

app_name = 'asset'

urlpatterns = [
    # path('', include(router.urls)),
    path('database/<str:symbol>',
         views.RetrieveAssetView.as_view(), name='asset'),
    path('details/<str:symbol>',
         views.DetailedAssetView.as_view(), name='details'),
    path('list/', views.ListAssets.as_view(), name='list'),
]
