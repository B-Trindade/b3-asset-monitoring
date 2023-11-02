"""
Views for the simplified/provisory frontend.
"""
import requests

# from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core.models import Asset
from user.serializers import UserSerializer
from home.serializers import RegisterSerializer, LoginSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


CREATE_USER_URL = "http://localhost:8000/api/user/create/"
TOKEN_URL = "http://localhost:8000/api/user/token/"
# ME_URL = reverse('user:me')


class RegisterView(APIView):
    """View for registering new users."""
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    template_name = 'home/register.html'
    renderer_class = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/select')

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


class LoginView(APIView):
    """View for the login handle."""
    serializer_class = LoginSerializer
    template_name = 'home/login.html'
    renderer_class = [TemplateHTMLRenderer]

    def get(self, request):
        serializer = self.serializer_class()
        return render(request, self.template_name,
                      {'serializer': serializer})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = request.data['email']
            password = request.data['password']
            try:
                user = get_user_model().objects.get(email=email)
                payload = {
                    'email': email,
                    'password': password,
                }
                res = requests.post(TOKEN_URL, payload)
                if res.status_code == status.HTTP_200_OK:
                    Response({
                        'token': Token.objects.get(user=user),
                        'details': _('Login Successfull!')
                        }, status=status.HTTP_200_OK)

                    return redirect('home:assetSelection')

                return Response({'details': res.json()},
                                status=status.HTTP_400_BAD_REQUEST)
            except get_user_model().DoesNotExist:
                content = {
                    'details': _('User credentials incorrect.'),
                    'serializer': serializer.data
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return render(request, self.template_name,
                      {'serializer': serializer})


class LogoutView(APIView):
    """View for the log out handle."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Remove auth tokens for user."""
        tokens = Token.objects.filter(user=request.user)
        for token in tokens:
            token.delete()
        content = {'success': _('User signed out.')}
        Response(content, status=status.HTTP_200_OK)
        return redirect('/login')


class AssetSelectionView(APIView):
    """View for select assets based on symbols."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Shows the list of valid symbols in the database."""
        asset_list = Asset.objects.values_list('symbol', flat=True)
        # print(asset_list)
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
