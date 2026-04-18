import pytest

from flask import Blueprint
from flask import Flask


def test_blueprint_name_with_dot_raises_error():
    """Test that blueprint names containing dots raise ValueError."""
    with pytest.raises(ValueError, match="Blueprint names should not contain dots"):
        Blueprint("my.blueprint", __name__)


def test_blueprint_name_without_dot_works():
    """Test that blueprint names without dots work normally."""
    bp = Blueprint("my_blueprint", __name__)
    assert bp.name == "my_blueprint"


def test_blueprint_name_with_multiple_dots_raises_error():
    """Test that blueprint names with multiple dots raise ValueError."""
    with pytest.raises(ValueError, match="Blueprint names should not contain dots"):
        Blueprint("my.nested.blueprint", __name__)


def test_blueprint_name_empty_string_works():
    """Test that empty string blueprint names work."""
    bp = Blueprint("", __name__)
    assert bp.name == ""


def test_blueprint_name_with_underscore_works():
    """Test that blueprint names with underscores work normally."""
    bp = Blueprint("my_blueprint_name", __name__)
    assert bp.name == "my_blueprint_name"


def test_blueprint_name_with_dash_works():
    """Test that blueprint names with dashes work normally."""
    bp = Blueprint("my-blueprint-name", __name__)
    assert bp.name == "my-blueprint-name"


def test_blueprint_registration_with_valid_name():
    """Test that blueprints with valid names can be registered."""
    app = Flask(__name__)
    bp = Blueprint("valid_blueprint", __name__)
    
    @bp.route("/test")
    def test_route():
        return "test"
    
    app.register_blueprint(bp)
    assert "valid_blueprint" in app.blueprints
