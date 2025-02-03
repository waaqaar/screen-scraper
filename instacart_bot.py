from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

REMOTE_CHROME_URL = "http://localhost:4444/wd/hub"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
INSTACART_URL = "https://www.instacart.com/"


class WebDriverHandler:
    def __init__(self, remote_url, user_agent, window_size="1920,1080"):
        """
        Initializes the WebDriverHandler instance with desired options and capabilities.

        Args:
            remote_url (str): URL of the remote Selenium WebDriver.
            user_agent (str): Custom User-Agent string.
            window_size (str): Window size for the browser (default is "1920,1080").
        """
        self.remote_url = remote_url
        self.user_agent = user_agent
        self.window_size = window_size
        self.driver = None

    def configure_options(self):
        """
        Configures Chrome options for the WebDriver to avoid detection and improve compatibility.

        Returns:
            Options: Configured Chrome options.
        """
        options = Options()

        # Set custom User-Agent
        options.add_argument(f"user-agent={self.user_agent}")

        # Browser configuration
        options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
        options.add_argument(f"--window-size={self.window_size}")  # Set window size
        options.add_argument("--no-sandbox")  # Disable sandboxing for stability
        options.add_argument("--disable-extensions")  # Disable extensions
        options.add_argument("--disable-gpu")  # Disable GPU
        options.add_argument("--incognito")  # Enable incognito mode
        options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors

        return options

    def start_driver(self):
        """
        Starts the WebDriver with the configured options.

        Returns:
            webdriver.Remote: The initialized WebDriver instance.
        """
        chrome_options = self.configure_options()

        # Initialize the remote WebDriver
        self.driver = webdriver.Remote(
            command_executor=self.remote_url,
            options=chrome_options  # Use options instead of desired_capabilities
        )
        return self.driver

    def open_page(self, url, wait_time=10):
        """
        Opens a webpage and waits for the page to load.

        Args:
            url (str): The URL of the webpage to open.
            wait_time (int): Time to wait for the page to load (default is 5 seconds).
        """
        if not self.driver:
            raise RuntimeError("WebDriver is not initialized. Call start_driver() first.")

        self.driver.get(url)
        time.sleep(wait_time)  # Time to saty on page

    def get_page_source(self):
        """
        Fetches the HTML source of the currently loaded webpage.

        Returns:
            str: The HTML source of the webpage.
        """
        if not self.driver:
            raise RuntimeError("WebDriver is not initialized. Call start_driver() first.")

        return self.driver.page_source

    def close_driver(self):
        """
        Closes the WebDriver instance.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None


# Usage example
if __name__ == "__main__":

    # Instantiate the WebDriverHandler
    web_driver_handler = WebDriverHandler(REMOTE_CHROME_URL, USER_AGENT)

    try:
        # Start WebDriver
        driver = web_driver_handler.start_driver()

        # Open the page
        web_driver_handler.open_page(INSTACART_URL)

        # Get and print the page source
        html_source = web_driver_handler.get_page_source()
        print(html_source)

    finally:
        # Close the WebDriver
        web_driver_handler.close_driver()
