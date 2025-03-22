import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'Pass123456'
        user = User.objects.create_user(username='my_user', password=string_password)
        
        # user open the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # user see the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_place_holder(form, 'Type your username')
        password_field = self.get_by_place_holder(form, 'Type your password')

        # user insert the login data
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # user send the login form
        form.submit()

        # user see the success message
        self.assertIn(f'You are logged in with {user.username}.', self.browser.find_element(By.TAG_NAME, 'body').text)
        
    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn('Not Found', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_is_invalid(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        username = self.get_by_place_holder(form, 'Type your username')
        password = self.get_by_place_holder(form, 'Type your password')

        username.send_keys(' ')
        password.send_keys(' ')

        form.submit()

        self.assertIn('Invalid username or password', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_invalid_credentials(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        username = self.get_by_place_holder(form, 'Type your username')
        password = self.get_by_place_holder(form, 'Type your password')

        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        form.submit()

        self.assertIn('Invalid credentials', self.browser.find_element(By.TAG_NAME, 'body').text)
        self.assertIn('Invalid credentials', self.browser.find_element(By.TAG_NAME, 'body').text)
