class Scroller:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.current_position = 0
        self.last_position = driver.execute_script("return window.pageYOffset;")
        self.scrolling = True
        self.scroll_count = 0
        pass

    def reset(self) -> None:
        self.current_position = 0
        self.last_position = self.driver.execute_script("return window.pageYOffset;")
        self.scroll_count = 0
        pass

    def scroll_to_top(self) -> None:
        self.driver.execute_script("window.scrollTo(0, 0);")
        pass

    def scroll_to_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pass

    def update_scroll_position(self) -> None:
        self.current_position = self.driver.execute_script("return window.pageYOffset;")
        pass
