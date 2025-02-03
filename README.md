# screen-scraper

## Overview

The `screen-scraper` project is a tool designed to scrape and extract data from web pages. It allows users to specify target websites and extract relevant information for further processing or analysis.

## Features

- **Customizable Scraping**: Define the elements to scrape using CSS selectors.
- **Data Export**: Export scraped data to various formats such as CSV, JSON, or XML.
- **Error Handling**: Robust error handling to manage network issues and invalid selectors.
- **Logging**: Detailed logging to monitor scraping activities and debug issues.

## Installation

To install the `screen-scraper`, clone the repository and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate # For Linux
pip install -r requirements.txt
```

## Usage

To use the `screen-scraper`, run the following command:

For screenscraping we need to make sure that standalone chrome is running, run the following command

```bash
docker compose up
python instacart_bot.py
```

For API scraping, we don't need explicit chrome running, for that we can simply execute the followiing command.
```bash
python instacart_scraper.py
```
