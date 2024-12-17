import gspread
from google.auth import default
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import gspread
from google.oauth2.service_account import Credentials

# Thông tin tài khoản Google
GOOGLE_EMAIL = "doanhieunghia560@gmail.com"  # Thay bằng email của bạn
GOOGLE_PASSWORD = "kannahashimoto"     # Thay bằng mật khẩu của bạn

# Hàm đăng nhập vào Google
def login_with_google(driver):
    try:
        # Mở trang đăng nhập Google
        driver.get("https://accounts.google.com/ServiceLogin")
        
        # Nhập email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_field.send_keys(GOOGLE_EMAIL)
        email_field.send_keys(Keys.RETURN)

        # Nhập mật khẩu
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(GOOGLE_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        
        # Chờ xác thực
        WebDriverWait(driver, 10).until(
            EC.url_contains("myaccount.google.com")
        )
        print("Đăng nhập Google thành công!")
    except TimeoutException as e:
        print(f"Timeout khi đăng nhập Google: {e}")
    except NoSuchElementException as e:
        print(f"Không tìm thấy phần tử khi đăng nhập Google: {e}")
    except Exception as e:
        print(f"Có lỗi khi đăng nhập Google: {e}")

# Hàm lấy thông tin công việc
def get_job_details(driver, job_link):
    try:
        # Mở trang công việc
        driver.get(job_link)

        # Đợi tiêu đề công việc tải
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-JobInfoHeader-title"))
        )

        # Lấy thông tin công việc
        def safe_get_text(by, value):
            try:
                return driver.find_element(by, value).text
            except NoSuchElementException:
                return None

        job_title = safe_get_text(By.CLASS_NAME, "jobsearch-JobInfoHeader-title")
        company_name = safe_get_text(By.CLASS_NAME, "css-1ioi40n")
        job_location = safe_get_text(By.CLASS_NAME, "css-waniwe")
        job_description = safe_get_text(By.ID, "jobDescriptionText")

        # Hiển thị thông tin công việc
        print("\nThông tin công việc:")
        print(f"Tiêu đề: {job_title}")
        print(f"Công ty: {company_name}")
        print(f"Địa điểm: {job_location}")
        print(f"Mô tả công việc:\n{job_description}")

        return {
            "Tiêu đề": job_title,
            "Công ty": company_name,
            "Địa điểm": job_location,
            "Mô tả công việc": job_description
        }

    except TimeoutException as e:
        print(f"Timeout khi lấy thông tin công việc: {e}")
    except Exception as e:
        print(f"Có lỗi xảy ra khi lấy thông tin công việc: {e}")
        return None

# Hàm ghi thông tin công việc vào Google Sheets
def write_to_google_sheet(job_info):
    try:
        # Cung cấp đường dẫn đến tệp credentials
        creds = Credentials.from_service_account_file(
            'D:/bot_get_jobs/modern-girder-444305-d6-81cd187f8089.json',  # Đảm bảo sửa đường dẫn chính xác
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        # Tạo kết nối với Google Sheets
        client = gspread.authorize(creds)

        # Mở trang tính (Google Sheets) theo tên
        sheet = client.open("ds_job").sheet1  # Đảm bảo tên sheet chính xác

        # Ghi dữ liệu vào Google Sheet
        row_data = [
            job_info["Tiêu đề"], 
            job_info["Công ty"], 
            job_info["Địa điểm"], 
            job_info["Mô tả công việc"]
        ]
        
        # Đảm bảo rằng job_info được chuyển thành dạng danh sách
        sheet.append_row(row_data)  # Ghi vào dòng mới của Google Sheets
        print("Thông tin công việc đã được ghi vào Google Sheets!")
    except Exception as e:
        print(f"Có lỗi khi ghi vào Google Sheets: {e}")

# Cấu hình Selenium
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")

# Khởi tạo trình duyệt
driver = webdriver.Chrome(options=options)

try:
    # Mở trang Indeed
    driver.get("https://www.indeed.com/")
    
    # Đăng nhập Google
    login_with_google(driver)

    # Link công việc
    job_link = "https://vn.indeed.com/jobs?q=developer&l=vietnam&from=searchOnHP%2Cwhatautocomplete&vjk=1f403c018451b836"
    job_info = get_job_details(driver, job_link)

    if job_info:
        write_to_google_sheet(job_info)

finally:
    # Đóng trình duyệt
    driver.quit()
