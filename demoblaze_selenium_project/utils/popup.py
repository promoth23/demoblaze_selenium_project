def show_alert(driver, message):
    driver.execute_script(f"alert('{message}')")
