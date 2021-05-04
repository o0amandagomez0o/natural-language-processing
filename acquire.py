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
    soup = bs4.BeautifulSoup(response.text, features="lxml")
    
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
    sites = ["https://codeup.com/codeups-data-science-career-accelerator-is-here/", 
         "https://codeup.com/data-science-myths/", 
         "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/", 
         "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/", 
         "https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/"]
    
    all_blog_posts = loop_blog_articles(sites)
    df = pd.DataFrame(all_blog_posts)
    return df





def get_article(article, category):
    """
    This function takes in an article and category
    -IDs it's Title
    - Body of content
    creates an empty dictionary to house this information
    returns the dictionary
    """
    
    title = article.select("[itemprop='headline']")[0].text
    
    content = article.select("[itemprop='articleBody']")[0].text
    
    output = {}
    output["title"] = title
    output["content"] = content
    output["category"] = category
    
    return output





def get_articles(category):
    """
    This function takes in a str (must be available category in website)
    returns a list of dictionaries that represents a sgl inshorts article
    """
    
    base = "https://inshorts.com/en/read/"
    url = base + category
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, features="lxml")
    
    articles = soup.select('.news-card')
    
    output = []
    for article in articles:
        output.append(get_article(article, category))
        
    return output
        
    
    
    
    
    
def get_all_news_articles(categories):
    """
    This function takes in a list of categories
    - creates an empty list
    - loops through the arguements categories
        - applies get_articles to ea category to create a list of dictionaries
            containing title, content, category
        - appends all lists created for each category
    - converts to pandas DF
    returns df.    
    """
    
    all_inshorts = []
    
    for category in categories:
        all_category_articles = get_articles(category)
        all_inshorts = all_inshorts + all_category_articles
        
    df = pd.DataFrame(all_inshorts)
    
    return df
