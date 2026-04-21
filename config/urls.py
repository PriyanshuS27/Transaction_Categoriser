"""
URL configuration for transaction_categorizer project.
"""

from django.urls import path, include

urlpatterns = [
    path('api/', include('categorization.urls')),
]
