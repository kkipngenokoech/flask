import pytest
from flask import Blueprint

def test_issue_reproduction():
    """Test that creating a Blueprint with a dot in the name raises ValueError."""
    # This should raise an error since blueprint names should not contain dots
    # due to the significance of dots in nested blueprint naming
    with pytest.raises(ValueError, match="Blueprint name should not contain dots"):
        Blueprint("my.blueprint", __name__)