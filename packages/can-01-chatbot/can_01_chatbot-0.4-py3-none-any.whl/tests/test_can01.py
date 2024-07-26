import os
import sys
import pytest
from dotenv import load_dotenv

# Add the project directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

from can_01_chatbot.can01 import get_openai_response

def test_get_openai_response():
    # Ensure the environment variable is set
    assert 'OPENAI_API_KEY' in os.environ

    response = get_openai_response("Hello, chatbot!")
    assert isinstance(response, str)
