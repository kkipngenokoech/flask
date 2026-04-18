import pytest
from flask import Blueprint

def test_issue_reproduction():
    """Test that creating a Blueprint with a dot in the name raises ValueError."""
    with pytest.raises(ValueError, match="Blueprint names should not contain dots"):
        Blueprint("my.blueprint", __name__)