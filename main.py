import requests
from bs4 import BeautifulSoup
import os


def download_html(url):
    response = requests.get(url)
    html_content = response.text
    return html_content

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = ''
    for element in soup.descendants:
        if element.name in ('p', 'a', 'code', 'pre'):
            text += element.get_text()
            text += '\n'
        elif element.name == 'img' and element.has_attr('alt') and element['alt']:
            text += element['alt']
            text += '\n'
        elif element.name == 'a' and element.has_attr('href'):
            text += element.get_text()
            text += ': '
            text += element['href']
            text += '\n'
    return text

def save_to_file(text, url, output_dir):
    page_name = url.split('/')[-1]
    filename = os.path.join(output_dir, url + ' # ' + page_name + '.txt')
    filename = filename.replace('/', '_')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(text)

def delete_url(url, input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    with open(input_file, 'w') as f:
        for line in lines:
            if line.strip() != url:
                f.write(line)
    return f'{url} deleted from {input_file}'


input_file = 'urls.txt'
output_dir = '/path/to/text'
with open(input_file, 'r') as f:
    urls = f.readlines()

num_copied = 0
for url in urls:
    url = url.strip()
    html_content = download_html(url)
    text = extract_text(html_content)
    save_to_file(text, url, output_dir)
    num_copied += 1
    print(f'{url} has been copied')
    delete_url(url, input_file)
print(f'total copied {num_copied} pages')