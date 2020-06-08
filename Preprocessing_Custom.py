# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:12:02 2020

@author: abisht
"""
#libraries
#import libraries
import sys
sys.setrecursionlimit(10000)
import re
import pandas as pd
from tika import parser
import glob



# enable logging
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

#important to add words
stop_words.extend(['www','docprops_thumbnail_jpeg','gb','upon','ca','llc','copyright','right','com','appendix','html','docprops','thumbnail','jpeg','cr','image_png_image_png','insert_fss_acronym','reserved','na','image_png_image_png','llp','png','like'])
# stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
#-----------------------------------------------------------------------


# function to normalize data
def preprocess(text):
    
    text=text.lower()
    text=re.sub('(\\d|\\W^&)+',' ',text)
    text=re.sub('&lt;/?.*?&gt;',' &lt;&gt; ',text)
    text=re.sub('(©|\\||/|,|"|\\?|\\(|\\)|#|‹|›|\\$| – |…| & |;|:|%|“|”|\\+|~|\\*|>|<|•|❶|||❑|■|✓||●|™|[|]||²| —|--| — |http|https|=|·||)',' ',text)
    text=re.sub('\\.+','.',text)
    text=re.sub('\s+',' ',text)
    return text

#Extract data from input source
def data_extraction():
    flag=1
       
    if flag==1: #debug
        print("1.-------- Running Data Extraction along with normalization----------------- ")        
#        get all the files within the folder
        
        path=r'EXTRACTION FOLDER'   
        pptfiles = [f for f in glob.glob(path + "**/*.pptx", recursive=True)]
        docfiles = [f for f in glob.glob(path + "**/*.docx", recursive=True)]
        pdffiles = [f for f in glob.glob(path + "**/*.pdf", recursive=True)]        
        files=pptfiles+pdffiles+docfiles
        print("No of files: {}".format(len(files)))
        doclist=[] # create empty list and initialize with default values
        i=0   
        

        df=pd.read_excel(r'FILTER USING EXCEL')
        df=df.loc[df.Status.isin(['Downloaded','Fetched']),['Titles','Details']]
        titles=df.Titles.tolist()
        files=df.Details.tolist()  #assuming details we contain links
     
        for f in files:        
            i=i+1
            print('{} {}'.format(i,f))
            parsed = parser.from_file(f)
            #print(parsed["content"])
            doclist.append(preprocess(parsed["content"]))
        
        print("-------- Data Extraction Completed----------------- ")
        print("No of Documents scanned: {}".format(len(doclist)))
    
    return files,titles,doclist

#read the link validation excel
#filter only those records with Status=Fetched or Downloaded    
#iterated and get data from their details section






#  main function
if __name__ == "__main__":
    
#    1. Data collection phase -----------------------------
    
#    Setting up the parameters
    f=1   #1 for read data ,2 for write date to input stream
    filename='doclist.pkl'   
     
     
    if f==1:
        print('-------Read from stored binary------------------')
#        df = pd.read_pickle(filename)    
        df = pd.read_pickle(r'model\document.pkl')    
        data = df.Text.values.tolist()
        print(data)
    else:  
        files,titles,doclist= data_extraction()        
        list1=pd.Series(files, name='File')
        list2=pd.Series(doclist, name='Text')
        
        # Create data frame with file path and normalized text data
        df=pd.concat([list1,list2],axis=1)
        print('-------Save as binary file------------------')
        df.to_pickle(filename) 

#------------------------------------------------------------
        
#   2. Data Cleansing ----------------------------------------
    


    

