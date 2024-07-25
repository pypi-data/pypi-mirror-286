# main.py

import asyncio
from my_project85.log_configs import setup_logging
from my_project85.scrapping import scrape_urls
from my_project85.config import URLS_TO_SCRAPE
import my_project85.utils  # Importing utils to demonstrate logging usage
import my_project85.essential

def main():
    setup_logging()  # Set up the logging configuration
    my_project85.utils.simple_utility_function()  # Call a utility function to show logging

    # Run the main scraping tasks
    asyncio.run(scrape_urls(URLS_TO_SCRAPE))
    my_project85.essential.simple_essential_function()

if __name__ == "__main__":
    main()
