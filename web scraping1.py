# import request to get URL


import requests
from bs4 import BeautifulSoup

#  Write a function to Get and parse html content from a Wikipedia page

def get_and_parse(url):
    webpage = requests.get(url)
    parsed_webpage = BeautifulSoup(webpage.content, "html Parser")
    return parsed_webpage

# Write a function to Extract article title
def extract_article_title(parsed_webpage):
     article_title = parsed_webpage.find('h1', {'class': 'firstHeading'}).txt
     return article_title


#  Write a function to Extract article text for each paragraph with their respective

# headings. Map those headings to their respective paragraphs in the dictionary

def extract_heading_and_text(parsed_webpage):
    content = {}
    current_header = None
    corresonding_paragraph = []

    header_and_paragraphs = parsed_webpage.find_all(["h2", "p"])

    for element in header_and_paragraphs:
        if element.name =="h2":
            if current_header is not None and len(corresonding_paragraph)

## Write a function to collect every link that redirects to another Wikipedia page

def extract_wikipedia_links(soup):
    links = set()
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/') and ':' not in href:
            full_url = 'https://en.wikipedia.org' + href
            links.add(full_url)
    
    return links

##  Wrap all the previous functions into a single function that takes as parameters a Wikipedia link

def get_wikipedia_article_info(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        return None 

    soup = BeautifulSoup(response.content, 'html.parser')

    title_tag = soup.find('h1', {'id': 'firstHeading'})
    title = title_tag.text if title_tag else None
    
    content_dict = {}
    headings = soup.find_all(['h2', 'h3', 'h4']) 
    paragraphs = soup.find_all('p')
    
    heading_index = 0
    paragraph_index = 0
    
    while paragraph_index < len(paragraphs):
        if heading_index < len(headings) and headings[heading_index]:
            heading_text = headings[heading_index].text.strip()
            paragraph_text = paragraphs[paragraph_index].text.strip()
            
            if heading_text not in content_dict:
                content_dict[heading_text] = []
            content_dict[heading_text].append(paragraph_text)
            
            heading_index += 1
        else:
           
            paragraph_text = paragraphs[paragraph_index].text.strip()
            if 'Introduction' not in content_dict:
                content_dict['Introduction'] = []
            content_dict['Introduction'].append(paragraph_text)
        
        paragraph_index += 1
    
    wikipedia_links = extract_wikipedia_links(soup)
    
    return {
        'title': title,
        'paragraphs_with_headings': content_dict,
        'wikipedia_links': list(wikipedia_links)
    }



## Test the last function on a Wikipedia page of your choice

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

result = get_wikipedia_article_info(url)

if result:
    print(f"Title: {result['title']}")
    print("\nParagraphs and Headings:")
    for heading, paragraphs in result['paragraphs_with_headings'].items():
        print(f"\nHeading: {heading}")
        for paragraph in paragraphs:
            print(paragraph)
    
    print("\nWikipedia Links:")
    for link in result['wikipedia_links']:
        print(link)
else:
    print("Error fetching the Wikipedia page.")


