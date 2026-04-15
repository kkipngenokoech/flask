import tempfile
import os
import flask

def test_issue_reproduction():
    """Test that from_file fails when a binary mode loader is used with text mode file."""
    # Create a simple binary loader that expects a binary file handle
    def binary_loader(file_handle):
        # This will fail if file_handle is opened in text mode
        # because binary mode file handles have different methods/behavior
        try:
            # Try to read in binary mode - this should fail with text mode
            file_handle.mode
            if 'b' not in file_handle.mode:
                raise ValueError("Expected binary mode file handle")
            return {"TEST_KEY": "value"}
        except AttributeError:
            raise ValueError("File handle doesn't support binary operations")
    
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
        f.write("dummy content")
        temp_file = f.name
    
    try:
        app = flask.Flask(__name__)
        # This should fail because from_file opens in text mode but binary_loader expects binary mode
        app.config.from_file(temp_file, load=binary_loader)
        assert False, "Expected ValueError due to text mode vs binary mode mismatch"
    except ValueError as e:
        assert "binary" in str(e).lower()
    finally:
        os.unlink(temp_file)