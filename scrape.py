def scrape():

    #Dependencies
    from bs4 import BeautifulSoup
    import requests
    from splinter import Browser
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import pandas as pd
    import time

    #scraping the news
    news_url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response=requests.get(news_url)
    soup=BeautifulSoup(response.text,'html.parser')
    news_title=soup.find_all('div', class_='rollover_description_inner')[0].text
    news_title=news_title.split('\n')
    news_title=news_title[1]

    news_p=soup.find_all('div', class_='content_title')[0].text
    news_p=news_p.split('\n')
    news_p=news_p[2]

    #scraping featured image
    time.sleep(1)
    browser= webdriver.Chrome('chromedriver.exe')
    browser.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    button=browser.find_element_by_link_text("FULL IMAGE")
    button.click()
    pictures=browser.find_elements_by_tag_name('img')
    time.sleep(3)
    picture=browser.find_element_by_class_name("fancybox-image")
    featured_image_url=picture.get_attribute('src')

    #get tweet
    time.sleep(5)
    browser= webdriver.Chrome('chromedriver.exe')
    browser.get('https://twitter.com/marswxreport?lang=en')
    time.sleep(5)
    tweet=browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div[2]')
    mars_weather=tweet.text

    #get pandas table
    time.sleep(1)
    tables = pd.read_html('https://space-facts.com/mars/')
    df=tables[0]
    df.columns=['Record', 'Measurement']
    df.set_index('Record', inplace=True)
    html_table=df.to_html()

    #get images of hemispheres
    time.sleep(1)
    browser= webdriver.Chrome('chromedriver.exe')
    browser.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    links=browser.find_elements_by_class_name('itemLink')
    url_list=[]
    title_list=[]
    for link in links:
        title=link.text
        title_list.append(title)
        url=(link.get_attribute('href'))
        url_list.append(url)
    url_list=url_list[1::2]
    title_list=title_list[1::2]
    hemisphere_image_urls = {title_list[i]: url_list[i] for i in range(len(title_list))} 

    #final dictionary
    scrape_dict={"news_title":news_title,"featured_image_url": featured_image_url, "mars_weather": mars_weather, "html_table": html_table, "hemisphere_image_urls":hemisphere_image_urls}

    #plug it into mongo
    conn='mongodb://localhost:27017'
    client=pymongo.MongoClient(conn)
    db=client.mars_db
    mars_info = db.mars
    db.mars.drop()
    db.mars.insert_one(scrape_dict)