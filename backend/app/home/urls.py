"""
URL mappings for the home page API.
"""

from django.urls import path

from home import views


# Creates 'home' app name
app_name = 'home'

urlpatterns = [
    path('', views.assetSelection, name='assetSelection'),
    path('liveTracker/', views.assetTracker, name='assetTracker'),
    path('submitTunnels/', views.submitTunnel, name='submitTunnels'),
]
