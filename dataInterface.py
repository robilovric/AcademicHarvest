import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_professors_data(directory):
    professors_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                professors_data.append({
                    "name": data["name"],
                    "num_citations": data["num_citations"],
                    "num_pubs": len(data["publications"])
                })
    return professors_data

def find_professor_with_most_citations(professors_data):
    if not professors_data:
        return None
    
    max_citations=0
    prof_indx=0
    for prof_num in range(len(professors_data)):
        num_citations=professors_data[prof_num]["num_citations"]
        if num_citations is not None:
            if(num_citations > max_citations):
                max_citations=num_citations   
                prof_indx=prof_num
        else:
            professors_data[prof_num]["num_citations"]=0
    return professors_data[prof_indx]

def plot_histograms_for_groups(professors_data):
    sorted_data = sorted(professors_data, key=lambda x: x["num_citations"])
    
    group_size = len(sorted_data) // 5
    groups = [sorted_data[i:i+group_size] for i in range(0, len(sorted_data), group_size)]

    for i, group in enumerate(groups):
        citations = [professor["num_citations"] for professor in group]
        names = [professor["name"] for professor in group]
        
        plt.figure(figsize=(10, 6))
        plt.bar(names, citations)
        plt.xlabel("Professor Name")
        plt.ylabel("Number of Citations")
        plt.title(f"Group {i+1} - Number of Citations Histogram")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

def create_heatmap(professors_data):
    sorted_data = sorted(professors_data, key=lambda x: x["num_citations"])
    
    group_size = len(sorted_data) // 5
    groups = [sorted_data[i:i+group_size] for i in range(0, len(sorted_data), group_size)]
    
    for i, group in enumerate(groups):
        num_pubs = [professor["num_pubs"] for professor in group]
        num_citations = [professor["num_citations"] for professor in group]
        names = [professor["name"] for professor in group]
        
        plt.figure(figsize=(10, 6))
        plt.hexbin(num_pubs, num_citations, gridsize=20, cmap='viridis')
        plt.colorbar(label='count in bin')
        plt.xlabel('Number of Publications')
        plt.ylabel('Number of Citations')
        plt.title(f'Group {i+1} - Heatmap of Number of Publications vs Number of Citations')
        plt.tight_layout()
        plt.show()

def create_violin(professors_data):
    professors_df = pd.DataFrame(professors_data)

    plt.figure(figsize=(10, 6))
    sns.violinplot(data=professors_df, x='num_pubs', y='num_citations', scale='width', cut=0)
    plt.xscale('log') 
    plt.yscale('log')  
    plt.xlabel('Number of Publications')
    plt.ylabel('Number of Citations')
    plt.title('Violin Plot of Number of Publications vs Number of Citations')

    plt.tick_params(axis='x', labelsize=8)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:g}'.format(x)))
    plt.tick_params(axis='y', labelsize=8)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:g}'.format(y)))
    plt.show()

def plot_collaborator_bar_plot():
    df = pd.read_csv("relationIntensity/associatesFESB.csv")
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Collaborator', y='Count', palette='viridis')
    plt.xlabel('Collaborator')
    plt.ylabel('Number of academic research collobartions')
    plt.title("Bar Plot of Toni Perković's colleagues")
    plt.xticks(rotation=90) 
    plt.tight_layout()  
    plt.show()

def plot_collaboratorInternational_bar_plot():
    df = pd.read_csv("relationIntensity/associatesInternational.csv")
    
    plt.figure(figsize=(20, 8))
    sns.barplot(data=df, x='Collaborator', y='Count', palette='viridis')
    plt.xlabel('Collaborator')
    plt.ylabel('Number of foreign academic research collobartions')
    plt.title("Bar Plot of Toni Perković's collaborators outside of FESB")
    plt.xticks(rotation=90) 
    plt.tight_layout()  
    plt.show()

def most_cited_professor():
    most_cited_prof= find_professor_with_most_citations(professors_data)
    print(f"The professor with the most citations is {most_cited_prof['name']} with {most_cited_prof['num_citations']} citations.")

def plot_citations():
    find_professor_with_most_citations(professors_data)
    plot_histograms_for_groups(professors_data)

def plot_citations_vs_pubs():
    find_professor_with_most_citations(professors_data)
    create_heatmap(professors_data)

def plot_violin():
    find_professor_with_most_citations(professors_data)
    create_violin(professors_data)

directory = "professorsDataLake"
professors_data = load_professors_data(directory)