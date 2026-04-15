import pytest
from flask import Blueprint

def test_issue_reproduction():
    """Test that blueprint names containing dots should raise ValueError."""
    # This should raise an error but currently doesn't
    with pytest.raises(ValueError, match="Blueprint names should not contain dots"):
        Blueprint("my.blueprint", __name__)