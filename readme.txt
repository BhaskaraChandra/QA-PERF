Requirements for Installing Locust

1. Python 3.7 or newer installed on your system.
2. pip (Python package manager) installed.
3. (Optional) A virtual environment tool such as venv or virtualenv.

Installation Steps:

1. (Optional) Create and activate a virtual environment:
    python3 -m venv venv
    source venv/bin/activate

2. Install Locust using pip:
    pip install locust

3. Verify installation:
    locust --version

For more details, visit: https://docs.locust.io/

locust -f a.SingleUser.py
locust -f b.tasksSequence.py --headless -u 100 -r 10 --run-time 1h --csv=results
locust -f b.tasksSequence.py -u 100 -r 10 --run-time 10s
