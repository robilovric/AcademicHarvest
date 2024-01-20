import requests
from bs4 import BeautifulSoup

class Professor:
    name=''
    num_citations=0
    publications=[]
    co_authors=[]
    intensity=[]
    hasCoAuthors=True

    def __init__(self, name, num_citations=0, publications=[], co_authors=[], intensity=[]):
        self.name = name
        self.num_citations = num_citations
        self.publications = publications 
        self.co_authors = co_authors 
        self.intensity = intensity 

    def display_information(self):
        print(f"Professor: {self.name}")
        print(f"Number of Citations: {self.num_citations}")
        print("Publications:")
        for publication in self.publications:
            title = publication.get('bib', {}).get('title', 'N/A')
            year = publication.get('bib', {}).get('pub_year', 'N/A')
            print(f"- {title} ({year})")
        print("Co-authors:")
        for co_author in self.co_authors:
            coauthor_name = co_author.get('name', 'N/A')
            print(f"- {coauthor_name}")
        print("Intensity List:")
        for intensity_value in self.intensity:
            print(f"  - {intensity_value}")

professors=[] 

url = "https://nastava.fesb.unist.hr/nastava/nastavnici/detalji"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    professors_list = soup.find_all('li', class_='')
    professors_names = [] 

    for professor in professors_list:
        details_span = professor.find('span', class_='details')
        if details_span and 'vanjski suradnik' not in details_span.text.lower():
            name_span = professor.find('span', class_='name')
            if name_span:
                professor_name = name_span.text.strip()
                professors_names.append(professor_name)
                professorObj=Professor(professor_name) 
                professors.append(professorObj)

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")