from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Import Options từ selenium.webdriver.chrome.options
import time

# Tạo đối tượng Options
options = Options()
# Bạn có thể thêm các tùy chọn khác vào `options` nếu cần, ví dụ:
# options.add_argument("--headless")  # Chạy trình duyệt ở chế độ không có giao diện (headless)

# Khởi tạo WebDriver với Options
driver = webdriver.Chrome(service=Service("D:/bot_get_jobs/chromedriver-win64/chromedriver.exe"), options=options)

# Mở trang đăng nhập của Glassdoor
driver.get("https://www.glassdoor.com/profile/login_input.htm")

# Chờ cho trang tải xong
time.sleep(3)

# Click vào nút "Sign in with Google"
google_login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'gd-ui-button')]")
google_login_button.click()

# Chuyển hướng đến trang Google Sign-in
time.sleep(2)

# Nhập email và mật khẩu của Google
email_field = driver.find_element(By.XPATH, "//input[@type='email']")
email_field.send_keys("doanhieunghia560@gmail.com")  # Thay thế bằng email Google của bạn
email_field.send_keys(Keys.RETURN)

time.sleep(2)

password_field = driver.find_element(By.XPATH, "//input[@type='password']")
password_field.send_keys("kannahashimoto")  # Thay thế bằng mật khẩu Google của bạn
password_field.send_keys(Keys.RETURN)

# Chờ để quá trình đăng nhập hoàn thành
time.sleep(5)

# Kiểm tra nếu đăng nhập thành công bằng cách xác nhận URL hoặc một phần tử có sẵn trên trang sau đăng nhập
if "glassdoor.com" in driver.current_url:
    print("Đăng nhập thành công!")
else:
    print("Đăng nhập thất bại!")

# Đóng trình duyệt sau khi hoàn thành
driver.quit()
