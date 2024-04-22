from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from loguru import logger
import website_diff.htmldiff as hd

import pdb

# def soup_diff(old_soup, new_soup):
#     s = BeautifulSoup("", "html.parser")
#     s.extend(html_diff.NodeOtherTag(old_soup, new_soup, True).dump_to_tag_list(s))
#     return s

def diff(filepath_old, filepath_new, diff_images, root_element, out_root, filepath_out):
    # load the html files
    with open(filepath_old, 'r') as f:
        html_old = f.read()
    with open(filepath_new, 'r') as f:
        html_new = f.read()

    # TODO
    ## remove large data elements (plotly viz, altair viz) prior to diff
    #soup_old = BeautifulSoup(html_old, 'html.parser')
    #for elem in soup_old.select_one(root_element).find_all('script', {'type':'text/javascript'}):
    #    elem.decompose()
    #for elem in soup_old.select_one(root_element).find_all('div', {'class':'plotly'}):
    #    elem.contentdecompose()
    #html_old = str(soup_old)
    #soup_new = BeautifulSoup(html_new, 'html.parser')
    #for elem in soup_new.select_one(root_element).find_all('script', {'type':'text/javascript'}):
    #    elem.decompose()
    #for elem in soup_new.select_one(root_element).find_all('div', {'class':'plotly'}):
    #    elem.decompose()
    #html_new = str(soup_new)

    # generate the html diff
    diff = hd._htmldiff(html_old, html_new)
    soup = BeautifulSoup(diff, "html.parser")

    is_diff = False
    for tag in soup.select_one(root_element).select('ins'):
        tag['class'] = tag.get('class',[]) + ['diff']
        is_diff = True
    for tag in soup.select_one(root_element).select('del'):
        tag['class'] = tag.get('class',[]) + ['diff']
        is_diff = True
    for tag in soup.select_one(root_element).select('img'):
        relpath = tag.get('src')
        img_path_from_root = os.path.relpath(os.path.normpath(os.path.join(os.path.dirname(filepath_out), relpath)), out_root)
        if img_path_from_root in diff_images:
            tag['class'] = tag.get('class',[]) + ['diff']
            is_diff = True

    # append the js/css files
    js_soup = BeautifulSoup('<script src="website_diff.js"></script>', 'html.parser')
    css_soup = BeautifulSoup('<link rel="stylesheet" href="website_diff.css" type="text/css"/>', 'html.parser')
    soup.select_one("head").append(js_soup)
    soup.select_one("head").append(css_soup)

    # write the diff
    with open(filepath_out, 'w') as f:
        f.write(str(soup))

    return is_diff

# def highlight_links(filepath, root, add_pages, diff_pages, diff_images):
def highlight_links(file, root, add_pages, del_pages, diff_pages):
    # load the html
    logger.debug(f"Opening html file at {os.path.join(root, file)}")
    with open(os.path.join(root, file), 'r') as f:
        html = f.read()
    # parse
    soup = BeautifulSoup(html, 'html.parser')

    # current directory
    curdir = os.path.dirname(file)

    # find all links
    for link in soup.select('a'):
        # extract the url
        ref = link.get('href')
        # remove anchors
        ref = ref.split('#')[0]
        # parse the url
        url = urlparse(ref)
        logger.debug(f"Found link in {file}: {ref}")
        logger.debug(f"Parsed link: {url}")
        if not bool(url.netloc) and ref[-5:] == '.html':
            # this is a relative path to an html file. Find path relative to root
            #relative_link_path = os.path.relpath(os.path.normpath(os.path.join(curdir, ref)), diff)
            if url.path in diff_pages:
                logger.debug(f"This is a relative path to a diff'd page. Highlighting")
                link['class'] = link.get('class', []) + ["link-to-diff"]
            elif url.path in add_pages:
                logger.debug(f"This is a relative path to an added page. Highlighting")
                link['class'] = link.get('class', []) + ["link-to-add"]
            elif url.path in del_pages:
                logger.debug(f"This is a relative path to a deleted page. Highlighting")
                link['class'] = link.get('class', []) + ["link-to-del"]
            else:
                logger.debug(f"This is a relative path, but to an unchanged paged. Skipping")
        else:
            logger.debug(f"Not a relative path, or not an .html file. Skipping")

    with open(os.path.join(root, file), 'w') as f:
        f.write(str(soup))

    # find all images
    # TODO...



