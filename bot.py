from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Hàm lấy thông tin jobs từ Indeed
def scrape_jobs(keyword, location, max_pages=1):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Chạy trình duyệt ở chế độ nền
    service = Service(r'D:\bot_get_jobs\chromedriver-win64\chromedriver.exe')  # Đảm bảo đường dẫn đúng
    driver = webdriver.Chrome(service=service, options=chrome_options)

    jobs = []  # Danh sách lưu kết quả
    base_url = "https://www.indeed.com/jobs"

    for page in range(0, max_pages * 10, 10):
        url = f"{base_url}?q={keyword}&l={location}&start={page}"
        driver.get(url)
        time.sleep(2)

        job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for card in job_cards:
            try:
                title = card.find_element(By.CLASS_NAME, "jobTitle").text
                company = card.find_element(By.CLASS_NAME, "companyName").text
                location = card.find_element(By.CLASS_NAME, "companyLocation").text
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                })
            except Exception as e:
                print(f"Error extracting job details: {e}")

    driver.quit()
    return jobs

# Hàm ghi dữ liệu vào Google Sheets
def write_to_google_sheet(data, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1
    sheet.clear()  # Xóa dữ liệu cũ

    headers = ["Title", "Company", "Location"]
    sheet.append_row(headers)

    for row in data:
        sheet.append_row([row['title'], row['company'], row['location']])

# Chương trình chính
if __name__ == "__main__":
    keyword = "Java Developer"  # Từ khóa tìm kiếm
    location = "Remote"  # Địa điểm
    max_pages = 2  # Số trang muốn lấy
    sheet_name = "Indeed Jobs"  # Tên Google Sheet

    print("Scraping jobs...")
    jobs = scrape_jobs(keyword, location, max_pages)

    if jobs:
        print(f"Found {len(jobs)} jobs. Writing to Google Sheets...")
        write_to_google_sheet(jobs, sheet_name)
        print("Done!")
    else:
        print("No jobs found!")
