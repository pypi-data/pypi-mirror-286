import json
import requests
from bs4 import BeautifulSoup
import time

class FullTextScraper:
    """A class to scrape the full text of judgments from the National Archives website."""

    def __init__(self, json_file_path):
        """Initializes the scraper with the path to the JSON file containing judgment links."""
        self.json_file_path = json_file_path

    def load_json(self):
        """Loads the JSON file containing judgment links.

        Returns:
            A dictionary with judgment details.
        """
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_response(self, url, retries=5, backoff_factor=1.0):
        """Gets the response from a URL with retry mechanism.

        Args:
            url: The URL to get the response from.
            retries: Number of retries in case of failure.
            backoff_factor: Factor by which the wait time increases after each retry.

        Returns:
            The response object if the request is successful, None otherwise.
        """
        for attempt in range(retries):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise HTTPError for bad responses
                return response
            except requests.RequestException as e:
                if attempt < retries - 1:
                    sleep_time = backoff_factor * (2 ** attempt)
                    print(f"Request failed: {e}. Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    print(f"Request failed after {retries} attempts: {e}")
                    return None

    def scrape_full_text(self, url):
        """Scrapes the full text from the given URL.

        Args:
            url: The URL of the judgment page.

        Returns:
            A string containing the full text of the judgment.
        """
        response = self.get_response(url)
        if response is None:
            return "Failed to retrieve content."

        soup = BeautifulSoup(response.content, 'html.parser')
        judgment_body = soup.find("section", class_="judgment-body")
        if judgment_body:
            return judgment_body.get_text(separator=' ', strip=True)
        return "Judgment body not found."

    def add_full_text_to_json(self, data):
        """Adds the full text to each judgment entry in the data dictionary.

        Args:
            data: A dictionary with judgment details.
        """
        for case_name, details in data.items():
            url = details.get('link')
            if url:
                full_text = self.scrape_full_text(url)
                details['full_text'] = full_text

    def save_to_json(self, data, output_file_path):
        """Saves the updated data to a JSON file.

        Args:
            data: The dictionary containing the updated data.
            output_file_path: The path of the file to save the updated data to.
        """
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def output_scraper(self, output_file_path):
        """Runs the scraper to add full text to the JSON data and saves it to a new file.

        Args:
            output_file_path: The path of the file to save the updated data to.
        """
        data = self.load_json()
        self.add_full_text_to_json(data)
        self.save_to_json(data, output_file_path)