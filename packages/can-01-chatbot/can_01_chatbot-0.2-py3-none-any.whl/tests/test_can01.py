# tests/test_can01.py

import os
import sys
import pytest

# Add the project directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from can_01_chatbot.can01 import get_openai_response

def test_get_openai_response():
    # Set the environment variable for testing
    os.environ['OPENAI_API_KEY'] = 'sk-proj-GjFvMSLVhEhd57BMvvHBT3BlbkFJxCS45zqcvyTF6V4ilf9t'
    
    response = get_openai_response("Hello, chatbot!")
    assert isinstance(response, str)
