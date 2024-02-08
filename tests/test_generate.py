import pytest
from webapp.app import generate_response

# Sample CSV data for testing
SAMPLE_CSV_DATA = b"header1,header2\nvalue1,value2\n"

# Sample question for testing
SAMPLE_QUESTION = "Sample question for testing?"

@pytest.fixture
def mock_csv_loader(monkeypatch):
    """Mock CSVLoader to return sample CSV data."""
    class MockCSVLoader:
        @staticmethod
        def load():
            return SAMPLE_CSV_DATA

    monkeypatch.setattr("my_module.CSVLoader", MockCSVLoader)

@pytest.fixture
def mock_chat_openai(monkeypatch):
    """Mock ChatOpenAI to return a sample response."""
    class MockChatOpenAI:
        @staticmethod
        def invoke(query):
            return {"result": {"response": "Sample response", "score": "0.8"}}

    monkeypatch.setattr("my_module.ChatOpenAI", MockChatOpenAI)

def test_generate_response(mock_csv_loader, mock_chat_openai):
    # Call the function with sample question and CSV path
    response, score = generate_response(SAMPLE_QUESTION, "sample.csv")

    # Assert that the response and score match the expected values
    assert response == "Sample response"
    assert score == 0.8
