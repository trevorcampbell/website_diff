from bs4 import BeautifulSoup
import bs4
import os
from urllib.parse import urlparse
from loguru import logger
import website_diff.htmldiff as hd
import website_diff as wd

# Helper function that extends the contents of previous sibling with contents of input element
# if previous sibling has the same tag name as input element.
def _merge_previous(elem):
    if elem.previous_sibling is not None and elem.previous_sibling.name == elem.name:
        prev_sibling = elem.previous_sibling
        prev_sibling.extend(elem.extract().contents)

# Does a post-order traversal of the input element to find elements that have child ins or del elements.
# Merges any consecutive child ins or del elements.
def _merge_diffs(elem, soup):
    next_child = None

    if elem.contents:
        next_child = elem.contents[0]
    else: 
        return

    while next_child is not None:
        child = next_child
        next_child = child.next_sibling
        if isinstance(child, bs4.element.Tag):
            _merge_diffs(child, soup)
        else:
            continue

    # If there is only an ins or del element left in children, then propagate that ins or del tag
    # onto the parent element
    child = elem.contents[0]
    if len(elem.contents) == 1 and child.name in ['ins', 'del']:
        new_elem = soup.new_tag(child.name)
        elem.wrap(new_elem)
        child.unwrap()
        elem = new_elem
    # Delete element if all it contains is a newline character
    if len(elem.contents) == 1 and elem.name in ['ins', 'del'] and child == '\n':
        elem.decompose()
    elif elem.name in ['ins', 'del']:
        _merge_previous(elem)  

def diff(filepath_old, filepath_new, diff_images, root_element, out_root, filepath_out):
    # load the html files
    with open(filepath_old, 'r') as f:
        html_old = f.read()
    with open(filepath_new, 'r') as f:
        html_new = f.read()

    # generate the html diff
    diff = hd._htmldiff(html_old, html_new)
    soup = BeautifulSoup(diff, "html.parser")

    if not soup.html:
        raise Exception("html tag not found in soup")

    _merge_diffs(soup.html, soup)

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
        # skip <a> tags without href properties
        if ref is None:
            continue
        # remove anchors
        ref = ref.split('#')[0]
        # parse the url
        url = urlparse(ref)
        logger.debug(f"Found link in {file}: {ref}")
        logger.debug(f"Parsed link: {url}")
        if not bool(url.netloc) and ref[-5:] == '.html':
            path = os.path.normpath(url.path)
            if path in diff_pages:
                logger.debug(f"This is a relative path to a diff'd page. Highlighting")
                link['class'] = link.get('class', []) + ["link-to-diff"]
            elif path in add_pages:
                logger.debug(f"This is a relative path to an added page. Highlighting")
                link['class'] = link.get('class', []) + ["link-to-add"]
            elif path in del_pages:
                logger.debug(f"This is a relative path to a deleted page. Highlighting")
                link['class'] = link.get('class', []) + ["link-to-del"]
            else:
                logger.debug(f"This is a relative path, but to an unchanged paged. Skipping")
        else:
            logger.debug(f"Not a relative path, or not an .html file. Skipping")

    with open(os.path.join(root, file), 'w') as f:
        f.write(str(soup))

# Add banner to pages that were added or deleted
# TAKES: 
# diff_path - Path to diff folder
# add_pages - Set of added pages
# del_pages - Set of deleted pages
# RETURNS: nothing
def put_banner(diff_path, add_pages, del_pages):
    for page in add_pages.union(del_pages):
        with open(os.path.join(diff_path, page), 'r') as f:
            html_add = f.read()
        soup = BeautifulSoup(html_add, "html.parser")
        if page in add_pages:
            markup = """<div class='alert add-banner'><span class='closebtn' onclick="this.parentElement.style.display='none';">&times;</span>This is a newly added page.</div>"""
        else:
            markup = """<div class='alert del-banner'><span class='closebtn' onclick="this.parentElement.style.display='none';">&times;</span>This page was deleted from the website.</div>"""
        markup_soup = BeautifulSoup(markup, 'html.parser')
        soup.body.insert(1, markup_soup.div)
        # add css
        css_soup = BeautifulSoup('<link rel="stylesheet" href="website_diff.css" type="text/css"/>', 'html.parser')
        soup.select_one("head").append(css_soup)
        # write the page w/ banner
        with open(os.path.join(diff_path, page), 'w') as f:
            f.write(str(soup))
        

