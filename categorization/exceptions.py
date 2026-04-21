"""
Exception classes and handler for the API.

This module provides custom exception types for better error handling
and an API exception handler for DRF integration.
"""

import logging
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


# ============================================================================
# Custom Exception Classes
# ============================================================================

class CategorizationException(Exception):
    """Base exception for categorization service."""
    pass


class LLMException(CategorizationException):
    """Raised when LLM API call fails."""
    pass


class ConfigurationException(CategorizationException):
    """Raised when service configuration is invalid."""
    pass


class ValidationException(CategorizationException):
    """Raised when input validation fails."""
    pass


class ResponseParsingException(CategorizationException):
    """Raised when LLM response parsing fails."""
    pass


# ============================================================================
# Exception Handler
# ============================================================================


def custom_exception_handler(exc, context):
    """
    Custom exception handler for API views.
    
    Args:
        exc: The exception raised
        context: The context where the exception occurred
        
    Returns:
        Response object with error details
    """
    # Call the default DRF exception handler
    response = exception_handler(exc, context)

    if response is None:
        # Log unexpected exceptions
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return Response(
            {
                'status': 'error',
                'message': 'An unexpected error occurred. Please try again later.'
            },
            status=500
        )

    # Log validation and other errors
    logger.warning(f"API exception: {str(exc)}")

    # Return the existing response
    return response
