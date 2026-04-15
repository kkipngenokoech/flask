import pytest

from flask import Blueprint
from flask import Flask


def test_blueprint_name_with_dot_raises_error():
    """Test that blueprint names containing dots raise ValueError."""
    with pytest.raises(ValueError, match="Blueprint names should not contain dots"):
        Blueprint("test.blueprint", __name__)


def test_blueprint_name_without_dot_works():
    """Test that blueprint names without dots work normally."""
    # This should not raise any error
    bp = Blueprint("test_blueprint", __name__)
    assert bp.name == "test_blueprint"


def test_blueprint_name_multiple_dots_raises_error():
    """Test that blueprint names with multiple dots raise ValueError."""
    with pytest.raises(ValueError, match="Blueprint names should not contain dots"):
        Blueprint("test.blueprint.name", __name__)


def test_blueprint_name_dot_at_start_raises_error():
    """Test that blueprint names starting with dot raise ValueError."""
    with pytest.raises(ValueError, match="Blueprint names should not contain dots"):
        Blueprint(".test_blueprint", __name__)


def test_blueprint_name_dot_at_end_raises_error():
    """Test that blueprint names ending with dot raise ValueError."""
    with pytest.raises(ValueError, match="Blueprint names should not contain dots"):
        Blueprint("test_blueprint.", __name__)


def test_blueprint_registration_with_valid_name():
    """Test that blueprints with valid names can be registered successfully."""
    app = Flask(__name__)
    bp = Blueprint("valid_name", __name__)
    
    @bp.route("/test")
    def test_route():
        return "test"
    
    # This should not raise any error
    app.register_blueprint(bp)
    assert "valid_name" in app.blueprints
