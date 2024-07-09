# eBay Product Scraper

This Python script scrapes product listings from eBay, extracting key details like title, image, price, shipping cost, and seller information. The scraped data is then saved in a structured JSON file (`data.json`).

## Features

* **Efficient Scraping:** Uses Selenium WebDriver to automate browser interaction, extracting data directly from eBay's dynamic web pages.
* **Data Extraction:** Gathers product title, image URL, product URL, price, shipping price, and seller information.
* **Customizable:** Allows you to set the maximum number of products to scrape.
* **Error Handling:** Includes error handling for cases where elements are not found or the page doesn't load within the timeout limit.
* **JSON Output:** Saves the scraped data in a well-formatted JSON file for easy analysis and further processing.

## Usage

1. **Clone or download the repository:**

   ```bash
    git clone https://github.com/Dh-Kh/box_data2.git

    python3 -m venv venv

    source venv/bin/activate (or . venv/bin/activate)

    pip install -r requirements.txt

    python3 main.py
   ```

## Project Structure
```bash
    .
    ├── __init__.py
    ├── main.py
    ├── Readme.md
    └── requirements.txt
```