#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#this is a webscraper for physrev
#put in the volume and issue you want, and number of articles in it (may need number of articles+1)
#returns urls of downloadable pdfs of each article in that issue
#PhysRev doesn't like mass downloads, so make sure you include a delay between the download steps
def scrape(volume, issue, article_number):
    import time
    quote_page = "https://journals.aps.org/prper/pdf/10.1103/{}.{}.0{}01{}"
    urllist = []
    if volume <= 11:
        string = "PhysRevSTPER"
    else:
        string = "PhysRevPhysEducRes"
    for i in range (1,article_number):
        
        if i < 10:
            url = quote_page.format(string, volume, issue, str(0) + str(i))
        else:
            url = quote_page.format(string, volume, issue, i)
        urllist.append (url)

