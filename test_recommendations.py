import sys
from unittest.mock import MagicMock

# Mock dependencies before importing web_app
mock_flask = MagicMock()
sys.modules['flask'] = mock_flask
sys.modules['werkzeug'] = MagicMock()
sys.modules['werkzeug.utils'] = MagicMock()
sys.modules['requests'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['main_enhanced'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

import pytest
# Now we can import generate_recommendations
from web_app import generate_recommendations

def test_generate_recommendations_with_themes():
    insights = {
        'themes': ['Theme 1', 'Theme 2', 'Theme 3']
    }
    result = generate_recommendations(insights)

    assert "Based on the research findings, we recommend:" in result
    assert "1. Address the key finding: 'Theme 1'" in result
    assert "2. Address the key finding: 'Theme 2'" in result
    assert "3. Address the key finding: 'Theme 3'" in result
    assert "Next steps:" in result
    assert "• Validate findings with larger user group" in result

def test_generate_recommendations_empty_themes():
    insights = {
        'themes': []
    }
    result = generate_recommendations(insights)

    assert "Based on the research findings, we recommend:" in result
    assert "1. Address the key finding:" not in result
    assert "Next steps:" in result

def test_generate_recommendations_limit_top_3():
    insights = {
        'themes': ['Theme 1', 'Theme 2', 'Theme 3', 'Theme 4', 'Theme 5']
    }
    result = generate_recommendations(insights)

    assert "1. Address the key finding: 'Theme 1'" in result
    assert "2. Address the key finding: 'Theme 2'" in result
    assert "3. Address the key finding: 'Theme 3'" in result
    assert "4. Address the key finding: 'Theme 4'" not in result
    assert "5. Address the key finding: 'Theme 5'" not in result

def test_generate_recommendations_missing_themes_key():
    insights = {}
    result = generate_recommendations(insights)

    assert "Based on the research findings, we recommend:" in result
    assert "Next steps:" in result
    assert "1. Address the key finding:" not in result
