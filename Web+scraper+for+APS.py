
# coding: utf-8

# In[10]:

#import block
import urllib.request
import time
from bs4 import BeautifulSoup
import requests
import re
import csv

pdflist = []         #this is what the script will return to get text snippets

#%%
#sets save location 
save_location = "/Users/maxfranklin/Documents/scrape3"  #if running on Mac or Linux, make sure to change the \\ to /

#defines a function used to convert into utf8  to ascii, used during the scraping process
whitespaces = re.compile('\s+', flags=re.M)
def utf8_to_ascii(s, ws=whitespaces):
    s = s.encode("utf8")
    s = s.decode("ascii", errors="replace")
    s = s.replace(u"\ufffd", "")
    s = ws.sub(" ", s)
    return s.strip()
#%%
#This part does the actual scraping. Set the range to determine which items you get from the webscraping.
quote_page = "https://journals.aps.org/prper/abstract/10.1103/{}.{}.0{}01{}"
for i in range(10,16):
    if i <= 11:
        string = "PhysRevSTPER"
    else:
        string = "PhysRevPhysEducRes"

    for j in range(1,2):
        for l in range(1,3):
            if l < 10:
                l = "0" + str(l)
            else:
                l = str(l)
                     
            response = requests.get(quote_page.format(string,i,j,l))
            print(response)
            html = response.content
            #print(type(html))                      #these bits can be used to troubleshoot. If you need to see
            #print(html)                            #anything about what is contained in the html, or what is 
            #print(str(html))                       #in the page being scraped, use these. 
            #print(quote_page.format(string,i,j,l))

            page = urllib.request.urlopen(quote_page.format(string,i,j,l))
            soup = BeautifulSoup(page, "html.parser")
            for text in soup.find_all('div', class_='article-additional-info'):
                for links in text.find_all('a'):
                    print (links.get('href'))
           
            links = soup.find_all('a', href=re.compile(r'(.pdf)'))        #finds all pdfs in the page, puts first in 
            url_list = []                                                 #the pdflist
            for el in links:
                url_list.append(("https://journals.aps.org" + el['href']))
            #print (url_list)
            pdflist.append(url_list[0])
            
            
            try:
                if "The page you requested could not be found, please check the link and try again. If you believe you have reached this page in error please contact" not in str(html):
                    data=[]
                    #index=0
                    #while(index<19):  #gets up to 19 coauthors. You can adjust this number, but you shouldn't need to. 
                    name = soup.get_text()
                    data.append(name)
                    #index = index + 1
                    lst=[]
                    #print(data)
                    for k in data:
                        k = utf8_to_ascii(k)
                        k = k.encode("utf-8")
                        lst.append(k)
                    #print(lst[-2])
                    'print (lst)'
                    'KEEP APPEHEND IN BINARY MODE! ("ab"), otherwise it will skip lines and wont be able to extract information'
                    with open(save_location, "a") as f:
                        wr = csv.writer(f, delimiter=",")
                        wr.writerow(lst)
                    f.close()
        
                time.sleep(5)
            except IndexError:
                print("You have an issue")
                continue

"10007 to 25435 range of abstracts"
'''last web scraping file was obtaining all the correct information from AAPT, but it was converting everything into txt lists, which
is not useful, I needed the csv format to extract information. The error that would run into was that since everything was filled up
with commas, instead of taking the whole abstract as a variable, it would cut it whenever it would encounter the closest comma
(i.e given the list A= ["hi", "my name", "is Waika, and", "my favourite fruit","is watermelon"]. If I wanted to extract the third
value, that is index = 2, it would give me only "is Waika") I need to run the correct version of code'''
print (pdflist)
print("Done!")  #you can comment this out if you want to, but the code doesn't show anything when it's done. This is just so the human knows.



# In[ ]:



