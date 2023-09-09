import os
import sys
import pandas as pd
from progress import Progress
from scroller import Scroller
from tweet import Tweet

from datetime import datetime
from fake_headers import Headers
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager

TWITTER_LOGIN_URL = "https://twitter.com/i/flow/login"


class Twitter_Scraper():
    def __init__(self, username, password, max_tweets=50):
        print("Initializing Twitter Scraper...")
        self.username = username
        self.password = password
        self.data = []
        self.tweet_ids = set()
        self.max_tweets = max_tweets
        self.progress = Progress(0, max_tweets)
        self.tweet_cards = []
        self.driver = self._get_driver()
        self.scroller = Scroller(self.driver)
        self._login()

    def _get_driver(self):
        print("Setup WebDriver...")
        header = Headers().generate()['User-Agent']

        browser_option = ChromeOptions()
        browser_option.add_argument('--no-sandbox')
        browser_option.add_argument("--disable-dev-shm-usage")
        browser_option.add_argument('--ignore-certificate-errors')
        browser_option.add_argument('--disable-gpu')
        browser_option.add_argument('--log-level=3')
        browser_option.add_argument('--disable-notifications')
        browser_option.add_argument('--disable-popup-blocking')
        browser_option.add_argument('--user-agent={}'.format(header))

        # For Hiding Browser
        browser_option.add_argument("--headless")

        try:
            print("Initializing ChromeDriver...")
            driver = webdriver.Chrome(
                options=browser_option,
            )

            return driver
        except WebDriverException:
            try:
                print("Downloading ChromeDriver...")
                chromedriver_path = ChromeDriverManager().install()
                chrome_service = ChromeService(
                    executable_path=chromedriver_path)

                print("Initializing ChromeDriver...")
                driver = webdriver.Chrome(
                    service=chrome_service,
                    options=browser_option,
                )

                return driver
            except Exception as e:
                print(f"Error setting up WebDriver: {e}")
                sys.exit(1)

    def _login(self):
        print("Logging in to Twitter...")
        self.driver.get(TWITTER_LOGIN_URL)
        self.driver.maximize_window()
        sleep(3)

        self._input_username()
        self._input_unusual_activity()
        self._input_password()

        print("Login Successful")
        print()
        pass

    def _input_username(self):
        input_attempt = 0

        while True:
            try:
                username = self.driver.find_element(
                    "xpath",
                    "//input[@autocomplete='username']"
                )

                username.send_keys(self.username)
                username.send_keys(Keys.RETURN)
                sleep(3)
                break
            except NoSuchElementException:
                input_attempt += 1
                if input_attempt >= 3:
                    print()
                    print("""
There was an error inputting the username.

It may be due to the following:
- Internet connection is unstable
- Username is incorrect
- Twitter is experiencing unusual activity
                          """)
                    self.driver.quit()
                    sys.exit(1)
                else:
                    print("Re-attempting to input username...")

    def _input_unusual_activity(self):
        input_attempt = 0

        while True:
            try:
                unusual_activity = self.driver.find_element(
                    "xpath",
                    "//input[@data-testid='ocfEnterTextTextInput']"
                )
                unusual_activity.send_keys(self.username)
                unusual_activity.send_keys(Keys.RETURN)
                sleep(3)
                break
            except NoSuchElementException:
                input_attempt += 1
                if input_attempt >= 3:
                    break

    def _input_password(self):
        input_attempt = 0

        while True:
            try:
                password = self.driver.find_element(
                    "xpath",
                    "//input[@autocomplete='current-password']"
                )

                password.send_keys(self.password)
                password.send_keys(Keys.RETURN)
                sleep(3)
                break
            except NoSuchElementException:
                input_attempt += 1
                if input_attempt >= 3:
                    print()
                    print("""
There was an error inputting the password.

It may be due to the following:
- Internet connection is unstable
- Password is incorrect
- Twitter is experiencing unusual activity
                          """)
                    self.driver.quit()
                    sys.exit(1)
                else:
                    print("Re-attempting to input password...")

    def go_to_home(self):
        self.driver.get("https://twitter.com/home")
        sleep(3)
        pass

    def get_tweets(self):
        self.tweet_cards = self.driver.find_elements(
            'xpath',
            '//article[@data-testid="tweet"]'
        )
        pass

    def scrape_tweets(self, callback=None):
        if callback is None:
            callback = self.go_to_home

        callback()

        print("Scraping Tweets...")
        self.progress.print_progress(0)

        try:
            while self.scroller.scrolling:
                self.get_tweets()

                for card in self.tweet_cards[-15:]:
                    tweet_id = str(card)
                    if tweet_id not in self.tweet_ids:
                        self.tweet_ids.add(tweet_id)
                        tweet = Tweet(card)
                        if tweet:
                            if not tweet.is_ad:
                                self.data.append(tweet.tweet)
                                self.progress.print_progress(len(self.data))

                                if len(self.data) >= self.max_tweets:
                                    self.scroller.scrolling = False
                                    break

                                if len(self.data) % 50 == 0:
                                    sleep(2)

                if len(self.data) >= self.max_tweets:
                    break

                self.scroller.scroll_count = 0

                while True:
                    self.scroller.scroll_to_bottom()
                    sleep(2)
                    self.scroller.update_scroll_position()

                    if self.scroller.last_position == self.scroller.current_position:
                        self.scroller.scroll_count += 1

                        if self.scroller.scroll_count >= 3:
                            callback()
                            sleep(2)
                            self.scroller.reset()
                            break
                        else:
                            sleep(2)
                    else:
                        self.scroller.last_position = self.scroller.current_position
                        break

            print("\n")
            print("Scraping Complete")
        except StaleElementReferenceException:
            print("\n")
            print("Scraping Incomplete")

        print("Tweets: {} out of {}\n".format(len(self.data), self.max_tweets))

        pass

    def save_to_csv(self):
        print("Saving Tweets to CSV...")
        now = datetime.now()
        folder_path = './tweets/'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print("Created Folder: {}".format(folder_path))

        data = {
            'Name': [tweet[0] for tweet in self.data],
            'Handle': [tweet[1] for tweet in self.data],
            'Timestamp': [tweet[2] for tweet in self.data],
            'Verified': [tweet[3] for tweet in self.data],
            'Content': [tweet[4] for tweet in self.data],
            'Comments': [tweet[5] for tweet in self.data],
            'Retweets': [tweet[6] for tweet in self.data],
            'Likes': [tweet[7] for tweet in self.data],
            'Analytics': [tweet[8] for tweet in self.data],
            'Profile Image': [tweet[9] for tweet in self.data],
        }

        df = pd.DataFrame(data)

        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f'{folder_path}{current_time}_tweets_1-{len(self.data)}.csv'
        df.to_csv(file_path, index=False)

        print("CSV Saved: {}".format(file_path))

        pass
