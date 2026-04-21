"""
Unit tests for LLM wrapper module.

Tests the GroqProvider and LLMWrapper classes with various scenarios
including happy paths, error cases, and edge cases.
"""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock

from categorization.services.llm_wrapper import LLMProvider, GroqProvider, LLMWrapper
from categorization.exceptions import LLMException, ConfigurationException


class TestGroqProvider(unittest.TestCase):
    """Test cases for GroqProvider class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test-groq-key-123"

    def test_init_with_valid_api_key(self):
        """Test provider initialization with valid API key."""
        with patch('categorization.services.llm_wrapper.Groq'):
            provider = GroqProvider(api_key=self.api_key)
            self.assertIsNotNone(provider.client)
            self.assertEqual(provider.model, "llama-3.1-8b-instant")

    def test_init_with_env_variable(self):
        """Test provider initialization from environment variable."""
        with patch.dict(os.environ, {'GROQ_API_KEY': self.api_key}):
            with patch('categorization.services.llm_wrapper.Groq'):
                provider = GroqProvider()
                self.assertIsNotNone(provider)

    def test_init_missing_api_key(self):
        """Test that ConfigurationException is raised when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigurationException):
                GroqProvider(api_key=None)

    def test_init_empty_api_key(self):
        """Test that ConfigurationException is raised when API key is empty."""
        with self.assertRaises(ConfigurationException):
            GroqProvider(api_key="")

    def test_generate_response_success(self):
        """Test successful response generation."""
        with patch('categorization.services.llm_wrapper.Groq') as mock_groq:
            # Setup mock
            mock_client = MagicMock()
            mock_groq.return_value = mock_client
            mock_response = MagicMock()
            mock_response.choices[0].message.content = "Software & Subscriptions"
            mock_client.chat.completions.create.return_value = mock_response

            provider = GroqProvider(api_key=self.api_key)
            result = provider.generate_response("Test prompt")

            self.assertEqual(result, "Software & Subscriptions")
            mock_client.chat.completions.create.assert_called_once()

    def test_generate_response_empty_prompt(self):
        """Test that LLMException is raised for empty prompt."""
        with patch('categorization.services.llm_wrapper.Groq'):
            provider = GroqProvider(api_key=self.api_key)
            
            with self.assertRaises(LLMException):
                provider.generate_response("")

    def test_generate_response_empty_result(self):
        """Test handling of empty response from API."""
        with patch('categorization.services.llm_wrapper.Groq') as mock_groq:
            mock_client = MagicMock()
            mock_groq.return_value = mock_client
            mock_response = MagicMock()
            mock_response.choices[0].message.content = None
            mock_client.chat.completions.create.return_value = mock_response

            provider = GroqProvider(api_key=self.api_key)
            
            with self.assertRaises(LLMException):
                provider.generate_response("Test prompt")

    @patch('categorization.services.llm_wrapper.time.sleep')
    def test_generate_response_retry_logic(self, mock_sleep):
        """Test retry logic for transient failures."""
        with patch('categorization.services.llm_wrapper.Groq') as mock_groq:
            mock_client = MagicMock()
            mock_groq.return_value = mock_client
            
            # Fail twice, succeed on third attempt
            mock_response = MagicMock()
            mock_response.choices[0].message.content = "Success"
            mock_client.chat.completions.create.side_effect = [
                Exception("Connection error"),
                Exception("Timeout"),
                mock_response
            ]

            provider = GroqProvider(api_key=self.api_key)
            result = provider.generate_response("Test prompt")

            self.assertEqual(result, "Success")
            # Should have called sleep twice (for 2 retries)
            self.assertEqual(mock_sleep.call_count, 2)


class TestLLMWrapper(unittest.TestCase):
    """Test cases for LLMWrapper class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_provider = Mock(spec=LLMProvider)

    def test_init_with_valid_provider(self):
        """Test wrapper initialization with valid provider."""
        wrapper = LLMWrapper(self.mock_provider)
        self.assertEqual(wrapper.provider, self.mock_provider)

    def test_init_with_invalid_provider(self):
        """Test that ValueError is raised for invalid provider."""
        with self.assertRaises(ValueError):
            LLMWrapper(None)

        with self.assertRaises(ValueError):
            LLMWrapper("not a provider")

    def test_categorize_success(self):
        """Test successful categorization."""
        self.mock_provider.generate_response.return_value = '{"suggested_category": "Office Supplies"}'
        wrapper = LLMWrapper(self.mock_provider)

        result = wrapper.categorize("Test prompt")

        self.assertEqual(result, '{"suggested_category": "Office Supplies"}')
        self.mock_provider.generate_response.assert_called_once()

    def test_categorize_empty_prompt(self):
        """Test that ValueError is raised for empty prompt."""
        wrapper = LLMWrapper(self.mock_provider)

        with self.assertRaises(ValueError):
            wrapper.categorize("")

    def test_categorize_propagates_llm_exception(self):
        """Test that LLMException is propagated."""
        self.mock_provider.generate_response.side_effect = LLMException("API failed")
        wrapper = LLMWrapper(self.mock_provider)

        with self.assertRaises(LLMException):
            wrapper.categorize("Test prompt")

    def test_categorize_with_request_id(self):
        """Test categorization with request ID for tracing."""
        self.mock_provider.generate_response.return_value = "Success"
        wrapper = LLMWrapper(self.mock_provider)

        result = wrapper.categorize("Test prompt", request_id="req-123")

        self.assertEqual(result, "Success")
        # Verify request_id was passed to provider
        call_args = self.mock_provider.generate_response.call_args
        self.assertEqual(call_args[1].get('request_id'), 'req-123')


class TestLLMProviderInterface(unittest.TestCase):
    """Test cases for LLMProvider ABC interface."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that LLMProvider cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            LLMProvider()

    def test_subclass_must_implement_generate_response(self):
        """Test that subclasses must implement generate_response."""
        class IncompleteLLMProvider(LLMProvider):
            pass

        with self.assertRaises(TypeError):
            IncompleteLLMProvider()


if __name__ == '__main__':
    unittest.main()
