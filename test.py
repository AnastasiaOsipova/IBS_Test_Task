import pytest
from api import API
from page_object import HeadPage
from selenium import webdriver


class TestTask:

    driver = None
    request_buttons_list = ["users", "users-single", "users-single-not-found", "unknown", "unknown-single",
                            "unknown-single-not-found", "post", "put", "patch", "delete", "register-successful",
                            "register-unsuccessful", "login-successful", "login-unsuccessful", "delay"]

    def setup_class(cls):
        path = "chromedriver.exe"
        cls.driver = webdriver.Chrome(path)
        cls.web = HeadPage(cls.driver)
        cls.api = API()
        cls.driver.maximize_window()

    def setup(self):
        # Зайти на главную страницу
        url = "https://reqres.in/"
        self.driver.get(url)

        self.go_teardown = True

    def test_get_second_page_users(self):
        # get by api
        self.api_json, api_status_code = self.api.get_users(page=2)

        # get by web
        self.web.click_request_button(self.request_buttons_list[0])
        # compare status_code,
        self.web.compare_status_code(api_status_code)
        self.web_json = self.web.get_response_text()

    @pytest.mark.parametrize("user_id, request_button", [(2, request_buttons_list[1]), (23, request_buttons_list[2])])
    def test_get_user_by_id(self, user_id, request_button):
        # get users by correct user_id=2 and non_correct user_id=23
        # get by api
        self.api_json, api_status_code = self.api.get_users(user_id=user_id)

        # get by web
        self.web.click_request_button(request_button)
        # compare status_code,
        self.web.compare_status_code(api_status_code)
        self.web_json = self.web.get_response_text()

    @pytest.mark.parametrize("user_id, request_button", [(None, request_buttons_list[3]), (2, request_buttons_list[4]),
                                                         (23, request_buttons_list[5])])
    def test_get_unknown(self, user_id, request_button):
        # get resource withno user_id, by correct user_id=2 and non_correct user_id=23
        # get by api
        self.api_json, api_status_code = self.api.get_resource(user_id=user_id)

        # get by web
        self.web.click_request_button(request_button)
        # compare status_code,
        self.web.compare_status_code(api_status_code)
        self.web_json = self.web.get_response_text()

    def test_create_user(self):
        # don't run teardown
        self.go_teardown = False
        # post api
        self.api_json, api_status_code = self.api.create_user(name="morpheus", job="leader")

        # get by web
        self.web.click_request_button(self.request_buttons_list[6])
        # compare status_code,
        self.web.compare_status_code(api_status_code)
        self.web_json = self.web.get_response_text()

        # compare api and web responses
        assert self.api_json['name'] == self.web_json['name']
        assert self.api_json['job'] == self.web_json['job']

    def test_update_user(self):
        # don't run teardown
        self.go_teardown = False
        # put user by api
        self.api_json, api_status_code = self.api.update_user(name="morpheus", job="zion resident", user_id=2)

        # put user by web
        self.web.click_request_button(self.request_buttons_list[7])
        # compare status_code,
        self.web.compare_status_code(api_status_code)
        self.web_json = self.web.get_response_text()

        # compare api and web responses
        assert self.api_json['name'] == self.web_json['name']
        assert self.api_json['job'] == self.web_json['job']

    def test_patch_user(self):
        # don't run teardown
        self.go_teardown = False
        # post api
        self.api_json, api_status_code = self.api.patch_user(name="morpheus", job="zion resident", user_id=2)

        # get by web
        self.web.click_request_button(self.request_buttons_list[8])
        # compare status_code,
        self.web.compare_status_code(api_status_code)
        self.web_json = self.web.get_response_text()

        # compare api and web responses
        assert self.api_json['name'] == self.web_json['name']
        assert self.api_json['job'] == self.web_json['job']

    def test_delete_user(self):
        # don't run teardown
        self.go_teardown = False
        # delete by api
        api_status_code = self.api.delete_user()

        # delete by web
        self.web.click_request_button(self.request_buttons_list[9])

        # compare status_code,
        self.web.compare_status_code(api_status_code)

    @pytest.mark.parametrize("email, password, request_button",
                             [("eve.holt@reqres.in", "pistol", request_buttons_list[10]),
                              ("sydney@fife", None, request_buttons_list[11])])
    def test_register_user(self, email, password, request_button):
        # post api
        self.api_json, api_status_code = self.api.register_user(email=email, password=password)

        # get by web
        self.web.click_request_button(request_button)
        self.web_json = self.web.get_response_text()

        # compare status_code, gotten by api and by web
        self.web.compare_status_code(api_status_code)

    @pytest.mark.parametrize("email, password, request_button",
                             [("eve.holt@reqres.in", "cityslicka", request_buttons_list[12]),
                              ("peter@klaven", None, request_buttons_list[13])])
    def test_login(self, email, password, request_button):
        # post api
        self.api_json, api_status_code = self.api.login(email=email, password=password)

        # get by web
        self.web.click_request_button(request_button)
        self.web_json = self.web.get_response_text()

        # compare status_code, gotten by api and by web
        self.web.compare_status_code(api_status_code)

    def test_get_user_with_delay(self):
        # get by api
        self.api_json, api_status_code = self.api.get_users(delay=3)

        # get by web
        self.web.click_request_button(self.request_buttons_list[14])
        # compare status_code,
        self.web.compare_status_code(api_status_code)
        self.web_json = self.web.get_response_text()

    def teardown(self):
        if self.go_teardown:
            # compare api and web responses
            assert self.api_json == self.web_json

    def teardown_class(cls):
        cls.driver.quit()
