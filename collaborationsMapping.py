import professorData
import re
import csv
from scholarly import scholarly, ProxyGenerator  

pg = ProxyGenerator()
success = pg.ScraperAPI("c06ba0ead8c6972001e73b3807e139f0")
scholarly.use_proxy(pg)

#Extract publications title from PerkovicToni.json
prof=professorData.Professor.ReadDataFromFile("professorsDataLake/PerkovićToni.json")
#prof.display_information()

collaboratorsImage=dict()


def write_collaboratorsImage_to_csv():
    with open('CollaboratorsImage.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)
    
        # Write header
        csvwriter.writerow(['Collaborator', 'Count'])
    
        # Write data rows
        for collaborator, count in collaboratorsImage.items():
            csvwriter.writerow([collaborator, count])

def save_backup(data):
    with open('backup.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)
    
        # Write header
        csvwriter.writerow(['Title'])
    
        # Write data rows
        csvwriter.writerow([data])

def get_couauthors_from_publications(title):

    try:
        publication=scholarly.search_single_pub(title, filled=True)

        coauthors = publication.get('bib', {}).get('author', [])
        coautorString = ''.join(coauthors)

        print("RAW DATA FORMAT\n", coautorString)
        print("EXTRACTED AUTHORS")
        format_coauthors_adjust_intensity(coautorString)

    except StopIteration:
        print(f"No results found for the publication '{title}'.")

def format_coauthors_adjust_intensity(coauthor_raw):
  
    replacements = {
    r'{\\\'c}': 'ć',
    r'{\\v{S}}': 'Š',
    r'{\\v{C}}': 'Č',
    r'{\\v{s}}': 'š',
    r'{\\v{z}}': 'ž',
    r'{\\\'C}': 'Ć'
    }

    for pattern, replacement in replacements.items():
        coauthor_raw = re.sub(pattern, replacement, coauthor_raw)

    matches = re.findall(r'(\w+),\s*(\w+)', coauthor_raw)
    formatted_author_list = [' '.join(author) for author in matches]
    print(formatted_author_list)

    for author in formatted_author_list:
        print(author)
        if author not in collaboratorsImage:
            collaboratorsImage[author] = 0
        collaboratorsImage[author] += 1
        for key, value in collaboratorsImage.items():
            print(key, value)

# Test printing
for name, count in collaboratorsImage.items():
    print(name, count)

try:
    for pub in prof.publications:
        title = pub.get('bib', {}).get('title', 'N/A')
        save_backup(title)
        get_couauthors_from_publications(title)
    
    # Save to csv file
    write_collaboratorsImage_to_csv()
except Exception as e:
    print(type(e).__name__)