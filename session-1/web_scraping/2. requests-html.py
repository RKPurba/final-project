"""
Author: Kalim Amzad
Version: 1.1

This module demonstrates the usage of the `requests-html` library in Python for web scraping.
It covers various real-world examples including rendering JavaScript, extracting data, and
working with HTML elements. This script is designed as an educational tool for understanding
web scraping using Python.
"""

from requests_html import HTMLSession

def render_javascript(url):
    """
    Demonstrates how to render JavaScript using the `requests-html` library.
    This function fetches the page content after JavaScript has been executed.

    Parameters:
    url : str
        The URL of the website to scrape.

    Returns:
    None
    """
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render()  # This will download Chromium if not found
        print("Rendered web page:", response.html.html)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def extract_information(url):
    """
    Extracts and prints specific information from a webpage using CSS selectors.

    Parameters:
    url : str
        The URL of the website to scrape.

    Returns:
    None
    """
    session = HTMLSession()
    try:
        response = session.get(url)
        
        # Extracting the title
        title_tag = response.html.find('h1')
        if title_tag:
            print(f"{len(title_tag)} title tag(s) found:")
            print(f"Title: {title_tag[0].text}")
        else:
            print("No title tag found")

        # Extracting the datetime attribute
        datetime_element = response.html.find('time', first=True)
        if datetime_element and 'datetime' in datetime_element.attrs:
            datetime = datetime_element.attrs['datetime']
            print(f"Datetime attribute: {datetime}")
        else:
            print("No datetime attribute found")

        # Advanced usage of extraction using XPath
        temp = response.html.xpath('//div[contains(@class, "time-social-share-wrapper")]//time', first=True)
        if temp and 'datetime' in temp.attrs:
            datetime = temp.attrs['datetime']
            print(f"Advanced datetime extraction: {datetime}")
        else:
            print("Advanced datetime extraction not found")

        #Example: Extracting all links
        links = response.html.find('a')
        print(f"{len(links)} links found:")
        for link in links:
            print(f"Link Text: {link.text} Link href: {link.attrs.get('href')}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def main():
    """
    Main function to execute the web scraping examples.
    """
    # print("Rendering JavaScript on a web page...")
    # render_javascript('https://example.com')

    print("\nExtracting information from a web page...")
    extract_information('https://www.dailynayadiganta.com/national/1')
if __name__ == "__main__":
    main()
