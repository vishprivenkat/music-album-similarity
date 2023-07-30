from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
import sys


def get_id_tags(find_a_tags):
    '''
    Function to extract ID Tags
    '''  
    return find_a_tags['id']

def get_artist(find_a_tags):
    '''
    Function to extract artist names from <a></a> tags
    '''
    return  " ".join(re.findall("[a-zA-Z]+", find_a_tags.contents[0]))
    
def get_album(find_a_tags):
    '''
    Function to extract album names from the <i></i> tags within the <a> tags
    '''
    return find_a_tags.find("i").contents[0]

def get_description(find_p_tags):
    '''
    Function to get descriptions of the different albums
    '''
    find_p_tags = str(find_p_tags)
    return re.findall('\n(.*)—', find_p_tags)[0]

def extract_sales_figures(sales):
    '''
    Extract Sales Figures'''
    sales_figure = int(re.findall('[0-9]+', sales)[0])*1000000
    return sales_figure

def year_to_decade(year): 
    '''
    Function to convert years to decade 
    '''
    
    decade = year[2]+'0s'
    return decade 

def get_year(find_div):
    '''
    Extract Years from the div and convert it to decades
    '''
    years = re.findall('Year: [0-9]+', find_div)
    decades = [year_to_decade(year[6:]) for year in years]
    return decades

def get_sales(find_div):
    '''
    Extract Total Sales Figures from Div
    '''
    total_sales = re.findall(' Total sales: [0-9]+ | Total certified sales: [0-9]+', find_div)
    total_sales = [ int(re.sub("\D","", sales))*100000  for sales in total_sales ]
    return total_sales
    

def get_author(find_div):
    '''
    Extract Authors from the div
    '''
    authors = re.findall('—<i>[a-zA-Z.]+ [a-zA-Z.]+', find_div)
    authors = [ re.sub('—<i>','',author) for author in authors]
    
    return authors

def get_US_sales(find_div):
    '''
    Extract U.S Sales figures from Div
    '''
    total_us_sales = re.findall('U.S. sales: [0-9]+', find_div)
    total_us_sales = [ int(re.sub("\D", "", sales))*100000 for sales in total_us_sales ] 
    return total_us_sales

def get_data(soup):
    
    '''
    Attributes to Extract from Article, type of data: 
    1. id - string
    2. Artist - string 
    3. Album - string 
    4. Decade - string 
    5. sales_total - numbers
    6. sales_us - numbers
    7. description - string
    8. author - string
    '''
    #Extracting the div where the data we need is present
    find_div = soup.find("div", {"class":"copy entry manual-ads"})
    find_div_text = find_div.get_text()
    find_a_tags = find_div("a", {"class":"big jumplink"})
    find_a_tags = find_a_tags[1:]

    id_tags = [ get_id_tags(tags) for tags in find_a_tags ]
    artist_tags = [get_artist(tags) for tags in find_a_tags]
    album_tags = [get_album(tags) for tags in find_a_tags]
    decade = get_year(find_div_text)
    sales_total = get_sales(find_div_text)
    sales_us = get_US_sales(find_div_text)
    authors = get_author(str(find_div))
   
    #Extracting <p> tags for description, sales, decade information
    find_p_tags = find_div("p")
    find_p_tags = find_p_tags[4:]
    description = [get_description(str(p_tag)) for p_tag in find_p_tags]

    music_album_dictionary = {
        'id':id_tags,
        'artist':artist_tags,
        'album':album_tags,
        'decade':decade,
        'sales_total':sales_total, 
        'sales_us':sales_us, 
        'description':description,
        'author':authors
    }

    return music_album_dictionary

def convert_to_csv(music_album_dictionary, csv_file_name):
    print("Creating DataFrame.......")
    dataframe = pd.DataFrame.from_dict(music_album_dictionary)
    dataframe.to_csv(csv_file_name, index=False, header=True)
    print("Dataframe Created!")

if __name__ == "__main__":
    print("Reading and Extracting Data from the given URL.....")
    url = sys.argv[1]
    #"https://www.pastemagazine.com/music/best-selling-albums/the-best-selling-albums-of-all-time/#25-the-beatles-sgt-pepper-s-lonely-hearts-club-band"
    page = urlopen(url)
    html = page.read().decode("utf-8") 
    soup = BeautifulSoup(html, "html.parser")
    csv_file_name = sys.argv[2]
    data_dictionary = get_data(soup)
    convert_to_csv(data_dictionary, csv_file_name)
