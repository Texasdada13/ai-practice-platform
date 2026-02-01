"""
Input validation utilities for AI Practice Platform

Provides validation and sanitization for user inputs.
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from markupsafe import escape

from exceptions import (
    ValidationError,
    InvalidEmailError,
    InvalidSectorError,
    MissingFieldError
)


# Valid sectors (should match assessment.questions.SECTORS)
VALID_SECTORS = [
    'general', 'healthcare', 'financial', 'retail', 'manufacturing',
    'technology', 'government', 'education', 'energy', 'transportation'
]

# Email regex pattern (RFC 5322 simplified)
EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# Maximum field lengths
MAX_LENGTHS = {
    'name': 100,
    'email': 254,
    'organization': 200,
    'title': 100,
    'message': 10000,
    'custom_requirements': 5000
}


def sanitize_string(value: Any, max_length: Optional[int] = None) -> str:
    """
    Sanitize a string input to prevent XSS attacks.

    Args:
        value: Input value to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    if value is None:
        return ''

    # Convert to string and strip whitespace
    sanitized = str(value).strip()

    # Escape HTML characters
    sanitized = str(escape(sanitized))

    # Truncate if necessary
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def validate_email(email: str) -> str:
    """
    Validate and sanitize an email address.

    Args:
        email: Email address to validate

    Returns:
        Validated email address

    Raises:
        InvalidEmailError: If email format is invalid
    """
    sanitized = sanitize_string(email, MAX_LENGTHS['email']).lower()

    if not sanitized:
        raise MissingFieldError('email')

    if not EMAIL_PATTERN.match(sanitized):
        raise InvalidEmailError(sanitized)

    return sanitized


def validate_sector(sector: str) -> str:
    """
    Validate sector selection.

    Args:
        sector: Sector to validate

    Returns:
        Validated sector

    Raises:
        InvalidSectorError: If sector is not valid
    """
    sanitized = sanitize_string(sector, 50).lower()

    if not sanitized:
        return 'general'  # Default sector

    if sanitized not in VALID_SECTORS:
        raise InvalidSectorError(sanitized, VALID_SECTORS)

    return sanitized


def validate_name(name: str) -> str:
    """
    Validate and sanitize a name field.

    Args:
        name: Name to validate

    Returns:
        Validated name

    Raises:
        MissingFieldError: If name is empty
    """
    sanitized = sanitize_string(name, MAX_LENGTHS['name'])

    if not sanitized:
        raise MissingFieldError('name')

    return sanitized


def validate_organization(organization: str) -> str:
    """
    Validate and sanitize organization name.

    Args:
        organization: Organization name to validate

    Returns:
        Validated organization name

    Raises:
        MissingFieldError: If organization is empty
    """
    sanitized = sanitize_string(organization, MAX_LENGTHS['organization'])

    if not sanitized:
        raise MissingFieldError('organization')

    return sanitized


def validate_lead_data(form_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate all lead capture form data.

    Args:
        form_data: Dictionary containing form data

    Returns:
        Dictionary of validated and sanitized data

    Raises:
        ValidationError: If any field fails validation
    """
    errors = []
    validated = {}

    # Required fields
    try:
        validated['name'] = validate_name(form_data.get('name', ''))
    except ValidationError as e:
        errors.append(e)

    try:
        validated['email'] = validate_email(form_data.get('email', ''))
    except ValidationError as e:
        errors.append(e)

    try:
        validated['organization'] = validate_organization(form_data.get('organization', ''))
    except ValidationError as e:
        errors.append(e)

    # Optional fields
    validated['title'] = sanitize_string(
        form_data.get('title', ''),
        MAX_LENGTHS['title']
    )

    try:
        validated['sector'] = validate_sector(form_data.get('sector', 'general'))
    except ValidationError as e:
        errors.append(e)

    if errors:
        # Combine all errors
        error_messages = [e.message for e in errors]
        raise ValidationError(
            f"Validation failed: {'; '.join(error_messages)}",
            details={'errors': [e.to_dict() for e in errors]}
        )

    return validated


def validate_chat_message(message: str) -> str:
    """
    Validate and sanitize a chat message.

    Args:
        message: Chat message to validate

    Returns:
        Validated message

    Raises:
        ValidationError: If message is invalid
    """
    sanitized = sanitize_string(message, MAX_LENGTHS['message'])

    if not sanitized:
        raise ValidationError("Message cannot be empty", field='message')

    if len(sanitized) < 2:
        raise ValidationError("Message too short", field='message')

    return sanitized


def validate_assessment_responses(responses: Dict[str, Any]) -> Dict[str, int]:
    """
    Validate assessment question responses.

    Args:
        responses: Dictionary of question_id -> response_value

    Returns:
        Validated responses

    Raises:
        ValidationError: If responses are invalid
    """
    validated = {}

    for question_id, response in responses.items():
        # Sanitize question ID
        clean_id = sanitize_string(question_id, 50)

        # Validate response value (should be 1-5)
        try:
            value = int(response)
            if not 1 <= value <= 5:
                raise ValueError()
            validated[clean_id] = value
        except (ValueError, TypeError):
            raise ValidationError(
                f"Invalid response value for question {clean_id}",
                field=clean_id,
                details={'provided_value': response, 'expected_range': '1-5'}
            )

    return validated


def validate_document_type(doc_type: str, valid_types: List[str]) -> str:
    """
    Validate document type selection.

    Args:
        doc_type: Document type to validate
        valid_types: List of valid document types

    Returns:
        Validated document type

    Raises:
        ValidationError: If document type is invalid
    """
    sanitized = sanitize_string(doc_type, 50).lower()

    if sanitized not in valid_types:
        raise ValidationError(
            f"Invalid document type: {sanitized}",
            field='type',
            details={'valid_types': valid_types}
        )

    return sanitized


def validate_horizon(horizon: str) -> str:
    """
    Validate roadmap horizon selection.

    Args:
        horizon: Horizon to validate

    Returns:
        Validated horizon

    Raises:
        ValidationError: If horizon is invalid
    """
    valid_horizons = ['6 months', '12 months', '18 months', '24 months', '36 months']
    sanitized = sanitize_string(horizon, 20)

    if sanitized not in valid_horizons:
        raise ValidationError(
            f"Invalid horizon: {sanitized}",
            field='horizon',
            details={'valid_horizons': valid_horizons}
        )

    return sanitized


def validate_uuid(value: str, field_name: str = 'id') -> str:
    """
    Validate a UUID string.

    Args:
        value: UUID string to validate
        field_name: Name of the field for error messages

    Returns:
        Validated UUID string

    Raises:
        ValidationError: If UUID format is invalid
    """
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )

    sanitized = sanitize_string(value, 36).lower()

    if not uuid_pattern.match(sanitized):
        raise ValidationError(
            f"Invalid UUID format for {field_name}",
            field=field_name
        )

    return sanitized
