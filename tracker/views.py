from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse


def health_check(request):
    """Simple API health check endpoint."""
    return JsonResponse(
        {
            "status": "healthy",
            "service": "Workload Tracker",
            "version": "1.0.0",
        }
    )
