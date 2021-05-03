import requests
import bs4
import pandas as pd

def get_blog_articles(site):
    """
    This function takes in a Codeup websiteand scrapes
    - Article title
    - date posted
    - category
    - article content
    returns as a dictionary
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = site
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text)
    
    articles_container = soup.select('#jupiterx-primary')[0]
    article = articles_container.select('.jupiterx-post')
    article = article[0]
             
    title = article.find('h1').text
    time = article.find(class_='jupiterx-post-meta-date').text
    category = article.find(class_='jupiterx-post-meta-categories').text
    body = article.find(class_='jupiterx-post-content').text
    return {
        
        'title': title,
        "date posted": time,
        "category": category,
        "content": body

    }





def loop_blog_articles(sites): 
    """
    This function takes in a list of codeup sites
    Creates an empty list
    appends dictionary created by `get_blog_articles` consisting of:
    - Article title
    - date posted
    - category
    - article content
    Loops through list of sites 
    returns list of appended dictionaries.
    """
    
    sites = ["https://codeup.com/codeups-data-science-career-accelerator-is-here/", 
         "https://codeup.com/data-science-myths/", 
         "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/", 
         "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/", 
         "https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/"]
    list_of_dicts = []
    
    for site in sites:
        blog_dictionary = get_blog_articles(site)
        list_of_dicts.append(blog_dictionary)
        
    return list_of_dicts





def convert_to_df():
    """
    This function takes list of dictionaries created by `loop_blog_articles`
    returns converted list to df
    """
    all_blog_posts = loop_blog_articles(sites)
    df = pd.DataFrame(all_blog_posts)
    return df