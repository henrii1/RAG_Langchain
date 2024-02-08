import os 
import pytest

from webapp.utils import download_csv

current = os.curdir

@pytest.mark.parametrize("url, file_name", [
    ("https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/customers/customers-100.csv", "test_one")
])


def test_download(url, file_name):

    file_path = download_csv(url, file_name)

    assert os.path.exists(f"./{file_name}")

    assert file_path.lower().endswith('.csv')

    


