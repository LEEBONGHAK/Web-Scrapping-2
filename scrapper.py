# 스텍오버플로우에서 데이터를 긁어오는 함수들
from bs4 import BeautifulSoup
import requests


# url에서 max_page 추출 함수
def get_last_pages(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_pages = pages[-2].get_text(strip=True)

    return int(last_pages)


# 제목, 회사이름, 위치, 지원링크 추출
def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find(
        "h3", {"class": "fc-black-700"}).find_all("span", recursive=False)

    company = company.get_text(strip=True)
    location = location.get_text(strip=True)

    links = html["data-jobid"]

    # dictionary로 반환
    return {"title": title, "company": company, "location": location, "link": f"https://stackoverflow.com/jobs/{links}"}


# indeed의 pages를 받아서 그만큼의 request 생성
def extract_jobs(last_page, URL):

    jobs = []

    for page in range(last_page):
        print(f"Scrapping SO page: {page}")
        result = requests.get(f"{URL}&pg={page+1}")  # 페이지 요청
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs(word):
    URL = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_pages(URL)
    jobs = extract_jobs(last_page, URL)

    return jobs
