import datetime
from requests_html import HTMLSession
from .database import SessionLocal
from .crud import create_news
from .schemas import NewsCreate, News

def single_news_scraper(url: str):
    session = HTMLSession()
    try:
        response = session.get(url)
        # response.html.render()  # This will download Chromium if not found

        """publisher_website = url.split('/')[2]
        publisher = publisher_website.split('.')[-2]
        title = response.html.find('headline-header margin-bottom-10', first=True).text
        reporter = response.html.find('col-md-6 col-sm-6', first=True).text
        datetime_element = response.html.find('col-md-6 col-sm-6', first=True)
        news_datetime = datetime_element.attrs['datetime']
        category = response.html.find('.print-entity-section-wrapper', first=True).text
        content = '\n'.join([p.text for p in response.html.find('p')])
        img_tags = response.html.find('image-holder margin-bottom-10')
        images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]
        news_datetime = datetime.datetime.now()"""
  
        
        
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

        
        
        

        print(f"Scraped news from {url}")
        print(f"Title: {title}")
        print(f"Reporter: {reporter}")
        print(f"Date: {news_datetime}")
        print(f"Category: {category}")
        print(f"Images: {images}")


        return NewsCreate(
            publisher_website=publisher_website,
            news_publisher=publisher,
            title=title,
            news_reporter=reporter,
            datetime=news_datetime,
            link=url,
            news_category=category,
            body=content,
            images=images,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def scrape_and_store_news(url: str, db: SessionLocal): # type: ignore
    # db = SessionLocal()
    news_data = single_news_scraper(url)
    print(news_data)
    inserted_news = ""
    if news_data:
        # print(news_data)
        inserted_news = create_news(db=db, news=news_data)
    db.close()

    return inserted_news
