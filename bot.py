from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import username, pwd
import time
import random


class InstagramBot():

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd
        self.browser = webdriver.Chrome("webdrivers/chromedriver.exe")
        # xpath элемента страницы из несуществующей сслылки
        self.xpath_wrong_url = "/html/body/div[1]/section/main/div/div/h2"
        # xpath кнопки лайка
        self.xpath_like_button = "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button"
        # нужно для put_like_on_all_posts(), xpath кол-ства постов
        self.xpath_post_count = "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span"
        # xpath прошедшего времени с момента публикации поста
        self.xpath_post_age = "/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[2]/a/time"

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser

        browser.get('https://instagram.com/')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name("username")
        username_input.clear()
        username_input.send_keys(self.username)
        time.sleep(3)

        password_input = browser.find_element_by_name("password")
        password_input.clear()
        password_input.send_keys(self.pwd)
        time.sleep(3)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    def like_post_by_hashtag(self, hashtag, post_count):

        browser = self.browser

        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        # Как много бот соберет постов для лайка 1 = ~8 постов
        for i in range(1, post_count):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        # находит все ссылки на странице
        hrefs = browser.find_elements_by_tag_name('a')

        # перебирает все ссылки найденые на странице и оставляет только публикации
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:

            browser.get(url)
            time.sleep(3)

            if self.xpath_exist(self.xpath_wrong_url):
                continue
            else:
                post_age = browser.find_element_by_xpath(self.xpath_post_age).text

                time_name = post_age.split(" ")[1]
                time_names = ["SECOND", "SECONDS", "MINUTE", "MINUTES"]

                if time_name in time_names:
                    like_button = browser.find_element_by_xpath(self.xpath_like_button).click()
                    # врямя между лайками
                    # для акка < 3 мес 30 дайствий в час и 120 в день
                    # для акка > 6 мес 60 дайствий в час и 1604 в день
                    # если в среднем взять 40 лайков в час 3600 / 40 = 90
                    time.sleep(random.randrange(80, 100))
                else:
                    continue

    def xpath_exist(self, xpath):

        browser = self.browser

        try:
            browser.find_element_by_xpath(xpath)
            exist = True
        except Exception:
            exist = False
        return exist

    # Ставим лайк по прямой ссылке
    def put_like_by_link(self, url_post):

        browser = self.browser

        browser.get(url_post)
        time.sleep(3)

        if self.xpath_exist(self.xpath_wrong_url):
            print("Can not find link")
            self.close_browser()
        else:
            like_button = browser.find_element_by_xpath(self.xpath_like_button).click()
            time.sleep(5)
            self.close_browser()

    # Ставим лайки под всеми постами по ссылке на профиль
    def put_like_on_all_posts(self, profile_url):
        # БАГ!!! при попытке обработать кол-ство постов если их >999

        browser = self.browser

        browser.get(profile_url)
        time.sleep(3)

        if self.xpath_exist(self.xpath_wrong_url):
            print("Can not find user")
            self.close_browser()
        else:
            # кол-ство постов на странице
            post_count = int(browser.find_element_by_xpath(self.xpath_post_count).text)
            # инстаграм отдает по 12 постов за прокрутку, поэтому узнем сколько нужно прокруток
            loops_count = int(post_count / 12)

            posts_urls = []

            for _ in range(0, loops_count):

                # находит все ссылки на странице
                hrefs = browser.find_elements_by_tag_name('a')

                # перебирает все ссылки найденые на странице и оставляет только публикации
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

            file_name = profile_url.split('/')[-2]

            with open(f"{file_name}.txt", 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f"{file_name}_set.txt", "a") as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

            with open(f"{file_name}_set.txt", 'r') as file:
                urls_links = file.readline()

                for post_url in urls_links:
                    browser.get(post_url)
                    time.sleep(2)
                    like_button = browser.find_element_by_xpath(self.xpath_like_button).click()
                    time.sleep(random.randrange(80, 110))

            self.close_browser()
