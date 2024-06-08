from locust import HttpUser, task, between, TaskSet
from requests.auth import HTTPBasicAuth

class UserBehavior(TaskSet):

    def on_start(self):
        # Endpoint logowania
        login_url = "/user/login"
        # Dane logowania
        username = "your_username"
        password = "your_password"
        
        # Wysłanie żądania logowania z Basic Auth
        response = self.client.post(login_url, json={"username": username, "password": password})
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            print("Login failed:", response.text)
            self.token = None

    @task(1)
    def fetch_data(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/fetch", headers=headers)

    @task(1)
    def list_cars(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/all_cars", headers=headers)

    @task(1)
    def get_car(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/car/1", headers=headers)  # Przykładowe ID samochodu, dostosuj według potrzeb

    @task(1)
    def add_car(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/addcar", json={"make": "Test", "model": "Test Model"}, headers=headers)

    @task(1)
    def fill_db(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/fill_db", json=[{"make": "Test", "model": "Test Model"}], headers=headers)

    @task(1)
    def upload_image(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        files = {'file': ('test.jpg', open('test.jpg', 'rb'), 'image/jpeg')}
        self.client.post("/upload", headers=headers, files=files)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)