"""
Views for the simplified/provisory frontend.
"""
import requests

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from core.models import Asset
from user.serializers import UserSerializer
from home.serializers import RegisterSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


CREATE_USER_URL = "http://localhost:8000/api/user/create/"
# TOKEN_URL = reverse('user:token')
# ME_URL = reverse('user:me')


class RegisterView(APIView):
    """View for registering new users."""
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    template_name = 'home/register.html'  # TODO
    renderer_class = [TemplateHTMLRenderer]

    def get(self, request):
        serializer = RegisterSerializer()
        return render(request, self.template_name,
                      {'serializer': serializer})

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = request.data['email']
            password = request.data['password']
            name = request.data['name']

            try:
                user = get_user_model().objects.get(email=email)
                if user:
                    content = {
                        'serializer': serializer.data,
                        'detail': _('Email address already in use.')
                    }
                    return Response(
                        content,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except get_user_model().DoesNotExist:
                payload = {
                    'email': email,
                    'password': password,
                    'name': name
                }
                res = requests.post(CREATE_USER_URL, payload)
                if res.status_code == status.HTTP_201_CREATED:
                    content = {
                        'email': email,
                        'name': name,
                    }
                    return Response(content, status=status.HTTP_201_CREATED)
        content = {
            'serializer': serializer.data,
            'detail': _('Could not create user.'),
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


def loginView(request):
    """View for user login page."""
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            # Authenticate the user and log them in
            user = login_form.get_user()
            auth_login(request, user)  # Logs the user in
            # Redirect the user to their home page after login
            return redirect('home:assetSelection')
    else:
        login_form = AuthenticationForm()
    return render(request, 'home/login.html', {'login_form': login_form})


def assetSelectionView(request):
    """View for select assets based on symbols template."""
    asset_list = Asset.objects.values_list('symbol', flat=True)
    print(asset_list)
    return render(
        request,
        'home/asset_selection.html',
        {'asset_list': asset_list}
    )


def submitTunnelView(request):
    """View for submitting tunnels."""
    selected_assets = request.GET.getlist('asset_selection')
    print(selected_assets)
    return render(request, 'home/tunnel.html', {'assets': selected_assets})


def assetTrackerView(request):
    """View for visualizing user's assets data."""
    return render(request, 'home/asset_tracker.html')
