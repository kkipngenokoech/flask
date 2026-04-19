import os
import tempfile
import pytest
from flask import Flask


def mock_binary_loader(file_obj):
    """Mock loader that requires binary mode like tomllib.load"""
    if hasattr(file_obj, 'mode') and 'b' not in file_obj.mode:
        raise TypeError("File must be opened in binary mode, e.g. use `open('foo.toml', 'rb')`")
    # Simple mock parsing - just return a dict with uppercase keys
    content = file_obj.read()
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    return {'TEST_KEY': 'binary_mode_value'}


def test_issue_reproduction():
    """Test that from_file() fails when loader requires binary mode"""
    app = Flask(__name__)
    
    # Create a temporary TOML-like file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write('test_key = "binary_mode_value"\n')
        temp_file = f.name
    
    try:
        # This should fail because from_file opens in text mode but mock_binary_loader requires binary
        with pytest.raises(TypeError, match="File must be opened in binary mode"):
            app.config.from_file(os.path.basename(temp_file), mock_binary_loader)
    finally:
        os.unlink(temp_file)