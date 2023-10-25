"""
Views for the simplified/provisory home page.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

from core.models import Asset


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
