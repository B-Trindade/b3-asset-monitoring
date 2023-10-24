"""
Views for the simplified/provisory home page.
"""

from django.shortcuts import render


def assetSelection(request):
    """View for select assets based on symbols template."""
    return render(request, 'home/asset_selection.html')


def assetTracker(request):
    """View for visualizing user's assets data."""
    return render(request, 'home/asset_tracker.html')
