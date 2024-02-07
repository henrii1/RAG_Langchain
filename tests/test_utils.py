import os
import pytest

from webapp.utils import download_csv, load_csv



@pytest.mark.parametrize("url, file_name", [
    ("https://example.com/data.csv", "test_data"),
    ("https://example.com/data2.csv", "test_data2"),
])
def test_download(url, file_name, tmpdir):

    file_path = download_csv(url, file_name)

    assert os.path.exists(file_path)

    assert file_path.lower().endswith('.csv')

    assert file_path.startswith(str(tmpdir))




def test_load_csv(tmpdir):
    # Create a temporary file with some content
    csv_content = b"header1,header2\nvalue1,value2\n"
    csv_file_path = os.path.join(tmpdir, "test.csv")
    with open(csv_file_path, "wb") as f:
        f.write(csv_content)

    # Create a mock file_uploaded object
    class MockFileUploaded:
        def __init__(self, name):
            self.name = name

    # Call the function with the mock file_uploaded object
    file_uploaded = MockFileUploaded(name=csv_file_path)
    result_file_path = load_csv(file_uploaded)

    # Assert that the returned file path matches the original file path
    assert result_file_path == csv_file_path

    # Assert that the content of the original file and the loaded file are the same
    with open(result_file_path, "rb") as f:
        loaded_content = f.read()
        assert loaded_content == csv_content
