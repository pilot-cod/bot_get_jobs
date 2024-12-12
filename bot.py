import requests
from bs4 import BeautifulSoup
import json

# Hàm lấy danh sách công việc từ Indeed
def fetch_jobs(keyword, location, num_jobs=10):
    base_url = "https://www.indeed.com/jobs"
    params = {
        "q": keyword,
        "l": location,
        "start": 0
    }
    jobs = []
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.indeed.com/",
    "Upgrade-Insecure-Requests": "1"
    }

    cookies = {
    "CTK": "1iegsinjfh9eh800",  # Thay "cookie_name" và "cookie_value" bằng giá trị thực
    }

    while len(jobs) < num_jobs:
        session = requests.Session()
        session.headers.update(headers)

        # Thực hiện yêu cầu với session
        response = session.get(base_url, params=params, headers=headers, cookies=cookies)
        print(f"URL: {response.url}")
        print(f"Status Code: {response.status_code}")

        if response.status_code != 200:
            print("Request bị lỗi. Không thể tiếp tục.")
            break
        else:
            print("Request thành công.")

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="job_seen_beacon")

        for card in job_cards:
            title = card.find("h2", class_="jobTitle").get_text(strip=True)
            company = card.find("span", class_="companyName").get_text(strip=True)
            link = card.find("a", href=True)["href"]
            job_url = "https://www.indeed.com/" + link

            jobs.append({
                "title": title,
                "company": company,
                "link": job_url
            })

            if len(jobs) >= num_jobs:
                break
        
        # Tăng trang
        params["start"] += 10

    return jobs

# Hàm gửi dữ liệu đến Google Apps Script
def send_to_google_sheets(data, script_url):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(script_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Dữ liệu đã được ghi vào Google Sheets thành công!")
    else:
        print(f"Lỗi khi gửi dữ liệu: {response.text}")

if __name__ == "__main__":
    # Thông tin tìm kiếm
    keyword = " IT"
    location = "Vietnam"
    num_jobs = 10

    # URL của Google Apps Script (thay YOUR_WEB_APP_URL bằng URL thật)
    script_url = "https://script.google.com/macros/s/AKfycbwGZUZ0j_TWo-1aXsvcV8GUQyuAcnNeF9CncOPyOItjRvI_jgZr3vpWTolDKJtvGPnflg/exec"

    # Lấy danh sách công việc
    jobs = fetch_jobs(keyword, location, num_jobs)

    # Gửi dữ liệu đến Google Sheets
    send_to_google_sheets(jobs, script_url)