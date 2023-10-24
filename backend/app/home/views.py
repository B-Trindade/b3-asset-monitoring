"""
Views for the simplified/provisory home page.
"""

from django.shortcuts import render

from core.models import Asset


def assetSelection(request):
    """View for select assets based on symbols template."""
    asset_list = Asset.objects.values_list('symbol', flat=True)
    print(asset_list)
    return render(
        request,
        'home/asset_selection.html',
        {'asset_list': asset_list}
    )


def assetTracker(request):
    """View for visualizing user's assets data."""
    return render(request, 'home/asset_tracker.html')


def submitTunnel(request):
    """View for submitting tunnels."""
    selected_assets = request.GET.getlist('asset_selection')
    print(selected_assets)
    return render(request, 'home/tunnel.html', {'assets': selected_assets})
