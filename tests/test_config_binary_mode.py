import os
import tempfile
import pytest
from flask import Flask


def binary_loader(file_obj):
    """Simulates tomllib.load which requires binary mode"""
    # This will fail if file_obj is opened in text mode
    # because binary mode file objects have different methods
    if hasattr(file_obj, 'mode') and 'b' not in file_obj.mode:
        raise TypeError("File must be opened in binary mode, e.g. use `open('foo.toml', 'rb')`")
    return {'TEST_KEY': 'binary_value'}


def test_issue_reproduction():
    """Test that from_file fails when loader requires binary mode"""
    app = Flask(__name__)
    
    # Create a temporary TOML-like file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write('TEST_KEY = "binary_value"\n')
        temp_file = f.name
    
    try:
        # This should fail because from_file opens in text mode
        # but binary_loader (simulating tomllib.load) requires binary mode
        with pytest.raises(TypeError, match="File must be opened in binary mode"):
            app.config.from_file(os.path.basename(temp_file), binary_loader)
    finally:
        os.unlink(temp_file)