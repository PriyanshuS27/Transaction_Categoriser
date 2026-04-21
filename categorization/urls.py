"""
URL configuration for categorization app.
"""

from django.urls import path
from categorization.views import CategorizationView

urlpatterns = [
    path('categorize/', CategorizationView.as_view(), name='categorize'),
]
