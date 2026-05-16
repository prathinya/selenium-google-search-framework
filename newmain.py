import logging

import pytest

from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


# =========================
# CONFIGURATION
# =========================

BASE_URL = "https://www.google.com/"
WAIT_TIME = 10


# =========================
# LOGGING CONFIGURATION
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()


# =========================
# DRIVER FACTORY
# =========================

def initialize_browser():

    service = Service(
        ChromeDriverManager().install()
    )

    driver = webdriver.Chrome(
        service=service
    )

    driver.maximize_window()

    return driver


# =========================
# PAGE OBJECT MODEL
# =========================

class GooglePage:

    SEARCH_BOX = (
        By.CLASS_NAME,
        "gLFyf"
    )

    def __init__(
        self,
        driver,
        wait_time
    ):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            wait_time
        )

    def open_google(
        self,
        url
    ):

        self.driver.get(url)

        logger.info(
            "Google homepage opened successfully."
        )

    def search_google(
        self,
        search_text
    ):

        search_box = self.wait.until(
            ec.element_to_be_clickable(
                self.SEARCH_BOX
            )
        )

        search_box.clear()

        search_box.send_keys(
            search_text + Keys.ENTER
        )

        logger.info(
            "Search executed successfully -> %s",
            search_text
        )

    def open_search_result(
        self,
        partial_text
    ):

        result_link = self.wait.until(
            ec.element_to_be_clickable(
                (
                    By.PARTIAL_LINK_TEXT,
                    partial_text
                )
            )
        )

        result_link.click()

        logger.info(
            "Search result opened successfully."
        )

    def validate_page_title(
        self,
        expected_text
    ):

        page_title = self.driver.title

        assert (
            expected_text.lower()
            in page_title.lower()
        ), (
            "Expected text not found "
            "in page title."
        )

        logger.info(
            "TEST PASSED -> Expected text "
            "found in page title."
        )


# =========================
# PYTEST FIXTURE
# =========================

@pytest.fixture
def driver():

    driver = initialize_browser()

    yield driver

    driver.quit()

    logger.info(
        "Browser closed successfully."
    )


# =========================
# PARAMETERIZED TEST
# =========================

@pytest.mark.parametrize(
    "search_text",
    [
        "Shark Tank",
        "Python Programming",
        "Selenium Automation"
    ]
)
def test_google_search(
    driver,
    search_text
):

    try:

        google_page = GooglePage(
            driver,
            WAIT_TIME
        )

        google_page.open_google(
            BASE_URL
        )

        google_page.search_google(
            search_text
        )

        google_page.open_search_result(
            search_text
        )

        google_page.validate_page_title(
            search_text
        )

    except TimeoutException as error:

        logger.error(
            "Timeout occurred: %s",
            error
        )

        pytest.fail(
            "Test failed due to timeout."
        )

    except WebDriverException as error:

        logger.error(
            "WebDriver issue occurred: %s",
            error
        )

        pytest.fail(
            "Test failed due to WebDriver issue."
        )

    except Exception as error:

        logger.error(
            "Unexpected error occurred: %s",
            error
        )

        pytest.fail(
            "Unexpected test failure."
        )


# =========================
# MAIN EXECUTION
# =========================

if __name__ == "__main__":

    pytest.main(
        [
            "-v",
            "--html=report.html"
        ]
    )
