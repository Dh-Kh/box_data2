from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from typing import Dict, Any, Union, List
import os
import json

load_dotenv()

INITIAL_URL = os.getenv("INITIAL_URL")

class Ebay(object):
    
    def __init__(self, start_url: str, scraping_limit: int = 5):
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        
        self._driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        self.start_url = start_url 
        self.scraping_limit = scraping_limit
    
    def parse(self) -> Union[TimeoutException, List[Dict[str, Any]]]:
        
        self._driver.get(self.start_url)
        
        data = []

        
        try:
            wait = WebDriverWait(self._driver, 3)
            items = wait.until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "s-item__wrapper clearfix"))
            )
                        
            for i, item in enumerate(items):
                
                if i == self.scraping_limit:
                    break
                
                try:
                    title_element = item.find_element(By.CLASS_NAME, 's-item__title')
                    title = title_element.text
                except NoSuchElementException:
                    title = None
                    title_element = None

                try:
                    photo_link = item.find_element(By.CLASS_NAME, 's-item__image-img').get_attribute('src')
                except NoSuchElementException:
                    photo_link = None

                try:
                    product_link = item.find_element(By.CLASS_NAME, 's-item__link').get_attribute('href')
                except NoSuchElementException:
                    product_link = None

                try:
                    price = item.find_element(By.CLASS_NAME, 's-item__price').text
                except NoSuchElementException:
                    price = None

                try:
                    shipping_price = item.find_element(By.CLASS_NAME, 's-item__shipping s-item__logisticsCost').text
                except NoSuchElementException:
                    shipping_price = None

                salesman_info = None
                
                if title_element:
                    try:
                        title_element.click()
                        salesman_info = wait.until(
                            EC.visibility_of_element_located(
                                (By.CLASS_NAME, 'ux-textspans.ux-textspans--BOLD')
                            )
                        ).text
                        self._driver.back()
                    except (NoSuchElementException, TimeoutException):
                        salesman_info = None
                
                data.append({
                    'title': title,
                    'photo_link': photo_link,
                    'product_link': product_link,
                    'price': price,
                    'shipping_price': shipping_price,
                    'salesman_info': salesman_info
                })
            
            return data
        
        except TimeoutException as e:
            raise e
        
        finally:
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            self._driver.quit()

if __name__ == "__main__":
    ebay = Ebay(start_url=INITIAL_URL)
    print("Executing...")
    data = ebay.parse()
    print("Data has been stored in data.json!")
