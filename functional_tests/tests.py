import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import Keys

class RoutesFunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_searching_route_in_base(self):
        searched_route = 'Metallica'
        self.browser.get('http://127.0.0.1:8000/find_route/')
        search_box = self.browser.find_element_by_id('find_route')
        search_box.send_keys(searched_route)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)
        column=self.browser.find_elements_by_tag_name('td')
        self.assertIn(searched_route,[col.text for col in column])

    def test_searching_route_not_in_base(self):
        searched_route = 'Metallica123'
        not_in_base = 'There are no entries in this category yet...'
        self.browser.get('http://127.0.0.1:8000/find_route/')
        search_box = self.browser.find_element_by_id('find_route')
        search_box.send_keys(searched_route)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)
        column=self.browser.find_elements_by_tag_name('td')
        self.assertIn(not_in_base,[col.text for col in column])

