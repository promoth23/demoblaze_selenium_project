# pages/cart_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.popup import show_alert
from utils.logger import logger


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_samsung_to_cart(self):
        try:
            logger.info("🔍 Searching for Samsung Galaxy S6...")

            # ✅ Wait and click on the product link
            phone = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6"))
            )
            phone.click()

            # ✅ Wait for 'Add to cart' button and click it
            add_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']"))
            )
            add_btn.click()

            # ✅ Wait for and accept the alert
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()

            logger.info("🛒 Samsung Galaxy S6 added to cart and alert accepted")

        except (NoSuchElementException, TimeoutException) as e:
            show_alert(self.driver, "❌ Samsung Galaxy S6 not found on page")
            logger.error("❌ Samsung Galaxy S6 element not found")
            raise


