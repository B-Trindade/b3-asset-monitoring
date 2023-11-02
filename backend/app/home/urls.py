"""
URL mappings for the home page API.
"""

from django.urls import path

from home import views


# Creates 'home' app name
app_name = 'home'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('select/', views.AssetSelectionView.as_view(), name='assetSelection'),
    path('submitTunnels/', views.submitTunnelView, name='submitTunnels'),
    path('liveTracker/', views.assetTrackerView, name='assetTracker'),
]
