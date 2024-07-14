import re
from copy import deepcopy

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from web_crawling.edo_contact_crawler import EDOContactCrawler
from web_crawling.web_crawler_errors import NoResultsFoundError
from storage.storage_client import StorageClient


class EDOMoreContactInfoCrawler:
    WEBSITE_KEY = "Website URL"
    PHONE_KEY = "Phone"
    EMAIL_KEY = "email"

    def __init__(self, logging, storage_client: StorageClient):
        self.edo_contact_info = EDOContactCrawler(
            storage_client=storage_client,
            logging=logging
        )
        self._storage_client = storage_client
        self._logging = logging

    def _get_google_search_url(self, edo_name, key: str = None):
        edo = edo_name.replace(" ", "+")
        params = f"{edo}"
        if key:
            params = f"{params}+{key}"
        search_url = f"https://www.google.com/search?q={params}"
        return search_url

    def _get_first_google_search_link(self, search_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the search results: HTTP Status code {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('div', class_='g')

        if not search_results:
            raise NoResultsFoundError

        first_result = search_results[0]
        return first_result


    def _get_edo_website(self, edo):
        url = self._get_google_search_url(edo)
        results = self._get_first_google_search_link(url)
        first_link = results.find('a', href=True)

        if not first_link:
            return None

        return first_link['href']

    def _get_edo_phone(self, edo):
        url = self._get_google_search_url(edo, "phone")
        result = self._get_first_google_search_link(url)
        result_text = result.get_text()

        # Regular expression to match phone numbers
        phone_pattern = re.compile(r'\(?\b[0-9]{3}[-.) ]*[0-9]{3}[-. ]*[0-9]{4}\b')
        phone_match = phone_pattern.search(result_text)

        if not phone_match:
            return None

        return phone_match.group()

    def _get_edo_email(self, edo):
        url = self._get_google_search_url(edo, "email")
        result = self._get_first_google_search_link(url)
        result_text = result.get_text()

        # Regular expression to match email addresses
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        email_match = email_pattern.search(result_text)

        if not email_match:
            return None

        return email_match.group()

    def _get_filename(self, city):
        city_name = city.lower().replace(" ", "_")
        return f"{city_name}_edo_full_contact"

    def fill_more_contact_info(self, results: pd.DataFrame, city: str):
        contact_results = []
        for row_dict in tqdm(results.to_dict(orient="records")):
            edo_dict = deepcopy(row_dict)
            edo_name = edo_dict["NAME"]
            if not isinstance(edo_dict[self.WEBSITE_KEY], str):
                edo_dict[self.WEBSITE_KEY] = self._get_edo_website(edo_name)
            if not isinstance(edo_dict[self.PHONE_KEY], str):
                edo_dict[self.PHONE_KEY] = self._get_edo_phone(edo_name)
            edo_dict[self.EMAIL_KEY] = self._get_edo_email(edo_name)
            contact_results.append(edo_dict)

        df = pd.DataFrame.from_records(contact_results)
        filename = self._get_filename(city)
        self._storage_client.save(df, filename)
        return contact_results

    def _load_dataframe(self, filename):
        return self._storage_client.get_dataframe(filename)

    def get_edo_full_contact_info(self, city):
        self._logging.info("get full contact info")
        filename = f"{self._get_filename(city)}"
        #full_filename = f"{filename}.csv"
        df = self._storage_client.get_dataframe(filename)
        if df.empty:
            results = self.edo_contact_info.get_edo_contact_info(city)
            self.fill_more_contact_info(results, city)

        return self._load_dataframe(filename)
