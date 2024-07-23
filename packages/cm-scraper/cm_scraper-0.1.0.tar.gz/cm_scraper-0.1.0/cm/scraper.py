# cm/scraper.py

import requests
from bs4 import BeautifulSoup
import time
import re
import json
import logging
from requests.exceptions import RequestException
import argparse
import sys

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler('movie_scraper.log')
file_handler.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def refresh_session_cookies(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.cookies.get_dict()
    except RequestException as e:
        logger.error(f"Error refreshing session cookies: {e}")
        return {}

def access_yoteshin_page(yoteshin_url, persistent_cookies):
    base_url = 'https://yoteshinportal.cc'
    session_cookies = refresh_session_cookies(base_url)
    cookies = {**persistent_cookies, **session_cookies}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'identity',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    try:
        response = requests.get(yoteshin_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        save_button = soup.find('a', id='save-button')
        if save_button:
            onclick_attr = save_button.get('onclick')
            if onclick_attr:
                match = re.search(r"app\.saveToGoogleDrive\('([^']+)'", onclick_attr)
                if match:
                    return match.group(1)
        logger.warning(f"Save button not found on {yoteshin_url}")
    except RequestException as e:
        logger.error(f"Error accessing Yoteshin page {yoteshin_url}: {e}")
    return None

def send_save_request(yoteshin_id, persistent_cookies):
    base_url = 'https://yoteshinportal.cc'
    save_url = f'{base_url}/api/save'
    session_cookies = refresh_session_cookies(base_url)
    cookies = {**persistent_cookies, **session_cookies}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://yoteshinportal.cc',
        'Referer': 'https://yoteshinportal.cc/',
    }

    payload = {"key": yoteshin_id}

    try:
        response = requests.post(save_url, headers=headers, cookies=cookies, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        logger.info(f"Save request result for ID {yoteshin_id}: {result}")
        return result
    except RequestException as e:
        logger.error(f"Error sending save request for ID {yoteshin_id}: {e}")
        return None

def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all(class_="item")
        movies = []
        for item in items:
            link = item.find('a')
            title_span = item.find('span', class_="tt")
            if link and title_span:
                movie_url = link.get('href')
                title = title_span.text
                movies.append((movie_url, title))
        return movies
    except RequestException as e:
        logger.error(f"Error scanning page {url}: {e}")
        return []

def find_yoteshin_link(movie_url):
    try:
        response = requests.get(movie_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        enlaces_box = soup.find(class_="enlaces_box")
        if enlaces_box:
            links = enlaces_box.find_all('a')
            for link in links:
                href = link.get('href')
                if href and 'yoteshinportal.cc' in href:
                    size = link.find('span', class_='c').text if link.find('span', class_='c') else 'N/A'
                    quality = link.find('span', class_='d').text if link.find('span', class_='d') else 'N/A'
                    return href, size, quality
        logger.warning(f"No Yoteshin link found for {movie_url}")
    except RequestException as e:
        logger.error(f"Error finding Yoteshin link for {movie_url}: {e}")
    return None, None, None

def scrape_movies(start_page, end_page, token, delay):
    base_url = "https://www.channelmyanmar.to/movies/page/{}/"
    all_movies = []

    persistent_cookies = {
        'adonis-remember-token': token
    }

    for page in range(start_page, end_page + 1):
        url = base_url.format(page)
        logger.info(f"Scanning page {page}...")
        movies = scrape_page(url)
        all_movies.extend(movies)
        time.sleep(delay)

    logger.info(f"Total movies collected: {len(all_movies)}")

    for index, (movie_url, title) in enumerate(all_movies):
        if index > 0:
            logger.info("")
        logger.info(f"Processing: {title}")
        logger.info(f"Movie URL: {movie_url}")
        yoteshin_link, size, quality = find_yoteshin_link(movie_url)
        if yoteshin_link:
            logger.info(f"Yoteshin Link: {yoteshin_link}")
            logger.info(f"Size: {size}")
            logger.info(f"Quality: {quality}")
            yoteshin_id = access_yoteshin_page(yoteshin_link, persistent_cookies)
            if yoteshin_id:
                logger.info(f"Yoteshin ID: {yoteshin_id}")
                save_result = send_save_request(yoteshin_id, persistent_cookies)
                if save_result:
                    if save_result.get('status') == 'success':
                        logger.info(f"Save successful! File ID: {save_result.get('fileId')}, Folder ID: {save_result.get('folderId')}")
                    else:
                        logger.error(f"Save request failed. Error: {save_result.get('error', 'Unknown error')}")
                else:
                    logger.error("Save request failed. No response received.")
            else:
                logger.warning(f"Couldn't find the Yoteshin ID for {title}")
        else:
            logger.warning(f"No Yoteshin link found for {title}")
        time.sleep(delay)

def main():
    parser = argparse.ArgumentParser(description="Movie Scraper CLI")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--page", type=int, help="Single page to scrape")
    group.add_argument("--page-range", type=int, nargs=2, metavar=('START', 'END'), 
                        help="Range of pages to scrape (e.g., --page-range 10 40 to scrape pages 10 to 40)")
    parser.add_argument("--token", type=str, required=True, help="Authentication token")
    parser.add_argument("--delay", type=float, default=1, help="Time delay between requests in seconds (default: 1)")
    args = parser.parse_args()

    if args.page:
        start_page = end_page = args.page
    elif args.page_range:
        start_page, end_page = args.page_range
        if start_page > end_page:
            logger.error("Start page cannot be greater than end page.")
            return
    else:
        start_page = end_page = 1  # Default to scraping only page 1

    try:
        scrape_movies(start_page, end_page, args.token, args.delay)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()