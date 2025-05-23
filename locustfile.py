from locust import HttpUser, task, between
from bs4 import BeautifulSoup

class LoginUser(HttpUser):
    wait_time = between(1, 3)  # Simulate user "think time"

    def on_start(self):
        """Get CSRF token before every login attempt"""
        response = self.client.get("/", name="Load Login Page")
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
        self.csrf_token = csrf_token

    @task
    def login(self):
        # Simulate login with a fake username
        payload = {
            "csrfmiddlewaretoken": self.csrf_token,
            "username": f"tempuser{self.environment.runner.user_count}@temp1.com"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://qa-perf.onrender.com/"
        }

        # Perform the POST login request
        with self.client.post("/", data=payload, headers=headers, name="Login Attempt", allow_redirects=True) as response:
            if "/usersdashboard/" not in response.text:
                response.failure("Login failed!")