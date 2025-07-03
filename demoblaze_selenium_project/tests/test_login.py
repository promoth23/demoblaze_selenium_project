# tests/test_login.py

import time
import pytest
from pages.login_page import LoginPage
from utils.browser_setup import start_browser
from utils.logger import logger
from utils.popup import show_alert
from utils.helpers import take_screenshot, log_to_excel
from selenium.common.exceptions import UnexpectedAlertPresentException

@pytest.mark.smoke
def test_login():
    driver = start_browser()
    driver.get("https://www.demoblaze.com")
    login = LoginPage(driver)

    try:
        logger.info("🔐 Starting login test with invalid credentials")
        show_alert(driver, "🔐 Testing login")
        driver.switch_to.alert.accept()

        login.login("wronguser", "wrongpass")
        time.sleep(2)

        # ✅ Handle potential alert (wrong credentials pop-up)
        try:
            alert = driver.switch_to.alert
            logger.warning(f"⚠️ Alert appeared: {alert.text}")
            alert.accept()
        except:
            logger.info("✅ No alert present after login attempt")

        assert "Welcome" not in driver.page_source, "❌ Unexpected login success for invalid credentials"
        logger.info("✅ Login test passed (invalid credentials correctly blocked)")

        take_screenshot(driver, "invalid_login")
        log_to_excel("test_login", "Passed", "Invalid credentials rejected")

    except AssertionError as e:
        logger.error(str(e))
        take_screenshot(driver, "invalid_login_failed")
        log_to_excel("test_login", "Failed", str(e))
        raise

    except UnexpectedAlertPresentException as e:
        alert_text = driver.switch_to.alert.text
        logger.error(f"❌ Unexpected alert: {alert_text}")
        take_screenshot(driver, "unexpected_alert")
        log_to_excel("test_login", "Failed", f"Unexpected alert: {alert_text}")
        raise

    finally:
        show_alert(driver, "❌ Invalid credentials")
        driver.switch_to.alert.accept()
        driver.quit()
