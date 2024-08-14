import logging
import time
from datetime import datetime
import itertools
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from utils.enums.selenium_locators_enum import Locator, SortBy


from utils.values_utils import  get_output_dir_value
from utils.strings_utils import format_to_allowed_filename


class CustomSelenium:
    def __init__(self):
        logging.info("Starting configuration")

        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument('--remote-debugging-port=9222')
            chrome_options.add_argument("--disable-cookies")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            prefs = {
                        "download.default_directory": os.path.abspath(get_output_dir_value()),  
                        "download.prompt_for_download": False,       
                        "download.directory_upgrade": True,
                        "safebrowsing.enabled": True
                        }
            chrome_options.add_experimental_option("prefs", prefs)

            service = Service(ChromeDriverManager().install())

            self._driver = webdriver.Chrome(
                service=service, options=chrome_options)

            logging.basicConfig(level=logging.INFO)

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
        self.close_cookies()
        try:
            overlay_present = len(
                self.driver.find_elements(
                    By.XPATH,
                    Locator.OVERLAY_XPATH.value)) > 0

            if overlay_present:
                print("overlay apareceu")
                logging.info("Overlay detected, attempting to close")
                close_button = self.driver.find_element(
                    By.XPATH, Locator.CLOSE_BUTTON_XPATH.value)
                close_button.click()
                logging.info("Overlay closed successfully")
                print("overlay foi fechada")
                return True

        except Exception as e:
            logging.error("Overlay not found or other error: %s", e)
        
        return False

    def close_cookies(self):
        try:
            self.driver.execute_script("document.querySelector('#onetrust-consent-sdk').style.display = 'none';")
        except Exception:
            logging.warning("Doenst have any cookie on the page")

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


    def get_categories(self) -> dict:
        """
        Extracts and returns categories from the webpage 
        as a dictionary where keys are category names and values are the corresponding input values.
        
        :return: A dictionary of categories.
        """
        logging.info("Extracting categories...")
        self.close_cookies()
        categories = {}
        try:
            toggle_open_filter = self.driver.find_element(
                By.XPATH, Locator.FILTER_TOGGLE_XPATH.value)
            toggle_open_filter.click()
            toggle_open_all_filter = self.driver.find_element(
                By.XPATH, Locator.FILTER_SEE_ALL_BUTTON_XPATH.value)
            toggle_open_all_filter.click()
            filter_items = self.driver.find_elements(
                By.CSS_SELECTOR, Locator.FILTER_ITEMS_CSS_SELECTOR.value)
            for item in filter_items:
                span_text = item.find_element(
                    By.CSS_SELECTOR, Locator.CHECKBOX_INPUT_LABEL_SPAN.value).text
                input_value = item.find_element(
                    By.CSS_SELECTOR, Locator.INPUT.value).get_attribute("value")
                categories[span_text] = input_value

            logging.info("Extracted categories: %s", categories)
        except ImportError as exception:
            logging.error(
                "An error occurred while extracting categories: %s", exception)
        except NoSuchElementException as exception:
            logging.warning("Not found categories in site")
        except ElementNotInteractableException:
            is_overlay_present = self.close_overlay()
            if is_overlay_present:
                self.get_categories()
        return categories

    def go_to_next_page(self, timeout=120):
        """
        Navigates to the next page of results and waits for the page to fully load.
        """
        logging.info("Going to the next page.")
        self.close_cookies()
        try:
            pagination_div = self.driver.find_element(
                By.CLASS_NAME, Locator.PAGINATION_NEXT_PAGE_CLASS.value)
            next_page_link = pagination_div.find_element(By.TAG_NAME,  Locator.TAG_A.value)
            next_page_link.click()
            WebDriverWait(
                self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, Locator.SEARCH_RESULTS_CLASS.value)))
        except NoSuchElementException as exception:
            logging.error(
                f"Element not found: {exception}. This may be due to don't have a next page")

        except TimeoutException as exception:
            logging.error(
                f"Timeout while waiting for the page to load: {exception}. The page or element might be taking too long to load.")

        except ImportError as exception:
            logging.error(
                f"An unexpected error occurred: {exception}. Please check the details for more information.")

        logging.info("Next page has loaded successfully.")
        self.close_cookies()

    @staticmethod
    def is_article_in_range_time(last_article: WebElement, max_date: datetime):
        """
        Determines if the article's date is within the specified maximum date range.

        :param last_article: WebElement representing the article.
        :param max_date: The maximum date to check against.
        :return: Tuple indicating whether the article's date is within the max_date.
        """
    
        last_article_date = datetime.fromtimestamp(
            (int(
                last_article.find_element(
                    By.TAG_NAME,
                    Locator.TIMESTAMP_TAG_NAME.value).get_attribute(Locator.DATA_TIMESTAMP.value))) /
            1000.0)

        return (
            last_article_date.year,
            last_article_date.month) >= (
            max_date.year,
            max_date.month)

    def get_last_articles_in_range_time(self, articles, max_date):
        """
        Retrieves the articles within the specified date range.

        :param articles: List of articles to filter.
        :param max_date: The maximum date to include articles.
        :return: List of articles within the date range.
        """
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
                By.XPATH, Locator.FILTER_TOGGLE_XPATH.value)
            toggle_open_filter.click()
            toggle_open_all_filter = self.driver.find_element(
                By.XPATH, Locator.FILTER_SEE_ALL_BUTTON_XPATH.value)
            toggle_open_all_filter.click()

            logging.info("Successfully clicked the categories toggle button.")
        except ElementClickInterceptedException:
            is_overlay_present = self.close_overlay()
            if is_overlay_present:
                self.open_categories()
        except Exception as e:
            logging.error(
                f"Failed to click the categories toggle button: {str(e)}")

    def get_articles_element_on_date(
            self,
            max_date: datetime,
            categories_value: list,
            has_category: bool) -> WebElement:
        """
        Retrieves article elements within a specified date range and category.

        :param max_date: The maximum date to include articles.
        :param categories_value: List of category values to filter articles by.
        :param has_category: Boolean indicating if a category filter should be applied.
        :return: List of WebElements representing articles.
        """
        logging.info("Extracting articles...")
        validated_articles_element = []
        try:
            self.sort_by_newest()
            WebDriverWait(self.driver, 10).until(lambda driver: driver.execute_script(
                Locator.ELEMENT_READY_STATE.value) == Locator.COMPLETE.value)
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
        except Exception:
            logging.error("Error to extract articles")
            return []

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
            self.close_cookies()
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
        except ElementNotInteractableException:
            is_overlay_present = self.close_overlay()
            if is_overlay_present:
                self.check_categories(categories_values)
        except ImportError as exception:
            logging.error(
                "An error occurred while trying to click the checkbox: %s",
                exception)

        self.refresh_and_wait_for_categories()

    def sort_by_newest(self):
        """
        Sorts the elements on the page by 'Newest' using the sort dropdown.

        This function locates the sorting dropdown element on the page, 
        selects the 'Newest' option, and then refreshes the page to wait 
        for the results to be updated.

        Raises:
            NoSuchElementException: If the sort dropdown is not found on the page.
            UnexpectedTagNameException: If the located element is not a <select> tag.
        """
        logging.info("Attempting to sort items by 'Newest'.")
        
        try:
            sort_by_element = self.driver.find_element(By.XPATH, Locator.SORT_BY_XPATH.value)
            sort_by_ui = Select(sort_by_element)
            sort_by_ui.select_by_visible_text(SortBy.NEWEST.value)           
            self.refresh_and_wait_for_sort_results()
            logging.info("Page refreshed and waiting for results to be updated.")
        
        except Exception as e:
            logging.error(f"An error occurred while attempting to sort by 'Newest': {e}")
            raise

    def refresh_and_wait_for_sort_results(self, timeout=5):
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
                    (By.CLASS_NAME, Locator.SEARCH_RESULTS_CLASS.value))
            )
            logging.info("Page result sorted")

        except Exception as e:
            logging.error(f"Error to sort page")

        
    def refresh_and_wait_for_categories(self, timeout=5):
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
                    (By.XPATH, Locator.CATEGORIES_XPATH.value))
            )
            logging.info("Categories element is fully loaded")

        except Exception:
            logging.error(f"Error waiting categories: Categories not found, your search is blank")
            raise

    def get_article_element(self, timeout=10):
        """
        Waits for and retrieves article elements from the page.

        :param timeout: Maximum time to wait for articles to load (in seconds).
        :return: List of WebElements representing articles.
        """
        try:
            logging.info("getting article")
            WebDriverWait(
                self.driver,
                timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH,Locator.ARTICLE_XPATH.value)))
            articles_scraped = self.driver.find_elements(
                By.XPATH,Locator.ARTICLE_XPATH.value)
        except NoSuchElementException:
            logging.error(f"No articles were found: stopping application")
            raise
        except Exception:
            logging.error(f"No articles were found: stopping application ")
            raise

        return articles_scraped

    def extract_useful_data_from_articles(self,
                                          phrase: str,
                                          max_date: datetime,
                                          categories_value: list[str],
                                          is_categorized: bool) -> list[dict]:
        """
        Extracts useful data from articles based on specified criteria.

        :param phrase: The search phrase to count occurrences in article content.
        :param max_date: The maximum publication date for filtering articles.
        :param categories_value: List of categories to filter articles.
        :param is_categorized: Boolean indicating whether the articles are categorized.
        :return: A list of dictionaries containing extracted data from each article.
        """
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
            if articles_element:
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

                self.download_pictures(formated_articles_data)
            else:
                return []
        except Exception as e:
            logging.error(f"Error extracting useful data: {e}")
        self.driver_quit()        
        return formated_articles_data

    def download_pictures(self, formated_articles: list[dict]) -> None:
        """
        Downloads pictures based on article data and saves them to a directory.

        :param formated_articles: List of dictionaries containing article data including picture URLs.
        """
        
        try:
            for formated_article in formated_articles:
                image_url =formated_article["picture_url"]
                self.open_site(image_url)
                
                file_name = format_to_allowed_filename(formated_article["image_filename"])
                self.driver.execute_script(f"""
                var image = document.querySelector('img');
                var link = document.createElement('a');
                link.href = image.src;
                link.download = '{file_name}';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                """)
                time.sleep(0.5)

                
        except Exception as e:
            logging.error(f"Error downloading images: {e}")


    def extract_picture_url(self, element: WebElement, timeout=10) -> None:
        """
        Extracts the URL of the picture from the given article WebElement.

        :param element: The WebElement representing the article.
        :return: The extracted picture URL as a string.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, Locator.PAGE_PROMO_MEDIA_CLASS_NAME.value))
                )
            div_image_element = element.find_element(By.CLASS_NAME, Locator.PAGE_PROMO_MEDIA_CLASS_NAME.value)
            picture_element = div_image_element.find_element(By.TAG_NAME, Locator.PICTURE_TAG_NAME.value)
            img_url = picture_element.find_element(
                By.CLASS_NAME, Locator.IMAGE_CLASS_NAME.value).get_attribute(Locator.SOURCE.value)
        except Exception as e:
            logging.error(f"Error extracting picture url: {e}")    
        return img_url


@staticmethod
def extract_title(element: WebElement) -> str:
    """
    Extracts the title from the given article WebElement.

    :param element: The WebElement representing the article.
    :return: The extracted title as a string.
    """
    try:
        title_element = element.find_element(By.CLASS_NAME, Locator.PAGE_PROMO_TITLE_CLASS_NAME.value)
        return title_element.text
    except Exception as e:
        print(f"Error extracting title: {e}")
        return None


@staticmethod
def extract_date(element: WebElement) -> datetime:
    """
    Extracts the publication date from the given article WebElement.

    :param element: The WebElement representing the article.
    :return: The extracted publication date as a datetime object.
    """
    try:
        date_article = datetime.fromtimestamp(
            (int(
                element.find_element(
                    By.TAG_NAME,
                    Locator.TIMESTAMP_TAG_NAME.value).get_attribute(Locator.DATA_TIMESTAMP.value))) /
            1000.0)

        return date_article
    except Exception as e:
        print(f"Error extracting title: {e}")
        return None


@staticmethod
def extract_description(element: WebElement) -> str:
    """
    Extracts the description from the given article WebElement.

    :param element: The WebElement representing the article.
    :return: The extracted description as a string.
    """
    try:
        description_element = element.find_element(
            By.CLASS_NAME, Locator.PAGE_PROMO_DESCRIPTION_CLASS_NAME.value)
        return description_element.text
    except Exception as e:
        print(f"Error extracting description: {e}")
        return None


@staticmethod
def extract_image_filename(element: WebElement) -> str:
    """
    Extracts the image filename from the given article WebElement.

    :param element: The WebElement representing the article.
    :return: The extracted image filename as a string.
    """
    try:
        div_image_element = element.find_element(
            By.CLASS_NAME, Locator.PAGE_PROMO_MEDIA_CLASS_NAME.value)
        filename = div_image_element.find_element(
            By.TAG_NAME, Locator.TAG_A.value).get_attribute(Locator.ARIA_LABEL.value)
        return format_to_allowed_filename(filename)
    except Exception as e:
        print(f"Error extracting image filename: {e}")
        return None


@staticmethod
def extract_search_count(element: WebElement, search_phrase: str,) -> int:
    """
    Counts occurrences of a search phrase in the article content.

    :param element: The WebElement representing the article.
    :param search_phrase: The phrase to count in the article content.
    :return: The count of occurrences of the search phrase.
    """
    try:
        count_search_phrase = element.text.lower().count(search_phrase.lower())
        return count_search_phrase
    except Exception as e:
        print(f"Error extracting search count: {e}")
        return 0


@staticmethod
def extract_contains_money(element: WebElement) -> bool:
    """
    Checks if the article contains any monetary values.

    :param element: The WebElement representing the article.
    :return: True if the article contains monetary values, False otherwise.
    """
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