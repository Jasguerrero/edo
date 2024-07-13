import os
import argparse
import logging

from storage.csv_storage_client import CSVStorageClient
from storage.db_storage_client import DBStorageClient
from web_crawling.edo_more_contact_info_crawler import EDOMoreContactInfoCrawler
from city_state.city_to_state_generator import CityStateMapGenerator
from formatter.final_format import format_final_df

logging.basicConfig(level=logging.INFO)

def main(csv_storage_client: CSVStorageClient):
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Web crawler for EDOs.')
    parser.add_argument('--city', type=str, default='New York', help='City to search for EDOs')

    # Parse arguments
    args = parser.parse_args()

    # Use default city if none provided
    city = args.city
    if city == 'New York':
        logging.info('Using default city "New York"')

    # Placeholder for the actual crawling logic
    logging.info(f'Starting fetch for EDOs in {city}')

    csv_storage_client = CSVStorageClient(logging=logging)
    db_storage_client = DBStorageClient(logging=logging)
    full_contact_info_crawler = EDOMoreContactInfoCrawler(
        storage_client=csv_storage_client,
        logging=logging
    )
    full_contact_info = full_contact_info_crawler.get_edo_full_contact_info(city)
    final_df = format_final_df(full_contact_info)
    city_name = city.lower().replace(" ", "_")
    filename = f"{city_name}_edo_final"
    csv_storage_client.save(final_df, filename)
    db_storage_client.save(final_df, '')
    
if __name__ == '__main__':
    csv_storage_client = CSVStorageClient(logging=logging)
    city_state_file_name = 'city_state_map'

    # Persist the csv mapping that is generated on the first run
    if os.path.exists(f"/app/data/{city_state_file_name}.csv"):
        logging.info('Skipping city-state generator')
    else:
        csm_generator = CityStateMapGenerator(csv_storage_client, city_state_file_name)
        csm_generator.generate()

    main(csv_storage_client)
