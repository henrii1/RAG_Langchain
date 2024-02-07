import pytest
from webapp.app import main

@pytest.fixture
def mock_streamlit(mocker):
    """Mock Streamlit functions."""
    mocker.patch("webapp.app.st.title")
    mocker.patch("webapp.app.st.write")
    mocker.patch("webapp.app.st.text_area")
    mocker.patch("webapp.app.st.sidebar.file_uploader")
    mocker.patch("webapp.app.st.sidebar.button")
    mocker.patch("webapp.app.st.button")
    mocker.patch("webapp.app.st.spinner")
    mocker.patch("webapp.app.st.markdown")
    mocker.patch("webapp.app.st.code")

def test_main(mock_streamlit):
    # Call the main function
    main()

    # Assertions for Streamlit function calls
    webapp.app.st.title.assert_called_once_with("RAG POC Chatbot")
    webapp.app.st.write.assert_called_once_with("Ask questions based on the therapy session and get a response")
    webapp.app.st.text_area.assert_called_once_with("Enter your questions here")
    webapp.app.st.sidebar.file_uploader.assert_called_once_with("Upload a CSV file containing the transcript", key="file_upload")
    webapp.app.st.sidebar.button.assert_called_once_with("Upload CSV File")
    webapp.app.st.button.assert_called_once_with("Ask Question")

