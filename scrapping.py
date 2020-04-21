"""
    Reads a CVS file exported from PoP (Publish or Perish) and writes a CSV file with information
    gathered from articles.
    Data gathered is doi, title, authors, abstract and keywords.
"""
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json


def scrap_ieee_data(doi):
    """
        Gets a IEEE doi URL and returns a dict
    """
    paper_soup_page = BeautifulSoup(requests.get(doi).text, 'html.parser')
    paper_scripts = paper_soup_page.findAll('script', type='text/javascript')
    
    for paper_script in paper_scripts:
        
        paper_script_text = paper_script.text
        
        start_marker = 'global.document.metadata='
        end_marker = ';'
        
        if start_marker in paper_script_text:
            
            start = paper_script_text.find(start_marker)+len(start_marker)
            end = paper_script_text.rfind(end_marker)
            paper_json_text = paper_script_text[start:end]
            
            return json.loads(paper_json_text)
        
    return {}
    
    
def extract_from_ieee(doi):
    """
        Gets a DOI of a IEEE paper and adds extracted data into extracted dataframe
    """    
    paper_data = scrap_ieee_data(doi)
    
    if paper_data:

        title = ''
        abstract = ''
        authors = ''
        keywords = ''

        title = paper_data['formulaStrippedArticleTitle']

        if paper_data['sections']['abstract'] == 'true':
            abstract = paper_data['abstract']

        if paper_data['sections']['authors'] == 'true':
            authors = ', '.join([a['name'] for a in paper_data['authors']])

        if  paper_data['sections']['keywords'] == 'true':
            auth_kwds = list(filter(lambda k:'Author Keywords' in k['type'], paper_data['keywords']))
            if len(auth_kwds) == 1: keywords = ', '.join(auth_kwds[0]['kwd'])

        return {
            'doi': doi, 
            'title': title, 
            'authors': authors, 
            'abstract': abstract, 
            'keywords': keywords
        }                
    
    
    return {}

"""
    Goint to process CSV files
"""

if len(sys.argv) < 2:
    print('Error: You must pass the input csv PoP file name.')
    sys.exit();

input_filename = sys.argv[1]
output_filename = 'Output_' + input_filename

if len(sys.argv) == 3:
        output_filename = sys.argv[2]

print('Reading', input_filename)

input_data = pd.read_csv(input_filename)

print('Readed ', len(input_data.index), 'rows')
print('Going to scrap')


output_data = []

for paper in input_data.T.to_dict().values():
    publisher = paper['Publisher']
    article_url = paper['ArticleURL']
    
    print('Scrapping data from', article_url, 'of', publisher)
    
    if publisher == 'IEEE':
        paper_data = extract_from_ieee(article_url)
        if paper_data: 
            output_data.append(paper_data)
           
pd.DataFrame(output_data).to_csv(output_filename)

print('Finished.')