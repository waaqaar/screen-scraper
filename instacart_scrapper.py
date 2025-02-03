import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time
import json

CATEGORY_PATH = "/categories/"


class EcommerceScraper:
    """
    A class to scrape product data from e-commerce websites.
    """
    def __init__(self, base_url, headers=None):
        """
        Initialize the scraper with a base URL and optional headers.
        :param base_url: The root URL of the e-commerce website.
        :param headers: Optional HTTP headers for requests.
        """
        self.base_url = base_url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.data = []

    def fetch_page(self, url):
        """
        Fetch the HTML content of a page.
        :param url: The full URL of the page to fetch.
        :return: BeautifulSoup object of the page content.
        """
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def extract_data(self, soup):
        """
        Extract product data from the page content.
        :param soup: BeautifulSoup object containing the page HTML.
        """
        try:
            # Example: Replace with actual HTML element classes or tags
            product_elements = soup.find_all("div", class_="product-class")  # Replace with actual class name
            for product in product_elements:
                name = product.find("h2", class_="product-title").text.strip()  # Replace with actual tag/class
                price = product.find("span", class_="product-price").text.strip()  # Replace with actual tag/class
                self.data.append({"Product Name": name, "Price": price})
        except Exception as e:
            print(f"Error extracting data: {e}")

    def scrape_category(self, category_path):
        """
        Scrape a specific category page for product data.
        :param category_path: The relative URL of the category page.
        """
        url = f"{self.base_url}{category_path}"
        print(f"Scraping category: {url}")
        soup = self.fetch_page(url)
        if soup:
            self.extract_data(soup)
            time.sleep(2)  # Be polite and avoid overwhelming the server

    def save_to_csv(self, file_name):
        """
        Save the scraped data to a CSV file.
        :param file_name: The name of the CSV file to save.
        """
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_csv(file_name, index=False)
            print(f"Data saved to {file_name}")
        else:
            print("No data to save.")

    def scrape_multiple_categories(self, category_paths, output_file):
        """
        Scrape multiple categories and save the results to a file.
        :param category_paths: A list of category paths to scrape.
        :param output_file: The name of the output file.
        """
        for category_path in category_paths:
            self.scrape_category(category_path)
        self.save_to_csv(output_file)

    def get_all_category_urls(self, path):
        # Send an HTTP GET request
        response = requests.get(self.base_url + path, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all <a> tags with an href attribute
            links = soup.find_all("a", href=True)

            # Extract and clean URLs
            urls = [
                {
                    'url': urljoin(self.base_url, link['href']),
                    'category': link.find('div').get_text(strip=True) if link.find('div')
                    else ' '.join(
                        link['href'].split('/')[-1].split('-')[1:]
                    ).title()
                } for link in links if 'categories' in link['href']]

            return urls
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return []

    def get_product_links(self, target_url):
        # Send a GET request to the website
        response = requests.get(target_url, headers=self.headers)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the root div containing product cards
            root_div = soup.find('div', class_='e-10tu4d6')

            # Extract href links from product cards
            if root_div:
                product_links = []
                product_cards = root_div.find_all('div', class_='e-174im8r')
                for card in product_cards:
                    link_tag = card.find('a', href=True)  # Look for <a> tags with href
                    if link_tag:
                        product_links.append(link_tag['href'])  # Extract href
                return product_links
            else:
                print("Root div with class 'e-10tu4d6' not found.")
                return []
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return []

    def get_product_links_v2(self, target_url):
        product_links = []
        current_url = target_url

        while current_url:
            # Send a GET request to the current page
            response = requests.get(current_url, headers=self.headers)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, "html.parser")

                # Find the root div containing product cards
                root_div = soup.find('div', class_='e-10tu4d6')
                if root_div:
                    # Extract href links from product cards
                    product_cards = root_div.find_all('div', class_='e-174im8r')
                    for card in product_cards:
                        link_tag = card.find('a', href=True)
                        if link_tag:
                            product_links.append(link_tag['href'])
                else:
                    print("Root div with class 'e-10tu4d6' not found on this page.")

                # Check for the "Next" page link
                next_button = soup.find('a', {'aria-label': 'Next'})
                if next_button and 'href' in next_button.attrs:
                    next_page_url = next_button['href']
                    # Construct the full URL if the next page link is relative
                    if next_page_url.startswith('/'):
                        current_url = self.base_url + next_page_url
                    else:
                        current_url = next_page_url
                else:
                    # No more pages
                    current_url = None
            else:
                print(f"Failed to fetch the page. Status code: {response.status_code}")
                break

        return product_links

    def get_product_details(self, path):
        # Send a GET request to the website
        response = requests.get(self.base_url + path, headers=self.headers)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the root div containing product cards
            root_div = soup.find('div', class_='e-uqsf9v')

            # Extract href links from product cards
            if root_div:
                product_links = []
                product_cards = root_div.find_all('div', class_='e-174im8r')
                for card in product_cards:
                    link_tag = card.find('a', href=True)  # Look for <a> tags with href
                    if link_tag:
                        product_links.append(link_tag['href'])  # Extract href
                return product_links
            else:
                print("Root div with class 'e-10tu4d6' not found.")
                return []
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return []

    def save_response_to_json(self, data, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(f"{filename}.json", "w") as outfile:
            json.dump(data, outfile)


# Example Usage
if __name__ == "__main__":
    base_url = "https://www.instacart.com"

    # Initialize the scraper
    scraper = EcommerceScraper(base_url)
    all_url = scraper.get_all_category_urls('/categories/')
    prod_links = scraper.get_product_links_v2("https://www.instacart.com/categories/1361-household-essentials")

    base_path = 'data/'
    for link in prod_links:
        data = scraper.get_product_details(link)
        scraper.save_response_to_json(data, os.path.join(base_path, link))
