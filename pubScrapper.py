import professorData
import re
import requests 
from scholarly import scholarly, ProxyGenerator  
# Proxies api-endpoint 

pg = ProxyGenerator()

success = pg.ScraperAPI("3e12031c1432e05dc0a87eb2c8f6bc87")

scholarly.use_proxy(pg)



        
def get_coauthors_for_publication(title):
    
    try:
        #search_query = scholarly.search_pubs(title, filled=True)
        # first_publication_result = next(search_query)
        # publication = scholarly.fill(first_publication_result)
        
        publication = scholarly.search_single_pub(title, filled=True)

        
        #title = publication.get('bib', {}).get('title', 'N/A')
        #year = publication.get('bib', {}).get('pub_year', 'N/A')
        
        #print(f"Publication Title: {title}")
        #print(f"Publication Year: {year}")
        

        coauthors = publication.get('bib', {}).get('author', [])
        
        print(type(coauthors))
        coautorString = ''.join(coauthors)

        print("RAW DATA FORMAT\n", coautorString)
        
        print("EXTRACTED AUTHORS")
        formatCoautorList(coautorString)

            
    except StopIteration:
        print(f"No results found for the publication '{title}'.")

def formatCoautorList(author_string):
    # Hypothetical character list
    #author_string = "Papi{\\'c}, Vladan and Rogulj, Nenad and Ple{\\v{s}}tina, Vladimir"    

    author_string = author_string.replace("{\\'c}", "ć").replace("{\\v{s}}" or "{\v{s}}" , "š").replace("{\v{c}}", "č").replace("{\v{z}}", "ž")

    author_list = re.findall(r'(\w+),\s*(\w+)', author_string)

    formatted_author_list = [' '.join(author) for author in author_list]
    professorData.professors[97].co_authors.append(formatted_author_list)

    print(formatted_author_list)


try:
    prof = professorData.professors[97]
    search_query = scholarly.search_author(prof.name)
    first_author_result = next(search_query)
    author = scholarly.fill(first_author_result)
    
    prof.num_citations=author.get("citedby")
    coauthors = author.get('coauthors', [])
    if coauthors:
        prof.co_authors=coauthors
    else:
        print("No co-authors found.")
        prof.hasCoAuthors=False
    
    publications = author.get('publications', [])
    if publications:
        prof.publications=publications
    else:
        print("No publications found.")
    for pub in professorData.professors[97].publications:
        title = pub.get('bib', {}).get('title', 'N/A')
        print(title)
        get_coauthors_for_publication(title)
    
    professorData.professors[97].display_information()

except Exception as e:
    print(type(e).__name__)
