"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdrive.common.keys import Keys

class LoginTest(LiveServerTestCase):

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
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('adm1n')
        password_field.send_keys(Keys.RETURN)

        # username and password accepted, taken to the Site Administration
        # page.
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

class AuthorTest(LoginTest):
    def test_can_create_new_author_via_admin_site(self):
        # see hyperlinks that say "Authors"
        self.fail('finish this test')

        
