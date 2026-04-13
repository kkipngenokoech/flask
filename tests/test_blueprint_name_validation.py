import pytest
import flask


def test_issue_reproduction():
    """Test that creating a blueprint with a dot in the name raises an error."""
    with pytest.raises(ValueError, match="Blueprint names should not contain dots"):
        flask.Blueprint("my.blueprint", __name__)