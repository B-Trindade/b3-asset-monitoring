"""
URL mappings for the home page API.
"""

from django.urls import path

from home import views


# Creates 'home' app name
app_name = 'home'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.loginView, name='login'),
    path('select/', views.assetSelectionView, name='assetSelection'),
    path('liveTracker/', views.assetTrackerView, name='assetTracker'),
    path('submitTunnels/', views.submitTunnelView, name='submitTunnels'),
]
