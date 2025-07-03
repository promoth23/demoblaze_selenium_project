from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.home_page import HomePage
from utils.browser_setup import start_browser
from utils.helpers import take_screenshot, log_to_excel
from utils.logger import logger
from utils.popup import show_alert
import time

def test_full_flow():
    driver = start_browser()
    driver.get("https://www.demoblaze.com")
    logger.info("🔵 Opened demoblaze.com")

    login = LoginPage(driver)
    show_alert(driver, "🔐 Logging in...")
    driver.switch_to.alert.accept()

    login.login("promoth", "promoth@851")
    time.sleep(2)

    # 🔒 Assert login
    try:
        assert "Welcome promoth" in driver.page_source
        logger.info("✅ Login success")
        take_screenshot(driver, "login_attempt")
        login_result = "✅ Login Successful"
    except AssertionError:
        logger.error("❌ Login failed")
        take_screenshot(driver, "login_failed")
        show_alert(driver, "❌ Login Failed")
        driver.switch_to.alert.accept()
        login_result = "❌ Login Failed"
        log_to_excel(login_result, "", "")
        driver.quit()
        return

    # 🛒 Add to cart
    cart = CartPage(driver)
    cart.add_samsung_to_cart()
    time.sleep(2)
    take_screenshot(driver, "added_s6")
    logger.info("🛒 Samsung Galaxy S6 added")

    # 🔒 Assert cart
    driver.get("https://www.demoblaze.com/cart.html")
    try:
        assert "samsung galaxy s6" in driver.page_source.lower()
        cart_result = "✅ Samsung Galaxy S6 added to cart"
        logger.info(cart_result)
    except AssertionError:
        cart_result = "❌ Samsung Galaxy S6 NOT found in cart"
        logger.error(cart_result)
        take_screenshot(driver, "cart_failed")

    # 🔍 Search iPhone 16
    home = HomePage(driver)
    home.search_product("iPhone 16")
    time.sleep(2)
    take_screenshot(driver, "iphone_not_found")

    try:
        assert "iphone 16" not in driver.page_source.lower()
        search_result = "✅ iPhone 16 not found as expected"
        logger.info(search_result)
    except AssertionError:
        search_result = "❌ Unexpected search result for iPhone 16"
        logger.error(search_result)
        take_screenshot(driver, "iphone_found")

    show_alert(driver, "❌ iPhone 16 not found")
    driver.switch_to.alert.accept()

    # 🧾 Log to Excel
    log_to_excel(login_result, cart_result, search_result)

    driver.quit()
