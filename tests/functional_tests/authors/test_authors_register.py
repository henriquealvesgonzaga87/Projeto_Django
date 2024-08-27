from . base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorsRegisterTest(AuthorsBaseTest):
    def get_by_place_holder(self, web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')
    
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )
    
    def form_field_test_with_call_back(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form=form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)

        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_place_holder(form, "Ex: John")
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_call_back(callback=callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_place_holder(form, "Ex: Doe")
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_call_back(callback=callback)

    def test_empty_username_error_message(self):
        def callback(form):
            last_name_field = self.get_by_place_holder(form, "Your username")
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn("This field can't be empty", form.text)
        self.form_field_test_with_call_back(callback=callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_place_holder(form, "Your email")
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.sleep()

            self.assertIn("example@example.com", form.text)
        self.form_field_test_with_call_back(callback=callback)

    def test_password_does_not_match(self):
        def callback(form):
            password1 = self.get_by_place_holder(form, "Type your password")
            password2 = self.get_by_place_holder(form, "Repeat your password")
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)

            form = self.get_form()
            self.sleep()

            self.assertIn("This field can't be empty", form.text)
        self.form_field_test_with_call_back(callback=callback)

    def test_user_valid_data_register_successfuly(self):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()

        self.get_by_place_holder(form, 'Ex: John').send_keys('First name')
        self.get_by_place_holder(form, 'Ex: Doe').send_keys('Last name')
        self.get_by_place_holder(form, 'Your username').send_keys('my_username')
        self.get_by_place_holder(form, 'Your email').send_keys('email@valid.com')
        self.get_by_place_holder(form, 'Type your password').send_keys('P@ssword1')
        self.get_by_place_holder(form, 'Repeat your password').send_keys('P@ssword1')

        form.submit()

        self.assertIn(
            'Your user is created, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )