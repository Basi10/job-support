import script.logger as logging
import time
from typing import Union
from urllib.parse import ParseResult
import RPA.Browser.Selenium as Selenium


class Browser:
    #%%
    def __init__(self, selenium: Selenium):
        self.selenium = selenium
        self.logger = logging.setup_logger('./output/browser_action.log')

    def open_browser(self, url: Union[str, ParseResult]):
        """
        This method allows you to open a browser
        using selenium with any available browser in you environment.
        :param url: the url to open
        """
        self.selenium.open_available_browser(url)

    def maximize_browser(self):
        """
        This method allows you to maximize a browser
        """
        self.selenium.maximize_browser()

    def search_browser(self, url: Union[str, ParseResult]):
        """
        This method allows you to search a browser
        :param url: the url to open
        :return:
        """
        self.selenium.go_to(url)

    def close(self):
        """
        This method allows you to close a browser
        :return:
        """
        self.selenium.close_browser()


class LinkedIn(Browser):

    def __init__(self, selenium: Selenium):
        super().__init__(selenium)

    def retrieve_links(self):
        """
        This method allows you to retrieve the list of job posting links
        :return:
        """
        unordered_list = self.selenium.find_elements('class:base-card__full-link')
        link_list = [element.get_attribute('href') for element in unordered_list]
        self.logger.info(f'Retrieving {len(link_list)} links')
        return link_list

    def retrieve_description(self):
        """
        This method allows you to retrieve the description from a LinkedIn job posting
        :return: the job description in string format
        """
        try:
            self.selenium.wait_until_element_is_visible('class:show-more-less-button')
            self.selenium.wait_until_element_is_visible('class:description__text')
            self.selenium.click_element('class:show-more-less-button')
            description = self.selenium.find_element('class:description__text')
            self.logger.info('Successfully retrieved description from LinkedIn job posting')
            time.sleep(5)
            return description.text
        except Exception as e:
            self.logger.warn(e)
            return None
