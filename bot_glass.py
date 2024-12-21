import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
import os
import base64
import time

# Tải CAPTCHA qua API 2Captcha
def solve_captcha(captcha_image, api_key):
    image_data = base64.b64encode(captcha_image.getvalue()).decode("utf-8")
    payload = {
        "method": "base64",
        "key": api_key,
        "body": image_data,
        "json": 1
    }
    response = requests.post("http://2captcha.com/in.php", data=payload)
    captcha_id = response.json().get("request")
    
    # Chờ kết quả
    attempts = 0
    while attempts < 5:
        res = requests.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1")
        result = res.json()
        if result.get("status") == 1:
            return result.get("request")
        attempts += 1
        time.sleep(5)
    raise Exception("Failed to solve CAPTCHA after 5 attempts.")

# Selenium phần đăng nhập
options = Options()
driver = webdriver.Chrome(service=Service("D:/bot_get_jobs/chromedriver-win64/chromedriver.exe"), options=options)

try:
    # Lấy thông tin đăng nhập từ biến môi trường
    email = os.getenv("doanhieunghia560@gmail.com")
    password = os.getenv("kannahashimoto")
    api_key = os.getenv("36008c85749644460fe0c5d43ce48711")

    # Mở trang đăng nhập của Glassdoor
    driver.get("https://www.glassdoor.com/profile/login_input.htm")

    # Chờ nút xuất hiện và click
    google_login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'gd-ui-button')]"))
    )
    google_login_button.click()

    # Chờ CAPTCHA (nếu có)
    try:
        captcha_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='captcha']"))
        )
        captcha_image = BytesIO(captcha_element.screenshot_as_png)
        captcha_solution = solve_captcha(captcha_image, api_key)
        print(f"Captcha Solved: {captcha_solution}")

        # Nhập kết quả CAPTCHA
        captcha_input = driver.find_element(By.XPATH, "//input[@id='captcha']")
        captcha_input.send_keys(captcha_solution)
        captcha_input.send_keys(Keys.RETURN)
    except Exception:
        print("CAPTCHA không xuất hiện.")

    # Nhập email và mật khẩu
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
    )
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
    )
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Kiểm tra đăng nhập thành công
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='user-profile']"))  # Thay bằng thành phần cụ thể sau khi đăng nhập
    )
    print("Đăng nhập thành công!")

except Exception as e:
    print(f"Lỗi xảy ra: {e}")

finally:
    driver.quit()
