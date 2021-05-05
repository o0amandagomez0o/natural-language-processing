import unicodedata
import re
import json

import warnings
warnings.filterwarnings("ignore")

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire


def basic_clean(sentence):
    """
    This function takes in a string and
    - lowercases it
    - normalizes unicode characters to ASCII
    - replaces anything that is NOT a:
        - letter: a-z
        - number: 0-9
        - sgl quote: '
        - whitespace: \s
    returns cleaned string
    """
    #lowercases
    clean = sentence.lower()
    #normalize unicode
    clean = unicodedata.normalize('NFKD', clean).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    #uses regex to substitute anything non-alphanumeric, single quote or whitespace
    clean = re.sub(r"[^a-z0-9'\s]", '', clean)
    
    return clean





def tokenize(sentence):
    """
    This function takes in a string
    - tokenizes the entire string
    returns tokenized string
    """
    
    # Create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # Use the tokenizer
    return tokenizer.tokenize(sentence, return_str = True)





def stem(sentence):
    """
    This function takes in a string
    - strips each word to it's stem
    returns stripped string
    """
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer() 
    
    # Apply the stemmer to each word in our string.
    stems = [ps.stem(word) for word in sentence.split()]
    
    # Join our lists of words into a string again
    sentence_stemmed = ' '.join(stems)
    
    return sentence_stemmed





def lemmatize(sentence, nltkdl=True):
    """
    This function takes in a string
    - strips each word to it's lexicographically correct stem word 
    returns stripped string
    .
    .
    .
    # Download if not done so already.
    nltk.download('wordnet')
    """
    if nltkdl==False:
        nltk.download('wordnet')
    
    # Create the Lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Apply the lemmatizer on each word in the string.
    lemmas = [wnl.lemmatize(word) for word in sentence.split()]
    
    # Join our list of words into a string again; assign to a variable to save changes.
    sentence_lemmatized = ' '.join(lemmas)
    
    return sentence_lemmatized





def remove_stopwords(sentence, extra_words=None, exclude_words=None):
    """
    Takes in a string, and optional list of:
    - extra_words: words to include
    - exclude_words: words to exclude
    returns a string filtered for stopwords and optional exclusions.
    .
    .
    .
    .
    If recieving error: `Resource stopwords not found. Please use the NLTK Downloader to obtain the resource.`
    In Terminal type:
    python -c "import nltk; nltk.download('stopwords')"
    """
    
    # standard English language stopwords list from nltk
    stopword_list = stopwords.words('english')
        
    # Add to stopword list 
    stopword_list = stopwords.words('english') + extra_words
    
    # Remove from stopword list
    stopword_list = [word for word in stopword_list if word not in exclude_words]
    
    # Split words in lemmatized string.
    words = lemmatize(sentence).split()
    
    # Create a list of words from string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in the list back into strings; assign to a variable to keep changes.
    article_without_stopwords = ' '.join(filtered_words)
    
    return article_without_stopwords
    





def remove_columns(df, cols_to_remove):  
    """
    This function removes columns listed in arguement
    - cols_to_remove = ["col1", "col2", "col3", ...]
    returns DF w/o the columns.
    """
    df = df.drop(columns=cols_to_remove)
    return df





def full_df(df, columns):
    """
    This function will
    - drop unncessary cols
    - rename content col
    apply functions:
    - basic_clean
    - Tokenize
    - stem
    - lemmatize
    to create new columns
    returns appended columns as one pandas df
    """
    
    df = remove_columns(df, cols_to_remove=columns)
    
    df = df.rename(columns={"content": "original"})
    
    df['clean'] = df.original.apply(basic_clean).apply(tokenize)
    
    df['stemmed'] = df.clean.apply(stem)
    df['lemmatized'] = df.clean.apply(lemmatize)
    
    return df

