import sys
import os
import website_diff as wd
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from loguru import logger

def crawl(filepath, gathered, content_selector = 'html', crawled = None):
    # initialize crawl cache
    if crawled is None:
        crawled = {}

    # normalize the filepath
    filepath = os.path.normpath(filepath)

    # page must end in html
    if filepath[-5:] != '.html':
        logger.error(f"Error: Tried to crawl non-html file {filepath}")
        return

    # don't re-crawl any page
    if filepath in crawled:
        logger.debug(f"Already crawled {filepath}. Skipping")
        return

    logger.info(f"Crawling {filepath}")

    # load the HTML, parse, and add to crawl dict
    with open(filepath, 'r') as f:
        html = f.read()

    logger.debug(f"Parsing {filepath}")
    soup = BeautifulSoup(html, 'html.parser')

    crawled[filepath] = soup

    # get current directory name
    curdir = os.path.dirname(filepath)
    logger.debug(f"Directory of {filepath}: {curdir}")

    # crawl all local, relative links
    for elem in soup.find_all(content_selector):
    	for link in elem.find_all('a'):
            # extract the url
            ref = link.get('href')
            # skip <a> tags without href properties
            if ref is None:
                continue
            # remove anchors
            ref = ref.split('#')[0]
            # parse the url
            url = urlparse(ref)
            logger.debug(f"Found link in {filepath}: {ref}")
            logger.debug(f"Parsed link: {url}")
            if not bool(url.netloc) and ref[-5:] == '.html':
                # this is a relative path to an html file. Try to find the local html file
                logger.debug(f"This is a relative path. Trying to crawl {os.path.join(curdir, ref)}")
                crawl(os.path.join(curdir, ref), gathered, content_selector, crawled)
            else:
                logger.debug(f"Not a relative path, or not an .html file. Skipping")

    gather_local_images(filepath, soup, content_selector, gathered)

    # return the set of crawled pages
    return crawled

def gather_local_images(filepath, soup, root_element, gathered):
    logger.debug(f"Finding all images in {filepath}")
    # get current directory name
    curdir = os.path.dirname(filepath)
    logger.debug(f"Directory of {filepath}: {curdir}")
    # find all local images
    for img in soup.find(root_element).find_all('img'):
        src = img.get('src')
        url = urlparse(src)
        logger.debug(f"Found image source in {filepath}: {src}")
        logger.debug(f"Parsed image source {filepath}: {url}")
        if not bool(url.netloc):
            # this is a relative image.
            imgpath = os.path.normpath(os.path.join(curdir, src))
            # Convert any svg files to png
            if src.split('.')[-1] == 'svg':
                logger.info(f"SVG {imgpath} found, converting to PNG.") 

                src_png = os.path.splitext(src)[0] + ".png"
                imgpath_png = os.path.splitext(imgpath)[0] + ".png"

                wd.target.image.convert_svg_to_png(imgpath, imgpath_png)

                img['src'] = src_png

                # Write change to img src attribute
                with open(filepath, 'w') as f:
                    f.write(str(soup))

                imgpath = imgpath_png
            logger.debug(f"This is a relative image path. Adding {imgpath} to images")
            gathered.add(imgpath)
        else:
            logger.debug(f"Not a relative image path.")
