import requests


def green(text):
    print(f"\033[92m{text}\033[0m")


def red(text):
    print(f"\033[91m{text}\033[0m")


def get_latest_django_version():
    response = requests.get("https://pypi.org/pypi/Django/json")
    if response.status_code == 200:
        data = response.json()
        full_version = data["info"]["version"]
        minor_version = ".".join(full_version.split(".")[0:2])
        return full_version, minor_version
    else:
        raise Exception("Failed to fetch the latest Django version")
