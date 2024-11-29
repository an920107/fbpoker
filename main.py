from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from log import log

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)
driver.get("https://www.facebook.com/pokes")

with open("cookies.txt") as f:
    cookies_text = f.readline().strip().split(";")
    for cookie_text in cookies_text:
        cookie = cookie_text.strip().split("=")
        driver.add_cookie({"name": cookie[0], "value": cookie[1]})
driver.get("https://www.facebook.com/pokes")

refresh_count = 0
try:
    while True:
        if refresh_count == 20:
            driver.refresh()
            refresh_count = 0

        spans = driver.find_elements(By.TAG_NAME, "span")

        for span in spans:
            try:
                if span.get_attribute("innerHTML") == "戳回去":
                    span.click()
                    message_span = span.find_element(
                        By.XPATH, f"{'../' * 9}div[1]//a/.."
                    )
                    log(message_span.text, "access.log")
            except StaleElementReferenceException:
                pass
            except Exception as e:
                now = datetime.now()
                log(f"{type(e)}", "access.log", now)
                log(f"{type(e)}\n{e}", "error.log", now)

        spans.clear()
        refresh_count += 1
        sleep(20)

except KeyboardInterrupt:
    driver.quit()
