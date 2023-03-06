import json
import time
from selenium import webdriver


def main():
    driver = webdriver.Edge()
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    runtime_limit = 600  # minutes
    remote_config = {'command_executor': executor_url,
                     'session_id': session_id}
    with open("C:/Users/ADMIN/Desktop/odl/config/remote_config.json", "w") as file:
        json.dump(remote_config, file)
    driver.get('https://www.facebook.com/')

    time.sleep(runtime_limit * 60)


if __name__ == '__main__':
    main()
