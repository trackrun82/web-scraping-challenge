from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

    # First URL scraping
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(5)
    
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, "lxml")

    articles = nasa_soup.find('li', class_='slide')
    mars["title"] = articles.find('div', class_='content_title').get_text()
    mars["p"] = articles.find('div', class_='article_teaser_body').get_text()

    # Second URL scraping
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    
    image_html = browser.html
    image_soup = bs(image_html, 'lxml')

    featured_image = image_soup.find('a', class_='button fancybox')['data-fancybox-href']
    mars['featured_image_url'] = f'https://www.jpl.nasa.gov{featured_image}'

    # Third URL scraping
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(5)

    twitter_html = browser.html
    twitter_soup = bs(twitter_html, 'lxml')
    
    twitter = twitter_soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars['mars_weather'] = twitter.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').get_text()

    # Fourth URL scraping
    facts_url = 'https://space-facts.com/mars/'
    
    tables = pd.read_html(facts_url)

    df = tables[0]
    df.columns = ['Description', 'Values']
    df.set_index('Description', inplace=True)

    mars['mars_facts_table'] = df.to_html(table_id="Mars Planet Profile", border="2", justify="left", escape=False)

    # Fifth URL scraping
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    hemisphere_image_urls = []

    for x in range(0, 4):
        browser.visit(astro_url)
        browser_list = browser.links.find_by_partial_text('Enhanced')
        browser_list[x].click()
    
        astro_html = browser.html
        astro_soup = bs(astro_html, 'lxml')
    
        title = astro_soup.find('h2', class_='title').get_text()
    
        image = astro_soup.find('img', class_='wide-image')['src']
        img_url = f'https://astrogeology.usgs.gov{image}'

        dict = {"title":title, "img_url":img_url}
        hemisphere_image_urls.append(dict)

    mars['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()
    
    return mars
