"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def log_in_to_admin_site(lstc):
    # open web browser, go to admin page
    lstc.browser.get(lstc.live_server_url + '/admin/')
    # see 'Django administration' heading
    body = lstc.browser.find_element_by_tag_name('body')
    # type username and password and hit enter
    username_field = lstc.browser.find_element_by_name('username')
    username_field.send_keys('blannon')
    password_field = lstc.browser.find_element_by_name('password')
    password_field.send_keys('cuibono')
    password_field.send_keys(Keys.RETURN)

class LoginTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_login_to_admin_site(self):
        # open web browser, go to admin page
        self.browser.get(self.live_server_url + '/admin/')

        # see 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration',body.text)

        # type username and password and hit enter
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('blannon')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('cuibono')
        password_field.send_keys(Keys.RETURN)

        # username and password accepted, taken to the Site Administration
        # page.
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

class AuthorTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_author_via_admin_site(self):
        # login
        log_in_to_admin_site(self)

        # see hyperlinks that say "Authors"
        authors_links = self.browser.find_elements_by_link_text('Authors')
        #time.sleep(10)
        #body = self.browser.find_element_by_tag_name('body')
        #print body.text
        self.assertEquals(len(authors_links), 1)

        # click on author link
        authors_links[0].click()

        # look at author page, see no authors yet
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 authors', body.text)

        # see link to 'add' a new author, click it
        new_author_link = self.browser.find_element_by_link_text('Add author')
        new_author_link.click()

        # see some input fields
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Name:', body.text)
        self.assertIn('Profile page URL:', body.text)

        # enter the author's name
        name_field = self.browser.find_element_by_name('name')
        name_field.send_keys("Joel Duffman")

        # enter the author's profile page
        profile_page_url_field = self.browser.find_element_by_name('profile_page_url')
        profile_page_url_field.send_keys("http://www.newslytimes.com/people/duffman")

        # click the save button
        save_button = self.browser.find_element_by_css_selector(
                "input[value='Save']")
        save_button.click()

        # returned to the "Authors" listing, see new author
        time.sleep(10)
        new_author_links = self.browser.find_elements_by_link_text(
                "Joel Duffman")
        self.assertEquals(len(new_author_links),1)


