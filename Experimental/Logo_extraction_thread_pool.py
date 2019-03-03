from multiprocessing.dummy import Pool as ThreadPool
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import configparser
import logging
import sys

logging.basicConfig(filename='logo_extraction.log', level=logging.INFO, format='%(asctime)s %(message)s')

config = configparser.ConfigParser()
try:
    config.read('config.file')
    geckodriver_path = config['DEFAULT']['GECKODRIVER_LOCATION']

except FileNotFoundError:
    logging.error("File not found. Please place config.file in current working directory")

options = Options()
options.headless = True
options.log.level = 'error'
driver = webdriver.Firefox(options=options, executable_path=geckodriver_path)

images_link = {}

images_count = {'img': 0, 'a': 0, 'div': 0}

def get_url_from_file(input_filename):
    """
    Read input from file

    Returns:
    :rtype: list : List of urls from file
    """
    try:
        with open(input_filename) as input_file:
            urls = input_file.readlines()
            if not urls:
                logging.error("No valid url found! Input file is empty!")
                sys.exit(0)
            else:
                return urls
    except FileNotFoundError:
        logging.error("Input file not found.")

def get_element_by_xpath(driver, element_name):
    """
    Return element using xpath

    Parameters:
    :type element_name: str
    :type driver: selenium.webdriver.firefox.webdriver.WebDriver

    Returns:
    :rtype: selenium.webdriver.firefox.webelement.FirefoxWebElement

    """
    return driver.find_elements_by_xpath(element_name)

def fetch_logos(input_url):
    """
    Extract logos from website by finding different html elements

    Returns:
    :rtype: dict

    """
    urls = [input_url]
    while urls:
            # popping elements from front
            entry = urls.pop(0)

            # split is done since input is in format: http://webpage/url, http://logo/url/
            url = entry.split(",")[0]
            try:
                driver.get(url)
                logging.info("Processing URL: {}" + format(url))
            except:
                logging.error("Cannot process {} . Invalid URL.".format(url))
                #if not urls:
                    #driver.close()
                    #sys.exit(0)
                #else:
                continue
            # search for images inside <img> tag
            images = get_element_by_xpath(driver, '//img')
            images_link[url] = None
            if images:
                # process src attribute for logos found using 'img' tag
                images_count['img'] += 1
                for image in images:
                    logo_url = image.get_attribute('src')
                    logo_class = image.get_attribute('class')
                    logo_alt = image.get_attribute('alt')
                    if logo_url:
                        # check if name of the logo begins with "logo" or has an attribute that contains "logo"
                        if logo_url.split("/")[-1].lower().startswith("logo") or "logo" in logo_class.lower() or "logo" in logo_alt.lower() :
                            images_link[url] = logo_url
                            break
                        # check if name of the logo contains "logo" if not beginning with it
                        elif "logo" in logo_url.split("/")[-1].lower():
                            images_link[url] = logo_url
                        # check if the website's name is present in logo name and has the webiste address in it
                        elif url.split("/")[-1].split(".")[0] in logo_url.split("/")[-1] and url in logo_url:
                            images_link[url] = logo_url
            else:
                # search for images inside <a> tag
                images = get_element_by_xpath(driver,'//a/img')
                if images:
                    print("Images found using a tag")
                    images_count['a'] += 1
                    for image in images:
                        if image.get_attribute(''):
                            images_link[url] = image.get_attribute('src')
                else:
                    # search for images inside <div> tag
                    images = get_element_by_xpath(driver,'//div/a/img')
                    images_count['div'] += 1
                    for image in images:
                        if image.get_attribute('src'):
                            images_link[url] = image.get_attribute('src')

    #return images_link

def write_logo_urls_to_file(images_link):
    """

    Writes valid logo links from dictinary returned by fetch_logos to a text file

    Parameters:
    :type images_link: dict

    """
    #TODO: Add output file name in config file
    for key, value in images_link.items():
        with open("output_new.txt", "a") as out_f:
            if value is None:
                out_f.write(key + ",\n")
            else:
                try:
                    requests.get(value).raise_for_status()
                    out_f.write(key + "," + value + "\n")
                except:
                    out_f.write(key + ",\n")
                    logging.error("Unable to access logo when accessed through obtained URL.")

					
def calculateParallel(urls, threads=2):
    pool = ThreadPool(threads)
    pool.map(fetch_logos, urls)
    pool.close()
    pool.join()


if __name__ == "__main__":
    urls = get_url_from_file(sys.argv[1])
    calculateParallel(urls, 4)
    driver.close()
    write_logo_urls_to_file(images_link)
    logging.info("Total Number of URLs processed: {}".format(len(images_link)))
    logging.info("Analysis of logo extraction. Image sources by tags: ")
    logging.info(images_count)
