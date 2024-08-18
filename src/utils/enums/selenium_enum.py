"""
Enums for web scraping and automation tasks.

This module defines various enumerations used for locating elements on a webpage, sorting options,
and HTTP status codes. These enums provide a set of constants that represent different attributes,
selectors, and options commonly used in web scraping or automation tasks.

Classes:
- Locator: Defines XPath and CSS selectors for locating elements on a webpage.
- SortBy: Defines sorting options.
- HttpCode: Defines HTTP status codes.
"""

from enum import Enum


class Locator(Enum):
    """
    Enum for storing XPath and CSS selectors used for locating elements on a webpage.

    This class defines a set of constants that represent various locators 
    (e.g., XPaths, CSS selectors)
    for different elements on a webpage. These locators can be used with web scraping or 
    automation tools to interact with specific elements on the page.

    Attributes:
        OVERLAY_XPATH: XPath for the overlay element.
        CLOSE_BUTTON_XPATH: XPath for the close button.
        SEARCH_BUTTON_XPATH: XPath for the search button.
        SEARCH_INPUT_XPATH: XPath for the search input field.
        FILTER_TOGGLE_XPATH: XPath for the filter toggle.
        FILTER_SEE_ALL_BUTTON_XPATH: XPath for the "see all" button in filters.
        FILTER_ITEMS_CSS_SELECTOR: CSS selector for filter items.
        CHECKBOX_CSS_SELECTOR: CSS selector for checkbox inputs.
        CHECKBOX_INPUT_LABEL_SPAN: CSS selector for checkbox input label spans.
        SORT_BY_XPATH: XPath for the sort-by dropdown.
        ARTICLE_XPATH: XPath for article items.
        PAGE_PROMO_TITLE_CLASS_NAME: Class name for the page promo title.
        PAGE_PROMO_DESCRIPTION_CLASS_NAME: Class name for the page promo description.
        PAGE_PROMO_MEDIA_CLASS_NAME: Class name for the page promo media.
        IMAGE_TAG_NAME: Tag name for image elements.
        PICTURE_TAG_NAME: Tag name for picture elements.
        IMAGE_CLASS_NAME: Class name for image elements.
        TIMESTAMP_TAG_NAME: Tag name for timestamp elements.
        DATA_TIMESTAMP: Data attribute for timestamps.
        PAGINATION_NEXT_PAGE_CLASS: Class name for the next page button in pagination.
        SEARCH_RESULTS_CLASS: Class name for search results container.
        INPUT: Tag name for input elements.
        TAG_A: Tag name for anchor elements.
        ELEMENT_READY_STATE: JavaScript expression to check document readiness state.
        COMPLETE: Value for complete document readiness state.
        ARIA_LABEL: ARIA label attribute.
        SOURCE: Attribute name for image sources.
        CATEGORIES_XPATH: XPath for category checkboxes.
    """
    OVERLAY_XPATH = "//div[contains(@class, 'fancybox-overlay')]"
    CLOSE_BUTTON_XPATH = "//a[contains(@class, 'fancybox-close')]"
    SEARCH_BUTTON_XPATH = "//button[@class='SearchOverlay-search-button']"
    SEARCH_INPUT_XPATH = '//input[@type="text"]'
    FILTER_TOGGLE_XPATH = "//div[@class='SearchFilter-heading']"
    FILTER_SEE_ALL_BUTTON_XPATH = "//button[@class='SearchFilter-seeAll-button']"
    FILTER_ITEMS_CSS_SELECTOR = ".SearchFilter-items-item"
    CHECKBOX_CSS_SELECTOR = "input[type='checkbox']"
    CHECKBOX_INPUT_LABEL_SPAN = ".CheckboxInput-label span"
    SORT_BY_XPATH = "//select[@class='Select-input']"
    ARTICLE_XPATH = "//div[contains(@class, 'SearchResultsModule-results')]//div[contains(@class, 'PageList-items-item') and count(.//div[contains(@class, 'PagePromo')]) > 0 and count(.//div[contains(@class, 'PagePromoTrending')]) = 0]"
    PAGE_PROMO_TITLE_CLASS_NAME = "PagePromo-title"
    PAGE_PROMO_DESCRIPTION_CLASS_NAME = "PagePromo-description"
    PAGE_PROMO_MEDIA_CLASS_NAME = "PagePromo-media"
    IMAGE_TAG_NAME = "img"
    PICTURE_TAG_NAME = "picture"
    IMAGE_CLASS_NAME = "Image"
    TIMESTAMP_TAG_NAME = "bsp-timestamp"
    DATA_TIMESTAMP = "data-timestamp"
    PAGINATION_NEXT_PAGE_CLASS = "Pagination-nextPage"
    SEARCH_RESULTS_CLASS = "SearchResultsModule-results"
    INPUT = "input"
    TAG_A = "a"
    ELEMENT_READY_STATE = "return document.readyState"
    COMPLETE = "complete"
    ARIA_LABEL = "aria-label"
    SOURCE = "src"
    CATEGORIES_XPATH = "//input[@type='checkbox']"


class SortBy(Enum):
    """
    Enum for sorting options.

    This class defines constants for sorting options used in web scraping or automation tasks.

    Attributes:
        NEWEST: Value representing the "Newest" sorting option.
    """
    NEWEST = "Newest"


class HttpCode(Enum):
    """
    Enum for HTTP status codes.

    This class defines constants for commonly used HTTP status codes in web scraping or 
    automation tasks.

    Attributes:
        HTTP_404: Value representing the HTTP 404 Not Found error.
    """
    HTTP_404 = "HTTP ERROR 404"
