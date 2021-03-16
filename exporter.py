import csv  # csv 기능 가져오기


def save_to_file(jobs):
    file = open("jobs.csv", mode="w")  # 파일 만들기
    writer = csv.writer(file)  # csv 파일에 쓸 것이다.
    writer.writerow(["title", "company", "location", "link"])

    for job in jobs:
        writer.writerow(list(job.values()))

    return
