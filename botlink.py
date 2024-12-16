from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def safe_get_text(driver, by, value):
    """
    Hàm lấy văn bản của phần tử, nếu không tìm thấy thì trả về None.
    :param driver: đối tượng driver Selenium
    :param by: Phương thức tìm kiếm (By.CLASS_NAME, By.XPATH, etc.)
    :param value: Giá trị của phần tử (class, xpath, etc.)
    :return: Văn bản của phần tử hoặc None nếu không tìm thấy.
    """
    try:
        element = driver.find_element(by, value)
        return element.text.strip() if element else None
    except:
        return None

def login_to_indeed(driver, username, password):
    """
    Hàm đăng nhập vào Indeed.
    :param driver: đối tượng driver Selenium
    :param username: Tên đăng nhập
    :param password: Mật khẩu
    """
    # Mở trang đăng nhập của Indeed
    driver.get("https://secure.indeed.com/account/login")
    time.sleep(2)

    # Điền tên đăng nhập và mật khẩu (Cập nhật ID cho các trường nhập)
    driver.find_element(By.ID, "login-email").send_keys(username)  # Cập nhật selector email
    driver.find_element(By.NAME, "password").send_keys(password)  # Cập nhật selector mật khẩu

    # Nhấn nút đăng nhập
    driver.find_element(By.CLASS_NAME, "icl-Button").click()
    time.sleep(5)  # Chờ một lúc để đăng nhập hoàn tất

def scrape_job_details(job_url, username, password):
    """
    Hàm lấy thông tin chi tiết của một công việc từ URL Indeed.
    :param job_url: URL của công việc trên Indeed
    :param username: Tên đăng nhập Indeed
    :param password: Mật khẩu Indeed
    :return: Thông tin công việc (dictionary)
    """
    # Cấu hình Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Chạy ở chế độ không giao diện
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(r'D:\bot_get_jobs\chromedriver-win64\chromedriver.exe')  # Cập nhật đường dẫn driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Đăng nhập vào Indeed
        login_to_indeed(driver, username, password)

        # Truy cập vào URL công việc
        driver.get(job_url)
        time.sleep(10)  # Chờ trang tải

        # Lấy thông tin công việc
        title = safe_get_text(driver, By.CLASS_NAME, "jobsearch-JobInfoHeader-title")
        company = safe_get_text(driver, By.CLASS_NAME, "css-1ioi40n")
        location = safe_get_text(driver, By.CLASS_NAME, "css-waniwe")
        job_type = safe_get_text(driver, By.CLASS_NAME, "css-1msfjo7")

        job_details = {
            "title": title,
            "company": company,
            "location": location,
            "job_type": job_type,
            "url": job_url
        }
        return job_details

    except Exception as e:
        print(f"Error scraping job details: {e}")
        return None

    finally:
        driver.quit()

# Chương trình chính
if __name__ == "__main__":
    # Nhập thông tin tài khoản và mật khẩu Indeed
    username = input("Nhập tên đăng nhập Indeed: ").strip()
    password = input("Nhập mật khẩu Indeed: ").strip()

    # URL công việc trên Indeed
    job_url = input("Nhập URL công việc trên Indeed: ").strip()
    print("Đang lấy thông tin công việc...")

    job_info = scrape_job_details(job_url, username, password)

    if job_info:
        print("Thông tin công việc:")
        for key, value in job_info.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("Không thể lấy thông tin công việc.")
