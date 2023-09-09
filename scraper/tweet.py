from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException


class Tweet:
    def __init__(self, card: Chrome) -> None:
        self.card = card

        self.user = card.find_element(
            'xpath',
            './/div[@data-testid="User-Name"]//span'
        ).text

        try:
            self.handle = card.find_element(
                'xpath',
                './/span[contains(text(), "@")]'
            ).text
        except NoSuchElementException:
            return

        try:
            self.date_time = card.find_element(
                'xpath',
                './/time'
            ).get_attribute('datetime')

            if self.date_time is not None:
                self.is_ad = False
        except NoSuchElementException:
            self.is_ad = True
            return

        try:
            card.find_element(
                'xpath',
                './/*[local-name()="svg" and @data-testid="icon-verified"]'
            )

            self.verified = True
        except NoSuchElementException:
            self.verified = False

        self.content = ""
        contents = card.find_elements(
            'xpath',
            './/div[@data-testid="tweetText"]/span | .//div[@data-testid="tweetText"]/a'
        )

        for index, content in enumerate(contents):
            self.content += content.text

        try:
            self.reply_cnt = card.find_element(
                'xpath',
                './/div[@data-testid="reply"]//span'
            ).text
        except NoSuchElementException:
            self.reply_cnt = '0'

        try:
            self.retweet_cnt = card.find_element(
                'xpath',
                './/div[@data-testid="retweet"]//span'
            ).text
        except NoSuchElementException:
            self.retweet_cnt = '0'

        try:
            self.like_cnt = card.find_element(
                'xpath',
                './/div[@data-testid="like"]//span'
            ).text
        except NoSuchElementException:
            self.like_cnt = '0'

        try:
            self.analytics_cnt = card.find_element(
                'xpath',
                './/a[contains(@href, "/analytics")]//span'
            ).text
        except NoSuchElementException:
            self.analytics_cnt = '0'

        try:
            self.profile_img = card.find_element(
                'xpath',
                './/div[@data-testid="Tweet-User-Avatar"]//img'
            ).get_attribute('src')
        except NoSuchElementException:
            self.profile_img = ''

        self.tweet = (
            self.user,
            self.handle,
            self.date_time,
            self.verified,
            self.content,
            self.reply_cnt,
            self.retweet_cnt,
            self.like_cnt,
            self.analytics_cnt,
            self.profile_img
        )

        pass
