import professorData
from scholarly import scholarly

conpromited_strings=[]

for prof in professorData.professors:
    try:
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

        prof.display_information()

        #Spremanje u file
        prof.WriteDataToFile()        

    except Exception as e:
        conpromited_strings.append(prof.name)
        print(f"An exception of type {type(e).__name__} occurred: {e}")

print(conpromited_strings)
