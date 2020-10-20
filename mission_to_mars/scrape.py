# -------------------------------------------------------------------------------------
# ------ Mission to Mars - Web Scrapping Challenge ------------------------------------
# ------ Matheus Gratz - matheusgratz@gmail.com - https://github.com/matheusgratz/ ----
# -------------------------------------------------------------------------------------

# ------------------------------
# -------- Dependencies --------
# ------------------------------
import os
import re
import requests
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser

# ------------------------------
# ----- 1. NASA Mars News ------
# ------------------------------

def mars_news(browser):
    # URL of Mars News Website
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object and parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    # Assign the text to variables that you can reference later.
    news_title = soup.find_all('div', class_='content_title')
    news_paragraph = soup.find_all('div', class_='rollover_description_inner')

    title = news_title[0].text.replace('\n', '')
    paragraph = news_paragraph[0].text.replace('\n', '')

    return title, paragraph

# ------------------------------
# -- 2. JPL Mars Space Images --
# ------------------------------

def space_image(browser):

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img_url = image_soup.select_one("figure.lede a img").get("src")
    img_url = f'https://www.jpl.nasa.gov{img_url}'

    # browser.quit()

    return img_url

# ------------------------------
# ----- 3. Mars Weather --------
# ------------------------------

def mars_twitter_weather(browser):

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")

    mars_weather_tweet = weather_soup.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})

    try:
        mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
        mars_weather
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = weather_soup.find('span', text=pattern).text

    # browser.quit()
    
    return mars_weather
   

# ------------------------------
# ------ 4. Mars Facts ---------
# ------------------------------

# Visit the Mars Facts Site Using Pandas to Read
def facts_mars():

    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)

    return mars_df.to_html(classes="table table-striped")

# ------------------------------
# ----- 5. Mars Hemispheres ----
# ------------------------------

def hemisphere_imgs(browser):

    browser = Browser('chrome', headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_urls = []

    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_urls.append(hemisphere)
        browser.back()

    # browser.quit()

    return hemisphere_urls

def get_everything():
    browser = Browser('chrome', headless=False)

    news_title, news_paragraph = mars_news(browser)
    img_url = space_image(browser)
    mars_weather = mars_twitter_weather(browser)
    facts = facts_mars()
    hemisphere_urls = hemisphere_imgs(browser)
    timestamp = dt.datetime.now()

    data_dict = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_urls,
        "last_modified": timestamp
    }

    browser.quit()
    return data_dict

if __name__ == "__main__":
    
    print(get_everything())
    