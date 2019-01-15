from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    # URL of headlines page
    url_1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # Visit headlines page
    browser.visit(url_1)
    # Create bs object for headlines page
    soup_1 = bs(browser.html, "html.parser")
    # Scrape for latest title and description of latest headline
    news_title = soup_1.find_all('div', class_='content_title')[0].a.text
    description = soup_1.find_all('div', class_='rollover_description_inner')[0].text
    
    # Scrape for URL of news main page for lastest headline
    news_url = "https://mars.nasa.gov" + soup_1.find_all('div', class_='content_title')[0].a.get('href')    
    # Visit news main page
    browser.visit(news_url)
    # Create bs object for news main page for latest headline
    soup_news = bs(browser.html, "html.parser")
    # Scrap for featured img link of latest headline from news main page
    featured_img_url = "https://mars.nasa.gov" + soup_news.find('img', id='main_image')['src']

    
    # URL of twitter weather page
    url_weather = "https://twitter.com/marswxreport?lang=en"
    # Visit twitter weather page
    browser.visit(url_weather)
    # Create bs object for twitter weather page
    soup_weather = bs(browser.html, "html5lib")
    # Scrape for latest weather tweet
    mars_weather = soup_weather.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip("55pic.twitter.com/Or8q1l3tka")

    
    # URL of mars facts page
    url_facts = "https://space-facts.com/mars/"

    # Parse for tables from page using pandas (result is DataFrame)
    mars_facts = pd.read_html(url_facts)[0]
    # Rename columns
    mars_facts.columns=[" ", "Value"]
    # reset index
    mars_facts.set_index([" "], inplace=True)
    # Convert to html
    mars_facts_html = mars_facts.to_html().replace('\n', '')
 
   
    #  Mars hemisphere images URLs 
    hemisphere_image_urls = {
        'vmh': {"title": "Valles Marineris Hemisphere", "img_url": "https://mars.nasa.gov/system/resources/detail_files/6453_mars-globe-valles-marineris-enhanced-full2.jpg"},
        'ch': {"title": "Cerberus Hemisphere", "img_url": "https://planetary.s3.amazonaws.com/assets/images/4-mars/2014/20140202_cerberus_enhanced_f840.jpg"},
        'sh': {"title": "Schiaparelli Hemisphere", "img_url": "https://planetary.s3.amazonaws.com/assets/images/4-mars/2014/20140202_schiaparelli_enhanced_f840.jpg"},
        'smh': {"title": "Syrtis Major Hemisphere", "img_url": "https://planetary.s3.amazonaws.com/assets/images/4-mars/2014/20140202_syrtis_major_enhanced_f840.jpg"}
    }

    # Add to variables to dictionary
    mars = {
        "news_title": news_title,
        "descrition": description,
        "featured_image_url": featured_img_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_html, 
        "mars_hemisphere_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()


    return mars


if(__name__ == '__main__'):
    print(scrape())
    
