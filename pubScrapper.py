import professorData
from scholarly import scholarly, ProxyGenerator
from fp.fp import FreeProxy

def set_new_proxy():
    while True:
        proxy = FreeProxy(rand=True, timeout=1).get()
        proxy_works = scholarly.use_proxy(http=proxy, https=proxy)
        if proxy_works:
            break
    print(proxy)
    return proxy    

set_new_proxy()

# pg = ProxyGenerator()
# success = pg.FreeProxies()
# scholarly.use_proxy(pg)

search_query = scholarly.search_author(professorData.professors[97].name)

first_author_result = next(search_query)
author = scholarly.fill(first_author_result)

coauthors = author.get('coauthors', [])
if coauthors:
    professorData.professors[97].co_authors=coauthors
    for coauthor in coauthors:
        coauthor_name = coauthor.get('name', 'N/A')
else:
    print("No co-authors found.")
    
pub = author.get('publication', [])
publications = author.get('publications', [])

professorData.professors[97].num_citations=author.get("citedby")

if publications:
    professorData.professors[97].publications=publications
    for publication in publications:
        title = publication.get('bib', {}).get('title', 'N/A')
        year = publication.get('bib', {}).get('pub_year', 'N/A')
        coAuthors=publication.get('bib', {}).get('author', [])
else:
    print("No publications found.")
        
def get_coauthors_for_publication(title):
    search_query = scholarly.search_pubs(title)
    
    try:
        first_publication_result = next(search_query)
        publication = scholarly.fill(first_publication_result)
        
        title = publication.get('bib', {}).get('title', 'N/A')
        year = publication.get('bib', {}).get('pub_year', 'N/A')

        coauthors = publication.get('bib', {}).get('author', [])
        
        print(f"Publication Title: {title}")
        print(f"Publication Year: {year}")
        
        if coauthors:
            print("Co-authors:")
            for coauthor in coauthors:
                print(f"- {coauthor}") # Discuss
        else:
            print("No co-authors found.")
            
    except StopIteration:
        print(f"No results found for the publication '{title}'.")

while True:
    try:
        get_coauthors_for_publication('Chromablur: Rendering chromatic eye aberration improves accommodation and realism')
        break
    except Exception as e:
        set_new_proxy() 
