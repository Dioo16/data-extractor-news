import threading
import logging
import time
from datetime import datetime
import itertools
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.remote.webelement import WebElement



from utils.values_utils import get_chrome_driver_value, get_news_images_dir_value
from utils.strings_utils import format_to_allowed_filename


class CustomSelenium:
    def __init__(self):
        logging.info("Starting configuration")

        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument('--remote-debugging-port=9222')
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-logging"])

            driver_path = get_chrome_driver_value()

            service = Service(driver_path)

            self._driver = webdriver.Chrome(
                service=service, options=chrome_options)

            self.overlay_event = threading.Event()
            self.overlay_detected = threading.Event()
            thread = threading.Thread(target=self.close_overlay)
            thread.daemon = True
            thread.start()

            logging.info("configuration finished")

        except ImportError as exception:
            logging.error("Error initializing configuration: %s", exception)
            raise

    @property
    def driver(self):
        """Returns the Chrome WebDriver instance."""

        return self._driver

    def close_overlay(self):
        """
        Thread method that continuously checks for and closes overlay elements on the webpage.
        """        
        logging.info("Starting overlay close thread")
        while True:
            try:
                overlay_present = len(
                    self.driver.find_elements(
                        By.XPATH,
                        "//div[contains(@class, 'fancybox-overlay')]")) > 0

                if overlay_present:
                    print("overlay apareceu")
                    logging.info("Overlay detected, attempting to close")
                    self.overlay_detected.set()
                    close_button = self.driver.find_element(
                        By.XPATH, "//a[contains(@class, 'fancybox-close')]")
                    close_button.click()
                    logging.info("Overlay closed successfully")
                    print("overlay foi fechada")

                else:
                    if self.overlay_event.is_set():
                        self.overlay_detected.clear()  # Clear the detected event
                        logging.info("Overlay removed, continuing execution")

            except Exception as e:
                logging.info("Overlay not found or other error: %s", e)

    def driver_quit(self):
        """
        Attempts to quit the WebDriver instance and logs the success or failure of the attempt.
        """
        logging.info("Attempting to quit WebDriver")
        try:
            if self.driver:
                self.driver.quit()
                logging.info("WebDriver quit successfully")
        except ImportError as exception:
            logging.error("Error quitting WebDriver: %s", exception)

    def looking_at_element(self, locator):
        """
        Logs and attempts to locate an element on the webpage using the provided CSS locator.

        :param locator: The CSS locator of the element to find.
        """
        logging.info("Looking at element with locator: %s", locator)
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, locator)
            logging.info("Element found with locator %s: %s",
                         locator, dir(element))
        except ImportError as exception:
            logging.error(
                "Error finding element with locator %s: %s",
                locator,
                exception)

    def open_site(self, url):
        """
        Opens a webpage with the provided URL.

        :param url: The URL of the webpage to open.
        """       
        logging.info("Opening site: %s", url)
        try:
            self.driver.get(url)
            logging.info("Site opened: %s", url)
        except ImportError as exception:
            logging.error("Error opening site %s: %s", url, exception)

    def filling_input(self, locator, text):
        """
        Fills an input field identified by the CSS locator with the provided text.

        :param locator: The CSS locator of the input field.
        :param text: The text to input into the field.
        """
        logging.info(
            "Filling input with text '%s' at locator %s", text, locator)
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, locator)
            element.send_keys(text)
            logging.info(
                "Input filled with text '%s' at locator %s", text, locator)
        except ImportError as exception:
            logging.error(
                "Error filling input with text '%s' at locator %s: %s",
                text,
                locator,
                exception)

    def search_phrase(self, phrase):
        """
        Searches for a phrase on the webpage by interacting with the search button and input field.

        :param phrase: The phrase to search for.
        """
        logging.info("Searching for phrase: %s", phrase)
        try:
            button_open_search = self.driver.find_element(
                By.XPATH, "//button[@class='SearchOverlay-search-button']")
            button_open_search.click()
            search_input = self.driver.find_element(
                By.XPATH, '//input[@type="text"]')
            search_input.send_keys(phrase)
            search_input.submit()
        except ImportError as exception:
            logging.error("Error searching for phrase: %s", exception)
        except NoSuchElementException:
            logging.error("Overlay found trying again...")
            self.search_phrase(phrase=phrase)

    def get_categorys(self) -> dict:
        """
        Extracts and returns categories from the webpage as a dictionary where keys are category names and values are the corresponding input values.
        
        :return: A dictionary of categories.
        """
        logging.info("Extracting categories...")
        categories = {}
        try:
            toggle_open_filter = self.driver.find_element(
                By.XPATH, "//div[@class='SearchFilter-heading']")
            toggle_open_filter.click()
            toggle_open_all_filter = self.driver.find_element(
                By.XPATH, "//button[@class='SearchFilter-seeAll-button']")
            toggle_open_all_filter.click()
            filter_items = self.driver.find_elements(
                By.CSS_SELECTOR, ".SearchFilter-items-item")
            for item in filter_items:
                span_text = item.find_element(
                    By.CSS_SELECTOR, ".CheckboxInput-label span").text
                input_value = item.find_element(
                    By.CSS_SELECTOR, "input").get_attribute("value")
                categories[span_text] = input_value

            logging.info("Extracted categories: %s", categories)
        except ImportError as exception:
            logging.error(
                "An error occurred while extracting categories: %s", exception)

        return categories

    def go_to_next_page(self):
        """
        Navigates to the next page of results and waits for the page to fully load.
        """
        logging.info("Going to the next page.")
        try:
            pagination_div = self.driver.find_element(
                By.CLASS_NAME, "Pagination-nextPage")
            next_page_link = pagination_div.find_element(By.TAG_NAME, "a")
            next_page_link.click()
            WebDriverWait(
                self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "SearchResultsModule-results")))
        except NoSuchElementException as exception:
            logging.error(
                f"Element not found: {exception}. This may be due to changes in the page structure.")

        except TimeoutException as exception:
            logging.error(
                f"Timeout while waiting for the page to load: {exception}. The page or element might be taking too long to load.")

        except ImportError as exception:
            logging.error(
                f"An unexpected error occurred: {exception}. Please check the details for more information.")

        logging.info("Next page has loaded successfully.")

    @staticmethod
    def is_article_in_range_time(last_article: WebElement, max_date: datetime):
    
        last_article_date = datetime.fromtimestamp(
            (int(
                last_article.find_element(
                    By.TAG_NAME,
                    "bsp-timestamp").get_attribute('data-timestamp'))) /
            1000.0)

        return (
            last_article_date.year,
            last_article_date.month) >= (
            max_date.year,
            max_date.month)

    def get_last_articles_in_range_time(self, articles, max_date):
        last_article_in_range = -2
        while True:
            if self.is_article_in_range_time(
                    articles[last_article_in_range], max_date):
                return articles[0:last_article_in_range + 1]
            last_article_in_range -= 1

    def open_categories(self) -> None:
        """
        Function to click the SVG element that opens the categories.
        """
        logging.info("Attempting to click the categories toggle button.")

        try:
            toggle_open_filter = self.driver.find_element(
                By.XPATH, "//div[@class='SearchFilter-heading']")
            toggle_open_filter.click()
            toggle_open_all_filter = self.driver.find_element(
                By.XPATH, "//button[@class='SearchFilter-seeAll-button']")
            toggle_open_all_filter.click()

            logging.info("Successfully clicked the categories toggle button.")
        except Exception as e:
            logging.error(
                f"Failed to click the categories toggle button: {str(e)}")

    def get_articles_element_on_date(
            self,
            max_date: datetime,
            categories_value: list,
            has_category: bool) -> WebElement:
        logging.info("Extracting articles...")
        validated_articles_element = []
        try:
            sort_by_element = self.driver.find_element(
                By.XPATH, "//select[@class='Select-input']")
            sort_by_ui = Select(sort_by_element)
            sort_by_ui.select_by_visible_text("Newest")
            self.refresh_and_wait_for_body()
            WebDriverWait(self.driver, 10).until(lambda driver: driver.execute_script(
                'return document.readyState') == 'complete')
            if has_category:
                self.open_categories()
                self.check_categories(categories_values=categories_value)
            articles_scraped = self.get_article_element()
            while self.is_article_in_range_time(
                    articles_scraped[-1], max_date):
                validated_articles_element.append(articles_scraped)
                self.go_to_next_page()
                articles_scraped = self.get_article_element()

            if self.is_article_in_range_time(articles_scraped[0], max_date):
                validated_articles_element.append(
                    self.get_last_articles_in_range_time(
                        articles_scraped, max_date))

        except NoSuchElementException:
            logging.error("Articles werent found: stopping application...")
            raise
        except Exception as exception:
            logging.error("Error to extract articles: %s", exception)

        return list(itertools.chain(*validated_articles_element))

    def check_categories(self, categories_values: list, timeout=10) -> None:
        """
            Clicks on a checkbox based on the 'value' attribute.
            :param value: The 'value' attribute of the checkbox to click.
        """
        logging.info(
            "Starting to find and click the checkbox with the values: %s",
            ", ".join(categories_values))

        try:
            for value in categories_values:
                time.sleep(0.5)
                WebDriverWait(
                    self.driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//input[@type='checkbox' and @value='{value}']")))

                checkbox = self.driver.find_element(
                    By.XPATH, f"//input[@type='checkbox' and @value='{value}']")

                if checkbox and not checkbox.is_selected():
                    checkbox.click()
                    logging.info(
                        "Successfully clicked the checkbox with value: %s", value)
                else:
                    logging.warning(
                        "Checkbox with value '%s' is already selected or not found.", value)
        except NoSuchElementException:
            logging.error("Overlay found trying again...")
            self.check_categories(categories_values, timeout=10)
        except ImportError as exception:
            logging.error(
                "An error occurred while trying to click the checkbox: %s",
                exception)

        self.refresh_and_wait_for_body()

    def refresh_and_wait_for_body(self, timeout=10):
        """
        Refreshes the page and waits until the body of the page is fully loaded.

        :param driver: The Selenium WebDriver instance.
        :param timeout: Maximum time to wait for the body to load (in seconds).
        """
        try:
            # Refresh the page
            self.driver.refresh()
            logging.info("Page refreshed")

            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "SearchResultsModule-results"))
            )
            logging.info("Body element is fully loaded")

        except Exception as e:
            logging.error(f"Error waiting for the body to load: {e}")
            raise

    def get_article_element(self, timeout=10):
        try:
            logging.info("getting article")
            WebDriverWait(
                self.driver,
                timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                    "//div[contains(@class, 'SearchResultsModule-results')]//div[contains(@class, 'PageList-items-item') and count(.//div[contains(@class, 'PagePromo')]) > 0 and count(.//div[contains(@class, 'PagePromoTrending')]) = 0]")))
            articles_scraped = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'SearchResultsModule-results')]//div[contains(@class, 'PageList-items-item') and count(.//div[contains(@class, 'PagePromo')]) > 0 and count(.//div[contains(@class, 'PagePromoTrending')]) = 0]")
        except Exception as e:
            logging.error(f"Error getting articles: {e}")

        return articles_scraped

    def extract_useful_data_from_articles(self,
                                          phrase: str,
                                          max_date: datetime,
                                          categories_value: list[str],
                                          is_categorized: bool) -> list[dict]:
        articles_element = self.get_articles_element_on_date(
            max_date=max_date,
            categories_value=categories_value,
            has_category=is_categorized)
        ExtractArticleDataType = list[
            dict[str, str],
            dict[str, datetime],
            dict[str, str],
            dict[str, str],
            dict[str, int],
            dict[str, bool]
        ]

        formated_articles_data: ExtractArticleDataType = []
        try:
            for article_element in articles_element:
                article_data = {
                    "title": extract_title(article_element),
                    "date": extract_date(article_element),
                    "description": extract_description(article_element),
                    "image_filename": extract_image_filename(article_element),
                    "search_count": extract_search_count(article_element, phrase),
                    "contains_money": extract_contains_money(article_element),
                    "picture_url": extract_picture_url(article_element)
                }

                formated_articles_data.append(article_data)

            self.download_picture(formated_articles_data)
        except Exception as e:
            logging.error(f"Error extracting useful data: {e}")        
        return formated_articles_data

    def download_picture(self, formated_articles: list[dict]) -> None:
        save_directory = get_news_images_dir_value()
        try:
            for formated_article in formated_articles:
                self.open_site(formated_article["picture_url"])
                file_name = format_to_allowed_filename(
                    formated_article["image_filename"])
                self.driver.find_element(By.TAG_NAME, 'img').screenshot(
                    f"{save_directory}{file_name}.png")
        except Exception as e:
            logging.error(f"Error downloading images: {e}")

