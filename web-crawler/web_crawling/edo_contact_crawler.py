import time
from copy import deepcopy
from tqdm import tqdm

import pandas as pd
import requests
from bs4 import BeautifulSoup

from web_crawling.edo_contact_parser import EDOContactInfoParser
from web_crawling.edo_directory import EDODirectory
from web_crawling.web_crawler_errors import WebCrawlerError, NoResultsFoundError
from storage.storage_client import StorageClient


class EDOContactCrawler:
    DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    def __init__(self, storage_client: StorageClient, logging, user_agent=None):
        self.edo_directory = EDODirectory(logging, storage_client)
        self.contact_parser = EDOContactInfoParser()
        self._user_agent = self.DEFAULT_USER_AGENT if not user_agent else user_agent
        self._storage_client = storage_client

    def _get_google_search_cause_iq_url(self, edo_name):
        edo = edo_name.replace(" ", "+")
        search_parmas = f"{edo}+causeiq"
        search_url = f"https://www.google.com/search?q={search_parmas}"
        return search_url

    def _get_cause_iq_link(self, search_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the search results: HTTP Status code {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('div', class_='g')

        if not search_results:
            raise Exception("No search results found")

        first_result = search_results[0]
        first_link = first_result.find('a', href=True)

        if not first_link:
            raise Exception("No link found in the first search result")

        return first_link['href']

    def _fetch_edo_url(self, url):
        headers = {'User-Agent': self._user_agent}
        response = requests.get(url, headers=headers, timeout=15)
        time.sleep(5)  # to avoid getting throttled or denied
        if response.status_code != 200:
            raise WebCrawlerError("Failed to fetch Cause IQ results", response.status_code)
        return response.text

    def _parse_edo_url(self, html_content):
        parsed_edo_contact = self.contact_parser.parse_contact_info(html_content)
        return parsed_edo_contact

    def _get_filename(self, city):
        city_name = city.lower().replace(" ", "_")
        return f"{city_name}_edo_contact"

    def build_edo_contact_info(self, results: pd.DataFrame, city: str):
        contact_results = []
        for row_dict in tqdm(results.to_dict(orient="records")):
            edo_dict = deepcopy(row_dict)
            name = edo_dict["NAME"]
            try:
                google_search_cause_iq_url = self._get_google_search_cause_iq_url(name)
                cause_iq_link = self._get_cause_iq_link(google_search_cause_iq_url)
                html_content = self._fetch_edo_url(cause_iq_link)
                contact_dict = self._parse_edo_url(html_content)
            except NoResultsFoundError:
                contact_dict = {"Website URL": None, "Phone": None}

            edo_dict.update(contact_dict)
            contact_results.append(edo_dict)

        df = pd.DataFrame.from_records(contact_results)
        filename = self._get_filename(city)
        self._storage_client.save(df, filename)
        return contact_results

    def _load_dataframe(self, filename):
        return self._storage_client.get_dataframe(filename)

    def get_edo_contact_info(self, city):
        filename = self._get_filename(city)
        df = self._storage_client.get_dataframe(filename)
        if df.empty:
            results = self.edo_directory.get_city_edos(city)
            self.build_edo_contact_info(results, city)

        return self._load_dataframe(f"{filename}")
