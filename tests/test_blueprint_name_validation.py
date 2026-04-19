import pytest
import flask

def test_issue_reproduction():
    """Test that blueprint names containing dots should raise an error."""
    # This should raise an error but currently doesn't
    with pytest.raises(AssertionError, match="Blueprint name should not contain dots"):
        flask.Blueprint("my.blueprint", __name__)