@staticmethod
def extract_title(element: WebElement) -> str:
    try:
        title_element = element.find_element(By.CLASS_NAME, "PagePromo-title")
        return title_element.text
    except Exception as e:
        print(f"Error extracting title: {e}")
        return None


@staticmethod
def extract_date(element: WebElement) -> datetime:
    try:
        date_article = datetime.fromtimestamp(
            (int(
                element.find_element(
                    By.TAG_NAME,
                    "bsp-timestamp").get_attribute('data-timestamp'))) /
            1000.0)

        return date_article
    except Exception as e:
        print(f"Error extracting title: {e}")
        return None


@staticmethod
def extract_description(element: WebElement) -> str:
    try:
        description_element = element.find_element(
            By.CLASS_NAME, "PagePromo-description")
        return description_element.text
    except Exception as e:
        print(f"Error extracting description: {e}")
        return None


@staticmethod
def extract_image_filename(element: WebElement) -> str:
    try:
        div_image_element = element.find_element(
            By.CLASS_NAME, "PagePromo-media")
        filename = div_image_element.find_element(
            By.TAG_NAME, "a").get_attribute('aria-label')
        return filename
    except Exception as e:
        print(f"Error extracting image filename: {e}")
        return None


@staticmethod
def extract_search_count(element: WebElement, search_phrase: str,) -> int:
    try:
        count_search_phrase = element.text.lower().count(search_phrase.lower())
        return count_search_phrase
    except Exception as e:
        print(f"Error extracting search count: {e}")
        return 0


@staticmethod
def extract_contains_money(element: WebElement) -> bool:
    try:
        text = element.text
        money_patterns = [
            r'\$\d+(?:\.\d+)?',
            r'\$\d{1,3}(?:,\d{3})+(?:\.\d{2})',
            r'\b\d+\s+dollars\b',
            r'\b\d+\s+USD\b'
        ]

        patterns = [re.compile(pattern, re.IGNORECASE)
                    for pattern in money_patterns]
        contains_money = any(pattern.search(text) for pattern in patterns)

        return contains_money
    except Exception as e:
        print(f"Error checking for money formats: {e}")
        return False


@staticmethod
def extract_picture_url(element: WebElement) -> None:
    try:
        div_image_element = element.find_element(By.CLASS_NAME, "PagePromo-media")
        picture_element = div_image_element.find_element(By.TAG_NAME, "picture")
        img_url = picture_element.find_element(
            By.CLASS_NAME, "Image").get_attribute("src")
    except Exception as e:
        logging.error(f"Error extracting picture url: {e}")    
    return img_url
