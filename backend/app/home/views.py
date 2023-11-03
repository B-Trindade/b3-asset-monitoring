"""
Views for the simplified/provisory frontend.
"""
import requests

# from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core.models import Asset
from user.serializers import UserSerializer
from home.serializers import RegisterSerializer, LoginSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
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
    NEXT_PAGE = 'http://127.0.0.1:8000/select/'

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
                    token = Token.objects.get(user=user)

                    header = {'Authorization': f'Token {token}'}
                    return HttpResponse(
                        requests.get(self.NEXT_PAGE, headers=header)
                    )

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


# Currently not in use
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
    authentication_classes = [TokenAuthentication]
    LIST_ASSETS_URL = 'http://127.0.0.1:8000/api/asset/list/'

    def get(self, request):
        """Shows the list of valid symbols in the database."""

        token = Token.objects.get(user=request.user)
        header = {'Authorization': f'Token {token}'}
        res = requests.get(self.LIST_ASSETS_URL, headers=header)
        data = res.json()

        asset_list = []
        for dict in data:
            asset_list.append(dict.get('symbol'))

        return render(
            request,
            'home/asset_selection.html',
            {'asset_list': asset_list}
        )


class SubmitTunnelView(APIView):
    """View for submitting new tunnels."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        selected_assets = request.GET.getlist('asset_selection')
        return render(request, 'home/tunnel.html', {'assets': selected_assets})


def submitTunnelView(request):
    """View for submitting tunnels."""
    selected_assets = request.GET.getlist('asset_selection')
    return render(request, 'home/tunnel.html', {'assets': selected_assets})


def assetTrackerView(request):
    """View for visualizing user's assets data."""
    USER_SYMBOLS_API = 'http://127.0.0.1:8000/api/asset/me/'

    token = Token.objects.get_or_create(user=request.user.id)
    header = {'Authorization': f'Token {token}'}
    res = requests.get(USER_SYMBOLS_API, headers=header)
    data = res.json()

    user_assets = Asset.objects.filter(user=request.user.id)
    print(user_assets, request.user)
    print(data)
    return render(request, 'home/asset_tracker.html', {'assets': user_assets})
