import requests


class ReqresAPI:
    BASE_URL = "http://0.0.0.0:8000"

    def get_users(self):
        return requests.get(f"{self.BASE_URL}/api/users/")

    def get_user(self, user_id):
        return requests.get(f"{self.BASE_URL}/api/users/{user_id}")

    def login(self, email, password):
        return requests.post(f"{self.BASE_URL}/api/login", json={"email": email, "password": password})

    def create_user(self, payload):
        return requests.post(f"{self.BASE_URL}/api/users", json=payload)

    def update_user_put(self, user_id, payload):
        return requests.put(f"{self.BASE_URL}/api/users/{user_id}", json=payload)

    def update_user_patch(self, user_id, payload):
        return requests.patch(f"{self.BASE_URL}/api/users/{user_id}", json=payload)

    def delete_user(self, user_id):
        return requests.delete(f"{self.BASE_URL}/api/users/{user_id}")
