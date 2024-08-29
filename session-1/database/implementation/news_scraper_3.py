import os
PYPPETEER_CHROMIUM_REVISION = '1263111'

os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

import time
import datetime
from datetime import datetime
from requests_html import HTMLSession
from mysql.connector import Error
from db_connection import create_db_connection
from news_insert_modified import (
                            execute_query,
                            insert_reporter,
                            get_reporter_id, 
                            insert_category,
                            get_category_id, 
                            insert_news,
                            get_news_id,
                            insert_publisher,
                            get_publisher_id,
                            insert_image)


def process_and_insert_news_data(connection, publisher_website, publisher, title, reporter, news_datetime, category, images, url):
    
    try:
        # Insert category if not exists
        category_id = insert_category(connection, category, f"{category}") 
        c_id = get_category_id(connection, category)
        
        # Insert reporter if not exists
        reporter_id = insert_reporter(connection, reporter, f"{reporter}@{publisher_website}")
        r_id = get_reporter_id(connection, reporter)
        
        # Insert publisher as a placeholder (assuming publisher is not provided)
        publisher_id = insert_publisher(connection, publisher, f"{publisher_website}")
        p_id = get_publisher_id(connection, publisher)
        
        # Insert news article
        news_id = insert_news(connection, c_id, r_id, p_id, news_datetime, title, news_body, url)
        n_id = get_news_id(connection, title)
        
        # Insert images
        for image_url in images:
            image_id = insert_image(connection, n_id, image_url)
    
    except Error as e:
        print(f"Error while processing news data - {e}")


def single_news_scraper(url):
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render()  # This will download Chromium if not found
        # time.sleep(3)

        publisher_website = url.split('/')[2]
        publisher = publisher_website.split('.')[-2]

        # Extract the title
        title = response.html.find('h1', first=True).text

        # Extract the reporter's name
        reporter = response.html.find('.content-info p', first=True).text

        # Extract the publication date and time
        datetime_element = response.html.find('.content-info .time', first=True)
        news_datetime = datetime_element.text

        # Extract the category of the news
        category = response.html.find('.breadcrumb', first=True).text

        # Extract the content of the article
        content = '\n'.join([p.text for p in response.html.find('.description p')])

        # Extract image sources
        img_tags = response.html.find('.image-holder img')
        images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]

        # If you want the current time as a fallback
        news_datetime = datetime.datetime.now()

        #print(publisher_website, publisher, title, reporter, news_datetime, category, images)
        # process_and_insert_news_data(conn, publisher_website, publisher, title, reporter, reporter_location, datetime, category, images)
        return publisher_website, publisher, title, reporter, news_datetime, category, news_body, images
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


# Example usage
if __name__ == "__main__":
    conn = create_db_connection()
    if conn is not None:
        bd_urls = [
            "https://www.dailynayadiganta.com/politics/859421/%E0%A6%B6%E0%A7%87%E0%A6%96-%E0%A6%B9%E0%A6%BE%E0%A6%B8%E0%A6%BF%E0%A6%A8%E0%A6%BE%E0%A6%95%E0%A7%87-%E0%A6%8F%E0%A6%95-%E0%A6%A6%E0%A6%BF%E0%A6%A8%E0%A7%87%E0%A6%B0-%E0%A6%9C%E0%A6%A8%E0%A7%8D%E0%A6%AF-%E0%A6%B9%E0%A6%B2%E0%A7%87%E0%A6%93-%E0%A6%86%E0%A6%AF%E0%A6%BC%E0%A6%A8%E0%A6%BE-%E0%A6%98%E0%A6%B0%E0%A7%87-%E0%A6%B0%E0%A6%BE%E0%A6%96%E0%A6%BE-%E0%A6%B9%E0%A7%8B%E0%A6%95-%E0%A6%AB%E0%A6%BE%E0%A6%B0%E0%A7%81%E0%A6%95"
            
        ]
        
        for url in bd_urls:
            result = single_news_scraper(url)
            if result is not None:
                publisher_website, publisher, title, reporter, news_datetime, category, news_body, images = result
                process_and_insert_news_data(conn, publisher_website, publisher, title, reporter, news_datetime, category, news_body, images, url)
            else:
                print(f"Failed to scrape the news article from URL: {url}")