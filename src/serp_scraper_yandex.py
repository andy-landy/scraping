"""
Gets urls and thumbs for search queries without extra web requests
"""

from collections import OrderedDict
import datetime
import random
import time
import urllib

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

from i_serp_scraper import ISerpScraper


class SerpScraperYandex(ISerpScraper):
    def __init__(self, browser_config, logger):
        self.browser_config = browser_config
        self.logger = logger
        
        self.driver = None

    def start(self):
        self.driver = webdriver.Chrome(executable_path='../../bin/chromedriver', service_log_path='./active_page.driver.log')  # TODO param

    def close(self):
        self.driver.quit()

    def scrap_image_urls_and_thumbs(self, query, count, filters):
        params = {'text': query}
        params.update(filters)
        self.driver.get('https://yandex.ru/images/search?' + urllib.parse.urlencode(params))
        
        self.move_mouse_around(self.driver.find_elements_by_class_name('websearch-button')[0])
       
        url_to_thumb = OrderedDict()
        
        empty_trials = 0
        while len(url_to_thumb) < count and empty_trials < 5:
            old_thumb_count = len(url_to_thumb)

            for a in self.driver.find_elements_by_class_name('serp-item__link'):
                if extract_url(a) in url_to_thumb:
                    continue

                try:
                    url_to_thumb[extract_url(a)] = extract_thumb(a)
                except WebDriverException as e:
                    pass

                if len(url_to_thumb) >= count:
                    break

            empty_trials = 0 if old_thumb_count != len(url_to_thumb) else (empty_trials + 1)
    
            self.driver.execute_script('window.scrollBy(0, 50)')
            self.driver.execute_script('window.scrollBy(0, 50)')
            self.driver.execute_script('window.scrollBy(0, 50)')
            self.driver.execute_script('window.scrollBy(0, 50)')
            time.sleep(random.random() + 1)

        return list(url_to_thumb.items())
        
    def save_screenshot(self):
        self.driver.save_screenshot('screenshot.{}.png'.format(datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')))    

    def move_mouse_around(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element)

        vx = random.randint(5, 10)
        vy = random.randint(5, 10)
        t = 0.8
        for _ in range(2):
            actions.move_by_offset(vx, vy)
            vx = (1.0 - t) * vx + t * random.randint(-10, 10)
            vy = (1.0 - t) * vy + t * random.randint(-10, 10)

        actions.perform()


def extract_url(a):
    return urllib.parse.parse_qs(urllib.parse.urlsplit(a.get_attribute('href')).query)['img_url'][0]


def extract_thumb(a):
    return a.find_elements_by_tag_name('img')[0].screenshot_as_png
