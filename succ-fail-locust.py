from locust import HttpUser, task, between
from random import choice, randint
import time

valid_users = [("user1", "pass1"), ("user2", "pass2"), ("user3", "pass3"),
               ("user4", "pass4"), ("user5", "pass5"), ("user6", "pass6")]
# Insert 4 invalid ones
invalid_users = [("user7", "wrong1"), ("user8", "wrong2"),
                 ("user9", "wrong3"), ("user10", "wrong4")]

total_success = 0
total_fail = 0

class QAPerfUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        global total_success, total_fail

        self.username, self.password = choice(valid_users + invalid_users)
        with self.client.post("", data={"username": self.username, "password": self.password}, catch_response=True) as response:
            if "Dashboard" in response.text:
                response.success()
                total_success += 1
                self.logged_in = True
            else:
                response.failure("Login failed")
                total_fail += 1
                self.logged_in = False

    @task
    def perform_actions(self):
        if not self.logged_in:
            self.environment.runner.quit()  # stop failed users from continuing
            return

        menu_paths = ["/TODO_PAGE", "/settings", "/usersdashboard"]
        for path in menu_paths:
            with self.client.get(path, name="Menu Item") as response:
                time.sleep(5)

        self.client.get("/logout", name="Logoff")
        self.environment.runner.quit()

    def on_stop(self):
        print(f"User {self.username} finished. Logged in: {self.logged_in}")
