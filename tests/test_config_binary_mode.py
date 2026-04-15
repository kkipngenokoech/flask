import tempfile
import os
import flask

def test_issue_reproduction():
    """Test that from_file fails when loader expects binary mode but file is opened in text mode."""
    
    # Create a simple binary loader that expects a binary file handle
    def binary_loader(file_handle):
        # This will fail if file_handle is in text mode
        # because binary mode file handles have .mode attribute as 'rb'
        # and text mode handles have .mode as 'r'
        if hasattr(file_handle, 'mode') and 'b' not in file_handle.mode:
            raise ValueError("Expected binary mode file handle")
        return {"TEST_KEY": "binary_value"}
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
        f.write(b"dummy binary content")
        temp_filename = f.name
    
    try:
        app = flask.Flask(__name__)
        # This should fail because from_file opens in text mode by default
        # but our binary_loader expects binary mode
        app.config.from_file(temp_filename, load=binary_loader)
    finally:
        os.unlink(temp_filename)