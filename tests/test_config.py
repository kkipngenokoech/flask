import os
import tempfile
import pytest
from flask import Flask
from flask.config import Config


class TestConfigFromEnvvar:
    def test_from_envvar_absolute_path(self):
        """Test from_envvar with absolute path."""
        app = Flask(__name__)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('TEST_VALUE = "absolute_path"\n')
            config_file = f.name
        
        try:
            os.environ['TEST_CONFIG'] = config_file
            result = app.config.from_envvar('TEST_CONFIG')
            
            assert result is True
            assert app.config['TEST_VALUE'] == 'absolute_path'
        finally:
            os.environ.pop('TEST_CONFIG', None)
            os.unlink(config_file)
    
    def test_from_envvar_relative_path(self):
        """Test from_envvar with relative path resolves to instance folder."""
        app = Flask(__name__)
        
        # Create instance directory
        instance_dir = os.path.join(app.root_path, 'instance')
        os.makedirs(instance_dir, exist_ok=True)
        
        # Create config file in instance directory
        config_file = os.path.join(instance_dir, 'test_config.py')
        with open(config_file, 'w') as f:
            f.write('TEST_VALUE = "relative_path"\n')
        
        try:
            # Set environment variable to relative path
            os.environ['TEST_CONFIG'] = 'test_config.py'
            result = app.config.from_envvar('TEST_CONFIG')
            
            assert result is True
            assert app.config['TEST_VALUE'] == 'relative_path'
        finally:
            os.environ.pop('TEST_CONFIG', None)
            if os.path.exists(config_file):
                os.unlink(config_file)
            if os.path.exists(instance_dir):
                os.rmdir(instance_dir)
    
    def test_from_envvar_missing_env_var(self):
        """Test from_envvar raises RuntimeError when env var is missing."""
        app = Flask(__name__)
        
        with pytest.raises(RuntimeError, match="The environment variable 'MISSING_CONFIG' is not set"):
            app.config.from_envvar('MISSING_CONFIG')
    
    def test_from_envvar_missing_env_var_silent(self):
        """Test from_envvar returns False when env var is missing and silent=True."""
        app = Flask(__name__)
        
        result = app.config.from_envvar('MISSING_CONFIG', silent=True)
        assert result is False
    
    def test_from_envvar_missing_file_silent(self):
        """Test from_envvar returns False when file is missing and silent=True."""
        app = Flask(__name__)
        
        try:
            os.environ['TEST_CONFIG'] = '/nonexistent/config.py'
            result = app.config.from_envvar('TEST_CONFIG', silent=True)
            assert result is False
        finally:
            os.environ.pop('TEST_CONFIG', None)
    
    def test_from_envvar_relative_path_with_subdirectory(self):
        """Test from_envvar with relative path including subdirectory."""
        app = Flask(__name__)
        
        # Create instance directory and subdirectory
        instance_dir = os.path.join(app.root_path, 'instance')
        config_subdir = os.path.join(instance_dir, 'configs')
        os.makedirs(config_subdir, exist_ok=True)
        
        # Create config file in subdirectory
        config_file = os.path.join(config_subdir, 'app_config.py')
        with open(config_file, 'w') as f:
            f.write('TEST_VALUE = "subdir_config"\n')
        
        try:
            # Set environment variable to relative path with subdirectory
            os.environ['TEST_CONFIG'] = 'configs/app_config.py'
            result = app.config.from_envvar('TEST_CONFIG')
            
            assert result is True
            assert app.config['TEST_VALUE'] == 'subdir_config'
        finally:
            os.environ.pop('TEST_CONFIG', None)
            if os.path.exists(config_file):
                os.unlink(config_file)
            if os.path.exists(config_subdir):
                os.rmdir(config_subdir)
            if os.path.exists(instance_dir):
                os.rmdir(instance_dir)
