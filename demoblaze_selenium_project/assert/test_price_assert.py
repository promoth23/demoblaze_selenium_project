import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.cart_page import CartPage
from utils.browser_setup import start_browser
from utils.helpers import log_to_excel, take_screenshot
from utils.logger import logger
from utils.popup import show_alert

@pytest.mark.smoke
def test_product_price_assertion():
    driver = start_browser()
    driver.get("https://www.demoblaze.com")
    login = LoginPage(driver)
    login.login("promoth", "promoth@851")
    time.sleep(2)

    cart = CartPage(driver)
    cart.add_samsung_to_cart()
    time.sleep(2)

    driver.get("https://www.demoblaze.com/cart.html")

    try:
        # ✅ Wait for Samsung S6 to appear in cart
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Samsung galaxy s6')]"))
        )
        # ✅ Wait for price to appear
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '360')]"))
        )
        price_text = price_element.text.strip()
        expected_price = "360"

        assert expected_price in price_text

        logger.info(f"✅ Product and price verified: Samsung Galaxy S6 = ${expected_price}")
        show_alert(driver, f"✅ Price matched: ${expected_price}")
        driver.switch_to.alert.accept()

        take_screenshot(driver, "price_verified")
        log_to_excel("Price Assertion Test", "PASS", f"Samsung S6 priced at ${expected_price}")

    except Exception as e:
        logger.error("❌ Price assertion failed or product missing in cart")
        show_alert(driver, "❌ Price assertion failed or product missing")
        driver.switch_to.alert.accept()

        take_screenshot(driver, "price_assertion_failed")
        log_to_excel("Price Assertion Test", "FAIL", "Samsung S6 price mismatch or not found")
        raise e

    finally:
        driver.quit()
