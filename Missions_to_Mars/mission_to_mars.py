#import dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import os
import pandas as pd

def init_browser():
    #this is the same path that is in the same folder/path as the juypter notebook
    executable_path = {'executable_path': 'chromedriver.exe'}

    #headless opens in browser that we cannot see
    return Browser('chrome', **executable_path, headless=False)
#init_browser()

# In[2]:
def scrape():

    browser = init_browser()

## Step 1 - Scraping
#Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
### NASA Mars News
#Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
#URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'


    # In[24]:


    #Retrieve page with the requests module
    response = requests.get(url)


    # In[25]:


    #Create BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')


    # In[5]:


    #Examine the results, then determine element that contains sought info
    print(soup.prettify())


    # In[26]:


    #need to clarify which list items we need, find all list items that contain a particilar class
    results = soup.find_all('div', class_="content_title")
    #print(len(results))
    print(results)


    # In[27]:


    #wrap prettify in print statment
    title=results[0].text
    print(title)


    # In[32]:


    # Identify and return paragraph of listing
    paragraph = soup.find('div', class_="rollover_description_inner").text
    print(paragraph)


    # In[33]:
    #new dependencies that writes code to tell program what to do
 
    # In[ ]:


    #Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
    #Make sure to find the image url to the full size `.jpg` image.
    #Make sure to save a complete url string for this image.

    # In[34]:

    # In[38]:


    #Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    #Define URL to scrape and inform the browser to visit the page
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #tells the browser where to go . vists 

    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')


    # In[40]:


    #find featured image
    # Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # # Using BS, we can execute standard functions to capture the page's content
    featured_image_url = soup.find('figure', class_='lede')
    
    print(featured_image_url)
    
    # In[44]:


    image=featured_image_url.a['href']
    final_image='https://www.jpl.nasa.gov'+ image
    print(final_image)


    # In[ ]:


    #Iterate over multiple pages and scrape content from each
    # work with html for page and capture the info, take the browser and do this for from 
    
    # In[45]:


    # #Close the browser window
    #browser.quit()


    # In[47]:


    #Import dependencies
    import pandas as pd


    # In[48]:


    ### Mars Facts
    #Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #Use Pandas to convert the data to a HTML table string.

    url='https://space-facts.com/mars/'


    # In[49]:


    tables = pd.read_html(url)
    len(tables)


    # In[50]:


    print(type(tables))
    print(type(tables[0]))


    # In[55]:


    df = tables[2]
    df.columns=['Facts', 'Values']


    # In[56]:


    df.set_index('Facts', inplace=True)
    df.head()#Use Pandas to convert the data to a HTML table string.


    # In[57]:


    #Use Pandas to convert the data to a HTML table string.
    html_table = df.to_html(classes='table table-striped')
    print(html_table)


    # In[58]:


    #save the table directly to a file
    df.to_html('factstable.html')


    # In[59]:


    ### Mars Hemispheres
    #Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())


    # In[65]:


    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys 

    items=soup.find_all(class_="itemLink product-item")
    print((items))


    # In[66]:


    hemi=[]
    for image in items:
        imgurl='https://astrogeology.usgs.gov'+image.get('href')
        hemi.append(imgurl)
    print(hemi)


    # In[ ]:


    #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    hemi_url=[]

    for item in hemi:
        response = requests.get(item)
        soup = BeautifulSoup(response.text, 'html.parser')
        beg_url=soup.find('a', href=True,text='Sample')
        fin_url=beg_url ['href']
        title=soup.find(class_='title').text.strip().replace(' Enhanced', '')
        hemi_url.append({'URL':fin_url, 'Title': title})
        
    #print(hemi_url)
    
    mission_dict={'Title': title, 'Paragraph': paragraph, 'Image' : final_image, 
    'Mars Facts': html_table, 'Hemisphere Images' : hemi_url }

    return mission_dict 

