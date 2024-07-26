import requests
from bs4 import BeautifulSoup
import csv


# **********************************************************************************

search = input("Search About Job: ").strip()

# to check if have any word in the search
if search != "":
    result_button = requests.get(f"https://wuzzuf.net/search/jobs/?q={search}")

    src_button = result_button.content

    soup_button = BeautifulSoup(src_button, "lxml")

    all_button_page = len(
        soup_button.find_all("li", {"class": "css-1q4vxyr", "tabindex": "0"})
    )

    if all_button_page == 0:
        all_button_page = 2

    # **********************************************************************************

    list_job_titles = []
    list_company_names = []
    list_location_name = []
    list_job_skills = []
    list_links = []
    list_salary = []

    for j in range(all_button_page):
        result = requests.get(f"https://wuzzuf.net/search/jobs/?q={search}&start={j}")
        src = result.content
        soup = BeautifulSoup(src, "lxml")

        #
        job_title = soup.find_all("h2", {"class": "css-m604qf"})

        company_names = soup.find_all("a", {"class": "css-17s97q8"})

        location_name = soup.find_all("span", {"class": "css-5wys0k"})

        job_skills = soup.find_all("div", {"class": "css-y4udm8"})

        for i in range(len(job_title)):
            list_job_titles.append(job_title[i].text)
            list_links.append(job_title[i].find("a").attrs["href"])
            list_company_names.append(company_names[i].text)
            list_location_name.append(location_name[i].text)
            links = job_skills[i].find_all("div")[1].text
            list_job_skills.append(links.strip())

    file_list = [
        list_job_titles,
        list_company_names,
        list_location_name,
        list_job_skills,
        list_links,
    ]

    # **********************************************************************************

    if True in list(map(lambda a: bool(a), file_list)):
        exported = zip(*file_list)

        with open("./jobs.csv", "w", newline="", encoding="utf-8") as myfile:
            wr = csv.writer(myfile)
            wr.writerow(
                ["job title", "company names", "location name", "skills", "links"]
            )

            wr.writerows(exported)
        print("successfully")
    else:  # noqa: E722
        print("change title word")
else:  # noqa: E722
    print("result is failed")
