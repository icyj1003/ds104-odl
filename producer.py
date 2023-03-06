import json
from kafka import KafkaProducer
import time
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import os
import json
from bs4 import BeautifulSoup


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


def clear():
    os.system('cls')


def create_snapshot(content, user):
    return {
        'content': content,
        'user': user,
        'timestamp': time.time()
    }


if __name__ == '__main__':
    # connect to current browser
    if os.path.isfile('C:/Users/ADMIN/Desktop/odl/config/remote_config.json'):
        with open('C:/Users/ADMIN/Desktop/odl/config/remote_config.json', "r") as file:
            remote_config = json.load(file)
    else:
        raise Exception('Config file not found!')
    driver = webdriver.Remote(
        command_executor=remote_config['command_executor'])

    driver.close()
    driver.session_id = remote_config['session_id']

    # init Kafka Producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=json_serializer,
                             key_serializer=json_serializer)

    posts = []

    user = None

    while True:

        # click all "Xem thêm" buttons
        try:
            buttons = driver.find_elements(
                by=By.XPATH, value='//div[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"]')
            for button in buttons:
                button.click()
        except:
            pass

        # load all visible posts
        loaded_posts = driver.find_elements(
            by=By.XPATH, value="//div[@class='x1lliihq']")
        # clear stdout
        clear()

        # add new post to posts
        currents = len(posts)
        for i in range(currents, len(loaded_posts)):
            child = loaded_posts[i].find_element(
                by=By.XPATH, value='./*').get_attribute('innerHTML')
            soup = BeautifulSoup(child, 'html.parser')
            try:
                user = str(soup.find(lambda tag: tag.name == 'a' and tag.get(
                    'class') == "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f".split()).text)
                content = str(soup.find('div', attrs={"dir": "auto"}).text)
                # create data stream here
                producer.send(topic='post', key=0,
                              value=create_snapshot(content, user))
                producer.flush()
                # add new post content to posts
                posts.append(content)
            except Exception as e:
                posts.append(None)
        time.sleep(3)
