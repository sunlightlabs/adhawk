"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import LiveServerTestCase
from selenium import webdriver

class IssueTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_issue_via_admin_site(self):
        # open web browser, go to admin page
        self.browser.get(self.live_server_url + '/admin/')

        # see 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration',body.text)

        # TODO: use the admin site to create an Issue
        self.fail('finish this test')
