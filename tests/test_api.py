"""
Tests for API endpoints.
"""

import pytest
import json


class TestHealthEndpoints:
    """Tests for health and status endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint returns healthy status."""
        response = client.get('/health')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'services' in data
        assert 'stats' in data
        assert 'version' in data

    def test_api_status(self, client):
        """Test API status endpoint."""
        response = client.get('/api/status')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'operational'
        assert 'endpoints' in data


class TestIndexPage:
    """Tests for the index page."""

    def test_index_page_loads(self, client):
        """Test index page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_contains_form(self, client):
        """Test index page contains assessment form."""
        response = client.get('/')
        assert b'form' in response.data.lower()

    def test_index_contains_demo_button(self, client):
        """Test index page contains demo mode button."""
        response = client.get('/')
        assert b'demo' in response.data.lower()


class TestDemoMode:
    """Tests for demo mode functionality."""

    def test_demo_mode_redirects_to_dashboard(self, client):
        """Test demo mode route redirects to dashboard."""
        response = client.get('/demo', follow_redirects=False)
        assert response.status_code == 302
        assert '/dashboard' in response.location

    def test_demo_mode_sets_session(self, client):
        """Test demo mode creates session with assessment data."""
        # Follow redirect to dashboard
        response = client.get('/demo', follow_redirects=True)
        assert response.status_code == 200

        # Check session has expected values
        with client.session_transaction() as sess:
            assert 'assessment_id' in sess
            assert 'organization' in sess
            assert sess['organization'] == 'Demo Corporation'
            assert sess['is_demo'] == True

    def test_demo_mode_allows_access_to_features(self, client):
        """Test demo mode allows access to all feature pages."""
        # Enter demo mode
        client.get('/demo', follow_redirects=True)

        # Test access to various pages
        pages = ['/dashboard', '/chat', '/frameworks', '/roadmap', '/use-cases', '/documents']
        for page in pages:
            response = client.get(page)
            assert response.status_code == 200, f"Failed to access {page}"

    def test_demo_mode_chat_session_starts(self, client):
        """Test chat session can be started in demo mode."""
        # Enter demo mode
        client.get('/demo', follow_redirects=True)

        # Start chat session
        response = client.post('/api/chat/start',
                               data=json.dumps({'mode': 'general'}),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'session_id' in data
        assert 'suggested_prompts' in data

    def test_demo_mode_chat_streaming_works(self, client):
        """Test streaming chat works in demo mode."""
        # Enter demo mode
        client.get('/demo', follow_redirects=True)

        # Start chat session
        client.post('/api/chat/start',
                    data=json.dumps({'mode': 'general'}),
                    content_type='application/json')

        # Send a streaming message
        response = client.post('/api/chat/stream',
                               data=json.dumps({'message': 'Tell me about AI strategy'}),
                               content_type='application/json')
        assert response.status_code == 200
        assert 'text/event-stream' in response.content_type

        # Verify we get some response data
        data = response.get_data(as_text=True)
        assert 'data:' in data  # SSE format


class TestAssessmentFlow:
    """Tests for assessment flow."""

    def test_start_assessment_valid(self, client, sample_lead_data):
        """Test starting assessment with valid data."""
        response = client.post('/start', data=sample_lead_data, follow_redirects=False)
        # Should redirect to assessment page
        assert response.status_code == 302
        assert '/assessment' in response.location

    def test_start_assessment_invalid_email(self, client, sample_lead_data):
        """Test starting assessment with invalid email."""
        sample_lead_data['email'] = 'invalid-email'
        response = client.post('/start', data=sample_lead_data)
        assert response.status_code == 400

    def test_start_assessment_missing_name(self, client, sample_lead_data):
        """Test starting assessment without name."""
        del sample_lead_data['name']
        response = client.post('/start', data=sample_lead_data)
        assert response.status_code == 400

    def test_assessment_page_requires_session(self, client):
        """Test assessment page requires active session."""
        response = client.get('/assessment', follow_redirects=False)
        assert response.status_code == 302
        assert '/' in response.location

    def test_results_page_requires_session(self, client):
        """Test results page requires active session."""
        response = client.get('/results', follow_redirects=False)
        assert response.status_code == 302


class TestChatAPI:
    """Tests for chat API endpoints."""

    def test_chat_start_requires_session(self, client):
        """Test chat start requires assessment session."""
        response = client.post('/api/chat/start',
                               data=json.dumps({'mode': 'general'}),
                               content_type='application/json')
        # Without session, should still work but with limited context
        assert response.status_code == 200

    def test_chat_message_requires_session(self, client):
        """Test chat message requires chat session."""
        response = client.post('/api/chat/message',
                               data=json.dumps({'message': 'Hello'}),
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_chat_message_validation(self, client):
        """Test chat message validation (empty message)."""
        with client.session_transaction() as sess:
            sess['chat_session_id'] = 'test-session-id'

        response = client.post('/api/chat/message',
                               data=json.dumps({'message': ''}),
                               content_type='application/json')
        assert response.status_code == 400

    def test_chat_stream_requires_session(self, client):
        """Test streaming chat requires chat session."""
        response = client.post('/api/chat/stream',
                               data=json.dumps({'message': 'Hello'}),
                               content_type='application/json')
        assert response.status_code == 400

    def test_chat_stream_endpoint_exists(self, client, sample_lead_data):
        """Test streaming endpoint returns SSE response."""
        # Start assessment to get session
        client.post('/start', data=sample_lead_data, follow_redirects=True)

        # Start chat session
        client.post('/api/chat/start',
                    data=json.dumps({'mode': 'general'}),
                    content_type='application/json')

        # Test streaming endpoint
        response = client.post('/api/chat/stream',
                               data=json.dumps({'message': 'Hello'}),
                               content_type='application/json')
        assert response.status_code == 200
        assert 'text/event-stream' in response.content_type


class TestFrameworksAPI:
    """Tests for framework generation API."""

    def test_frameworks_page_requires_session(self, client):
        """Test frameworks page requires session."""
        response = client.get('/frameworks', follow_redirects=False)
        assert response.status_code == 302

    def test_strategy_generation(self, client, sample_lead_data):
        """Test strategy framework generation."""
        # First start an assessment
        client.post('/start', data=sample_lead_data, follow_redirects=True)

        response = client.post('/api/frameworks/strategy',
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        # Check for expected strategy components
        assert 'executive_summary' in data or 'business_case' in data or 'pillars' in data


class TestDocumentsAPI:
    """Tests for document generation API."""

    def test_documents_page_requires_session(self, client):
        """Test documents page requires session."""
        response = client.get('/documents', follow_redirects=False)
        assert response.status_code == 302


class TestErrorHandling:
    """Tests for error handling."""

    def test_404_html(self, client):
        """Test 404 returns HTML for browser requests."""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404

    def test_404_api(self, client):
        """Test 404 returns JSON for API requests."""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['code'] == 'NOT_FOUND'
