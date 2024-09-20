import website_diff as wd
import os
from loguru import logger
from bs4 import BeautifulSoup

# Finds all visual elements that are not images (e.g. plotly, altair)
# and prerenders them into a dir called "prerendered". 
# Replaces visual elements with a single img tag with src path to prerendered image.
def prerender(old,new,diff,selector,index):
    # Find all pages in old dir
    old_pages = wd.crawler.crawl(os.path.join(old, index), set(), selector)
    old_pages = set(os.path.relpath(path, old) for path in old_pages)

    # Find all pages in new dir
    new_pages = wd.crawler.crawl(os.path.join(new, index), set(), selector)
    new_pages = set(os.path.relpath(path, new) for path in new_pages)

    _prerender_pages(old, old_pages, selector)
    _prerender_pages(new, new_pages, selector)

    # Create prerendered in diff dir
    os.makedirs(os.path.join(diff, 'prerendered'), exist_ok=True)

def _prerender_pages(dir, pages, selector):
    for page in pages:
        filepath = os.path.join(dir, page)

        logger.info(f"Pre-rendering {filepath}")

        with open(filepath, 'r') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        # Render altair visualizations
        wd.render.altair.render(filepath, 'prerendered', soup, selector)

        # Render plotly visualizations
        wd.render.plotly.render(filepath, 'prerendered', soup, selector)

        with open(filepath, 'w') as f:
            f.write(str(soup))