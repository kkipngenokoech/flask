import tempfile
import os
import flask

def test_issue_reproduction():
    """Test that from_file() fails when a loader requires binary mode."""
    
    # Create a simple binary loader that mimics tomllib.load behavior
    def binary_loader(file_handle):
        # This loader expects a binary file handle
        # It will fail if given a text file handle
        content = file_handle.read()
        if isinstance(content, str):
            raise TypeError("Expected binary file handle, got text")
        return {"TEST_KEY": "binary_value"}
    
    # Create a temporary file with some content
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
        f.write(b"dummy binary content")
        temp_file = f.name
    
    try:
        app = flask.Flask(__name__)
        # This should fail because from_file opens in text mode by default
        # but our binary_loader expects binary mode
        app.config.from_file(temp_file, load=binary_loader)
    finally:
        os.unlink(temp_file)