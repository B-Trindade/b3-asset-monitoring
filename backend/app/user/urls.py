"""
URL mappings for the user API.
"""

from django.urls import path

from user import views


# Creates 'user' app name for paths such as " 'user:create' ".
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
