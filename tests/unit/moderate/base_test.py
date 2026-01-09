import unittest
import sys
import os
from unittest.mock import patch

# --- PATH CONFIGURATION ---
# Dynamically add the 'src' directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to the project root to find 'src'
# structure: project_root / tests / unit / moderate / base_test.py
project_root = os.path.abspath(os.path.join(current_dir, "../../../src"))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the module using the package structure
from cli.moderate import check_book_copyright

class BaseModerateTest(unittest.TestCase):
    """
    Parent class to handle common setup, environment variables, 
    and API mocking for both Gemini and Mistral.
    """

    def setUp(self):
        # 1. Mock Environment Variables
        self.env_patcher = patch.dict(os.environ, {
            "GEMINI_API_KEY": "test_key",
            "GEMINI_MODEL": "test_model",
            "MISTRAL_API_KEY": "test_key",
            "MISTRAL_MODEL": "test_model"
        })
        self.env_patcher.start()

        # 2. Mock Logging to keep the terminal clean
        self.log_patcher = patch('cli.moderate.Log.write')
        self.mock_log = self.log_patcher.start()

        # 3. Mock the LLM calls inside CopyrightLLMChecker
        self.gemini_patcher = patch('cli.moderate.CopyrightLLMChecker.ask_gemini')
        self.mistral_patcher = patch('cli.moderate.CopyrightLLMChecker.ask_mistral')
        
        self.mock_gemini = self.gemini_patcher.start()
        self.mock_mistral = self.mistral_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()
        self.log_patcher.stop()
        self.gemini_patcher.stop()
        self.mistral_patcher.stop()