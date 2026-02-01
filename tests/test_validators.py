"""
Tests for input validation utilities.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from validators import (
    sanitize_string, validate_email, validate_sector, validate_name,
    validate_organization, validate_lead_data, validate_chat_message,
    validate_assessment_responses, validate_uuid
)
from exceptions import ValidationError, InvalidEmailError, InvalidSectorError, MissingFieldError


class TestSanitizeString:
    """Tests for sanitize_string function."""

    def test_basic_sanitization(self):
        """Test basic string sanitization."""
        result = sanitize_string("Hello World")
        assert result == "Hello World"

    def test_html_escape(self):
        """Test HTML characters are escaped."""
        result = sanitize_string("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_max_length(self):
        """Test string truncation."""
        result = sanitize_string("Hello World", max_length=5)
        assert result == "Hello"

    def test_none_input(self):
        """Test None input returns empty string."""
        result = sanitize_string(None)
        assert result == ""

    def test_whitespace_stripping(self):
        """Test whitespace is stripped."""
        result = sanitize_string("  Hello World  ")
        assert result == "Hello World"


class TestValidateEmail:
    """Tests for email validation."""

    def test_valid_email(self):
        """Test valid email passes."""
        result = validate_email("test@example.com")
        assert result == "test@example.com"

    def test_email_lowercase(self):
        """Test email is converted to lowercase."""
        result = validate_email("Test@Example.COM")
        assert result == "test@example.com"

    def test_invalid_email_no_at(self):
        """Test email without @ fails."""
        with pytest.raises(InvalidEmailError):
            validate_email("invalid-email")

    def test_invalid_email_no_domain(self):
        """Test email without domain fails."""
        with pytest.raises(InvalidEmailError):
            validate_email("test@")

    def test_empty_email(self):
        """Test empty email raises MissingFieldError."""
        with pytest.raises(MissingFieldError):
            validate_email("")


class TestValidateSector:
    """Tests for sector validation."""

    def test_valid_sector(self):
        """Test valid sector passes."""
        result = validate_sector("technology")
        assert result == "technology"

    def test_default_sector(self):
        """Test empty sector returns default."""
        result = validate_sector("")
        assert result == "general"

    def test_invalid_sector(self):
        """Test invalid sector raises error."""
        with pytest.raises(InvalidSectorError):
            validate_sector("invalid_sector")

    def test_sector_lowercase(self):
        """Test sector is converted to lowercase."""
        result = validate_sector("TECHNOLOGY")
        assert result == "technology"


class TestValidateName:
    """Tests for name validation."""

    def test_valid_name(self):
        """Test valid name passes."""
        result = validate_name("John Doe")
        assert result == "John Doe"

    def test_empty_name(self):
        """Test empty name raises error."""
        with pytest.raises(MissingFieldError):
            validate_name("")

    def test_name_sanitized(self):
        """Test name is sanitized."""
        result = validate_name("<b>John</b>")
        assert "<b>" not in result


class TestValidateLeadData:
    """Tests for lead data validation."""

    def test_valid_lead_data(self, sample_lead_data):
        """Test valid lead data passes."""
        result = validate_lead_data(sample_lead_data)
        assert result['name'] == sample_lead_data['name']
        assert result['email'] == sample_lead_data['email'].lower()
        assert result['organization'] == sample_lead_data['organization']

    def test_missing_required_fields(self):
        """Test missing required fields raises error."""
        with pytest.raises(ValidationError):
            validate_lead_data({'title': 'CTO'})

    def test_partial_data(self):
        """Test partial data raises error."""
        with pytest.raises(ValidationError):
            validate_lead_data({'name': 'John', 'email': 'invalid'})


class TestValidateChatMessage:
    """Tests for chat message validation."""

    def test_valid_message(self):
        """Test valid message passes."""
        result = validate_chat_message("Hello, how are you?")
        assert result == "Hello, how are you?"

    def test_empty_message(self):
        """Test empty message raises error."""
        with pytest.raises(ValidationError):
            validate_chat_message("")

    def test_too_short_message(self):
        """Test too short message raises error."""
        with pytest.raises(ValidationError):
            validate_chat_message("a")


class TestValidateAssessmentResponses:
    """Tests for assessment response validation."""

    def test_valid_responses(self):
        """Test valid responses pass."""
        responses = {'q1': 3, 'q2': 5, 'q3': 1}
        result = validate_assessment_responses(responses)
        assert result == responses

    def test_invalid_response_value(self):
        """Test invalid response value raises error."""
        with pytest.raises(ValidationError):
            validate_assessment_responses({'q1': 6})  # Out of range

    def test_non_numeric_response(self):
        """Test non-numeric response raises error."""
        with pytest.raises(ValidationError):
            validate_assessment_responses({'q1': 'not a number'})


class TestValidateUUID:
    """Tests for UUID validation."""

    def test_valid_uuid(self):
        """Test valid UUID passes."""
        uuid = "123e4567-e89b-12d3-a456-426614174000"
        result = validate_uuid(uuid)
        assert result == uuid.lower()

    def test_invalid_uuid(self):
        """Test invalid UUID raises error."""
        with pytest.raises(ValidationError):
            validate_uuid("not-a-uuid")
