import tempfile
import os
import flask

def test_issue_reproduction():
    """Test that from_file() fails when a loader requires binary mode."""
    
    # Create a simple binary loader that requires binary mode
    def binary_loader(file_handle):
        # This loader expects a binary file handle
        # It will fail if given a text file handle
        data = file_handle.read()
        if isinstance(data, str):
            raise TypeError("Expected binary data, got text")
        return {"TEST_KEY": "binary_value"}
    
    # Create a temporary file with some binary content
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
        f.write(b'\x00\x01\x02\x03')  # Some binary data
        temp_file = f.name
    
    try:
        app = flask.Flask(__name__)
        # This should fail because from_file() opens in text mode
        # but binary_loader expects binary mode
        app.config.from_file(temp_file, load=binary_loader)
    finally:
        os.unlink(temp_file)