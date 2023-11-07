"""
URL mappings for the user API.
"""

from django.urls import path

from user import views


# Creates 'user' app name for paths such as " 'user:create' ".
app_name = 'user'

# WARNING: Currently token authentication is disabled.
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    # path('token/', views.CreateTokenView.as_view(), name='token'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
