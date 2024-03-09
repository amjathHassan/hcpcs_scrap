import requests
from bs4 import BeautifulSoup
import csv


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

base_url = "https://www.hcpcsdata.com"
check_flag = False


def get_soup(url):
    """
    Create and return soup object of url passed
    :param url: List of url passed to web scrap
    :return:soup object of the given url
    """
    res = requests.get(url, headers=headers)
    return BeautifulSoup(res.text, 'lxml')


def extract_group(element):
    """
    Fuction iis used to get the code name
    :param element: soup object of code name with count
    :return: code name
    """
    return element.text.split('(')[0].strip() if element else ''


def extract_short_description(tr):
    """
    Short description of each code is obtained
    :param tr: the description table row object of each code detailed page.
    :return: short description
    """
    if tr:
        tds = tr.find_all('td')
        return tds[1].get_text(strip=True) if len(tds) >= 2 else ''
    return ''


def scrape_code_details(url):
    """
    Main function to call for scrapping
    :param url: url to scrap
    :return: data to be written in csv,
    """
    soup = get_soup(url)
    group = extract_group(soup.select_one("h1"))
    category = soup.select_one("h5").text.strip()
    codelinks = [base_url + a['href'] for a in soup.select('tbody tr.clickable-row a')]
    data = []
    for codelink in codelinks:
        soup_list_detailed = get_soup(codelink)
        code = soup_list_detailed.select_one(".identifier16").text
        long_description = soup_list_detailed.select_one("h5").text
        short_description = extract_short_description(soup_list_detailed.select_one("#codeDetail tbody tr"))
        data.append([group, category, code, long_description, short_description])
        if check_flag:
            """
                Make check Flag True to create csv file with header and one row of data
            """
            break
    return data


soup = get_soup("https://www.hcpcsdata.com/Codes")
links = [base_url + a['href'] for a in soup.select('tbody tr.clickable-row a')]

with open('hcpcs_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Group', 'Category', 'Code', 'Long Description', 'Short Description'])
    for link in links:
        data = scrape_code_details(link)
        for row in data:
            writer.writerow(row)
        if check_flag:
            """
                For checking, Make check Flag True to create csv file with header and one row of data
            """
            break




