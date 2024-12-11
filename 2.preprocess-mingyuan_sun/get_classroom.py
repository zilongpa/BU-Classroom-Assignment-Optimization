import requests
from bs4 import BeautifulSoup
import csv
import json

def scrape_classroom_links(base_url, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Link'])
        page = 1
        while True:
            url = base_url.format(page)
            response = requests.get(url)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            error_message = soup.find('p', class_='cts-error')
            if error_message:
                print(f"{page} error, stopping...")
                break
            results_list = soup.find('ul', class_='cts-results-list')
            if results_list:
                li_items = results_list.find_all('li')
                for li in li_items:
                    link_tag = li.find('a', class_='cts-button cts-button-primary')
                    if link_tag and link_tag.get('href'):
                        classroom_link = link_tag['href']
                        writer.writerow([classroom_link])
            print(f"{page}")
            page += 1

def scrape_classroom_data(input_csv, output_json):
    urls = []
    with open(input_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            urls.append(row[0])

    classroom_data = []
    for url in urls:
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        name_elem = soup.find('div', class_='content-panel')
        if not name_elem:
            continue
        name = name_elem.find('h1').get_text().strip() if name_elem.find('h1') else "Unknown"
        detail_container = soup.find('div', class_='cts-detail-container')
        details = detail_container.find_all('div', class_='cts-detail-details') if detail_container else []

        classroom_info = {
            "Name": name,
            "Details": {},
            "AdditionalInfo": {}
        }

        first_detail = details[0] if len(details) > 0 else None
        if first_detail:
            h4_elements = first_detail.find_all('h4')
            for h4 in h4_elements:
                h4_title = h4.get_text().strip()
                ul_list = h4.find_next('ul', class_='cts-detail-list')
                if ul_list:
                    li_items = ul_list.find_all('li')
                    li_texts = []
                    for li in li_items:
                        span = li.find('span')
                        if span:
                            li_text = li.get_text(strip=True).replace(span.get_text(strip=True), "").strip()
                        else:
                            li_text = li.get_text(strip=True)
                        li_texts.append(li_text)
                    classroom_info["Details"][h4_title] = li_texts

        second_detail = details[1] if len(details) > 1 else None
        if second_detail:
            li_items = second_detail.find_all('li')
            for li in li_items:
                meta_name_span = li.find('span', class_='meta-name')
                meta_value_span = li.find('span', class_='meta-value')
                if meta_name_span and meta_value_span:
                    meta_name = meta_name_span.get_text(strip=True)
                    meta_value = meta_value_span.get_text(strip=True)
                    classroom_info["AdditionalInfo"][meta_name] = meta_value

        classroom_data.append(classroom_info)
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(classroom_data, json_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    base_url = "https://www.bu.edu/classrooms/find-a-classroom/page/{}/?cts_address&cts_capacity_lfa&cts_capacity&cts_filter_submit=Search"
    output_csv = './classroom_links.csv'
    output_json = './classroom_data.json'
    scrape_classroom_links(base_url, output_csv)
    scrape_classroom_data(output_csv, output_json)
