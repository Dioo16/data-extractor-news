from enum import Enum

class Locator(Enum):
    OVERLAY_XPATH = "//div[contains(@class, 'fancybox-overlay')]"
    CLOSE_BUTTON_XPATH = "//a[contains(@class, 'fancybox-close')]"
    SEARCH_BUTTON_XPATH = "//button[@class='SearchOverlay-search-button']"
    SEARCH_INPUT_XPATH = '//input[@type="text"]'
    FILTER_TOGGLE_XPATH = "//div[@class='SearchFilter-heading']"
    FILTER_SEE_ALL_BUTTON_XPATH = "//button[@class='SearchFilter-seeAll-button']"
    FILTER_ITEMS_CSS_SELECTOR = ".SearchFilter-items-item"
    CHECKBOX_CSS_SELECTOR = "input[type='checkbox']"
    CHECKBOX_INPUT_LABEL_SPAN =".CheckboxInput-label span"
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
    
class SortBy(Enum):
    NEWEST = "Newest"
