from locust import HttpUser, task, between, events
import re
import random

# Global counters
success_count = 0
failure_count = 0

class LoginLogoutUser(HttpUser):
    wait_time = between(1, 3)

    login_url = "/"         # login page
    logout_url = "/logout/" # logout page

    # List of username/password tuples for testing success and failure
    credentials = [
        ("tempuser1@temp.com", ""),        # assumed valid user, empty password if accepted
        ("tempuser1@temp.com", "wrongpw"), # invalid password
        ("invaliduser@example.com", "pw"), # invalid user
    ]

    def on_start(self):
        response = self.client.get(self.login_url)
        self.csrf_token = self.extract_csrf_token(response.text)
        self.logged_in = False

    def extract_csrf_token(self, text):
        match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\'](.*?)["\']', text)
        return match.group(1) if match else ""

    @task
    def login_logout_sequence(self):
        global success_count, failure_count

        username, password = random.choice(self.credentials)

        login_data = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": self.csrf_token,
        }

        with self.client.post(
            self.login_url,
            data=login_data,
            headers={"Referer": self.host + self.login_url},
            name="Login",
            catch_response=True,
        ) as response:
            # Determine login success: if redirected or dashboard shown
            if response.status_code == 200 and "/usersdashboard/" in response.url:
                response.success()
                self.logged_in = True
                success_count += 1
                print(f"Login success for {username}")
            else:
                response.failure(f"Login failed for {username}: {response.status_code} - {response.url}")
                failure_count += 1
                self.logged_in = False
                print(f"Login failed for {username}")

        self.wait()

        if self.logged_in:
            with self.client.get(
                self.logout_url,
                name="Logout",
                catch_response=True,
            ) as response:
                if response.status_code in [200, 302]:
                    response.success()
                    print(f"Logout success for {username}")
                else:
                    response.failure(f"Logout failed: {response.status_code}")

            # Refresh CSRF token for next login
            response = self.client.get(self.login_url)
            self.csrf_token = self.extract_csrf_token(response.text)
            self.logged_in = False


@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    print(f"\n===== TEST SUMMARY =====")
    print(f"Total Successful Logins: {success_count}")
    print(f"Total Failed Logins: {failure_count}")
    print("========================\n")
