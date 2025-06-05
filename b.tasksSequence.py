from locust import HttpUser, TaskSet, task, between
import time
from bs4 import BeautifulSoup
url = "https://edupulse-qa.onrender.com/"

class UserBehavior(TaskSet):

    def on_start(self):
        """Get CSRF token before every login attempt"""
        response = self.client.get("/", name="Load Login Page")
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
        self.csrf_token = csrf_token
        self.logoutCount = 0

    @task
    def sequence_of_tasks(self):
        self.login()
        time.sleep(1)  
        #Other activities will come here.
        self.logout()

    def login(self):
        # Simulate login with a fake username
        payload = {
            "csrfmiddlewaretoken": self.csrf_token,
            "username": f"sarthak@tiet.com"
            "password": "a"  # Replace with actual password if needed
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": url
        }
        # Perform the POST login request
        with self.client.post("/", data=payload, headers=headers, name="Login Attempt", allow_redirects=True) as response:
            if "/usersdashboard/" not in response.text:
                response.failure("Login failed!")

    def logout(self):
        print(f"logout:{self.logoutCount}")
        self.logoutCount += 1
        with self.client.get("/logout/", name="Logout") as response:
            if response.status_code != 200:
                response.failure("Failed to logout")

class WebsiteUser(HttpUser):
    host = url
    tasks = [UserBehavior]
    wait_time = between(0, 0)  # No wait time between tasks
    #time.sleep(6)
