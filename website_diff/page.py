import html_diff
from bs4 import BeautifulSoup
import os

def diff(filepath_old, filepath_new, diff_images, root_element, filepath_out):
    # load the html files
    with open(filepath_old, 'r') as f:
        html_old = f.read()
    with open(filepath_new, 'r') as f:
        html_new = f.read()

    # generate the html diff
    hdf = html_diff.diff(html_old, html_new)
    soup = BeautifulSoup(hdf, 'html.parser')

    is_diff = False
    if (soup.find(root_element).find('ins') is not None) or (soup.find(root_element).find('del') is not None):
        # add the scrolling javascript and style file to highlight the diff
        js_soup = BeautifulSoup('<script src="website_diff.js"></script>', 'html.parser')
        css_soup = BeautifulSoup('<link rel="stylesheet" href="website_diff.css" type="text/css"/>', 'html.parser')
        soup.find("head").append(js_soup)
        soup.find("head").append(css_soup)
        is_diff = True

    # write the diff
    with open(filepath_out, 'w') as f:
        f.write(str(soup))

    return is_diff

def highlight_links(filepath, root, add_pages, diff_pages, diff_images):
    # load the html
    with open(os.path.join(root, filepath), 'r') as f:
        html = f.read()
    # parse
    soup = BeautifulSoup(html, 'html.parser')

    # current directory
    curdir = os.path.dirname(filepath)

    # find all links
    for link in soup.find_all('a'):
        # extract the url
        ref = link.get('href')
        # remove anchors
        ref = ref.split('#')[0]
        # parse the url
        url = urlparse(ref)
        logger.debug(f"Found link in {filepath}: {ref}")
        logger.debug(f"Parsed link: {url}")
        if not bool(url.netloc) and ref[-5:] == '.html':
            # this is a relative path to an html file. Find path relative to root
            relative_link_path = os.relpath(os.path.normpath(os.path.join(curdir, ref)), root)
            if relative_link_path in diff_pages:
                logger.debug(f"This is a relative path to a diff'd page. Highlighting")
                link['class'] = link.get('class', []) + ["link-diff"]
            elif relative_link_path in add_pages:
                logger.debug(f"This is a relative path to an added page. Highlighting")
                link['class'] = link.get('class', []) + ["link-add"]
            else:
                logger.debug(f"This is a relative path, but to an unchanged paged. Skipping")
        else:
            logger.debug(f"Not a relative path, or not an .html file. Skipping")

    # find all images
    # TODO...



