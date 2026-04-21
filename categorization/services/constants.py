"""
Configuration constants for the categorization service.

Centralized configuration to avoid magic numbers and strings in code.
"""

# ============================================================================
# Groq API Configuration
# ============================================================================

# Model to use for categorization
DEFAULT_LLM_MODEL = "llama-3.1-8b-instant"

# API timeout in seconds
LLM_API_TIMEOUT = 30

# Maximum retries for transient failures
MAX_RETRIES = 3

# Base wait time for exponential backoff (seconds)
BASE_RETRY_DELAY = 1

# ============================================================================
# Categorization Configuration
# ============================================================================

# Confidence score thresholds
MIN_CONFIDENCE_THRESHOLD = 0.5
HIGH_CONFIDENCE_THRESHOLD = 0.8

# Maximum alternatives to suggest
MAX_ALTERNATIVES = 3

# Default number of historical examples to include in prompt
DEFAULT_HISTORICAL_EXAMPLES = 3

# ============================================================================
# Logging Configuration
# ============================================================================

# Log level for service operations
DEFAULT_LOG_LEVEL = "INFO"

# Whether to log full responses (set False for privacy)
LOG_FULL_RESPONSES = False
