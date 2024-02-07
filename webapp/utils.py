import os
import requests

def download_csv(url: str, file_name: str) -> str:
    """Downloads CSV from URL and saves it locally."""
    if not url:
        raise ValueError("URL cannot be empty.")
    if not file_name.lower().endswith('.csv'):
        file_name += '.csv'
    try:
        response = requests.get(url)
        response.raise_for_status()
        file_path = f"./{file_name}"
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading CSV: {e}")

def load_csv(file_uploaded) -> str:
    """Loads CSV file content."""
    if file_uploaded:
        with open(file_uploaded.name, "wb") as f:
            f.write(file_uploaded.read())
        return file_uploaded.name
