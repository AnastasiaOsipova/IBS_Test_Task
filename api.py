import requests


class API:

    def __init__(self):
        self.site_url = 'https://reqres.in/api'
        self.headers = {"Access-Token": None,
                        "Accept": "application/json",
                        "Content-Type": "application/json"}

    # button_list = ["users", "users-single", "users-single-not-found", "unknown", "unknown-single"]

    def create_user(self, name=None, job=None):

        data = {
            "name": name,
            "job": job
        }

        response = requests.post(f"{self.site_url}/users", json=data, headers=self.headers)
        return response.json(), response.status_code

    def update_user(self, name=None, job=None, user_id=None):

        data = {
            "name": name,
            "job": job
        }

        response = requests.put(f"{self.site_url}/users/{user_id}", json=data, headers=self.headers)
        return response.json(), response.status_code

    def patch_user(self, user_id=None, **kwargs):

        # if kwargs:
        data = {}
        for key, value in kwargs.items():
            data[key] = value

        response = requests.patch(f"{self.site_url}/users/{user_id}", json=data, headers=self.headers)
        return response.json(), response.status_code

    def register_user(self, email=None, password=None):

        data = {
            "email": email,
            "password": password
        }

        response = requests.post(f"{self.site_url}/register", json=data, headers=self.headers)
        return response.json(), response.status_code

    def login(self, email, password):

        data = {
            "email": email,
            "password": password
        }

        response = requests.post(f"{self.site_url}/login", json=data, headers=self.headers)
        return response.json(), response.status_code

    def get_users(self, user_id=None, **kwargs):

        params = {}
        for key, value in kwargs.items():
            params[key] = value

        if user_id:
            response = requests.get(f"{self.site_url}/users/{user_id}", params=params, headers=self.headers)
        else:
            response = requests.get(f"{self.site_url}/users", params=params, headers=self.headers)
        return response.json(), response.status_code

    def get_resource(self, user_id=None):

        if user_id:
            response = requests.get(f"{self.site_url}/unknown/{user_id}", headers=self.headers)
        else:
            response = requests.get(f"{self.site_url}/unknown", headers=self.headers)
        return response.json(), response.status_code

    def delete_user(self, user_id=None):

        response = requests.delete(f"{self.site_url}/users/{user_id}", headers=self.headers)
        return response.status_code
