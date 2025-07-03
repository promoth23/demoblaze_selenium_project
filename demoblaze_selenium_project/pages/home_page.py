from selenium.webdriver.common.by import By

class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def search_product(self, name):
        self.driver.find_element(By.LINK_TEXT, "Home").click()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
