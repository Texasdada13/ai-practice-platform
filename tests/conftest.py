"""
Pytest configuration and fixtures for AI Practice Platform tests.
"""

import os
import sys
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from web.app import app as flask_app


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    flask_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
        'SECRET_KEY': 'test-secret-key'
    })
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def sample_lead_data():
    """Sample lead data for testing."""
    return {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'organization': 'Test Corp',
        'title': 'CTO',
        'sector': 'technology'
    }


@pytest.fixture
def sample_assessment_responses():
    """Sample assessment responses for testing."""
    return {
        'strategy_q1': 3,
        'strategy_q2': 4,
        'strategy_q3': 2,
        'data_q1': 3,
        'data_q2': 4,
        'talent_q1': 2,
        'talent_q2': 3,
        'infrastructure_q1': 4,
        'infrastructure_q2': 3,
        'governance_q1': 2,
        'governance_q2': 3
    }
