import click
import sys
import os
import shutil
import website_diff as wd
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")

@click.command()
@click.option('--old', help='A directory containing the old version of the website (index.html should be in this directory).')
@click.option('--new', help='A directory containing the new version of the website (index.html should be in this directory).')
@click.option('--diff', help='A path to a new directory that will contain the diffed version of the website.')
@click.option('--root', default='html', help='A BeautifulSoup selector for the root element within which to search for diffs')
def _main(old, new, diff, root):
    # copy over the new directory to the diff directory
    # also ensure directory doesn't exist before this code runs
    logger.info(f"Preparing new website directory at {diff}")
    shutil.copytree(old, diff)
    shutil.copytree(new, diff, dirs_exist_ok=True)

    # crawl the old websites for pages and images
    logger.info(f"Crawling old website at {old}")
    old_images = set()
    old_gather = lambda filepath, html, soup, root_element : wd.crawler.gather_local_images(filepath, html, soup, root_element, old_images)
    old_pages = wd.crawler.crawl(os.path.join(old, 'index.html'), old_gather)
    # make old_images, old_pages relative to old dir
    old_pages = set(os.path.relpath(path, old) for path in old_pages)
    old_images = set(os.path.relpath(path, old) for path in old_images)

    # crawl the new websites for pages and images
    logger.info(f"Crawling new website at {new}")
    new_images = set()
    new_gather = lambda filepath, html, soup, root_element : wd.crawler.gather_local_images(filepath, html, soup, root_element, new_images)
    new_pages = wd.crawler.crawl(os.path.join(new, 'index.html'), new_gather)
    # make new_images, new_pages relative to new dir
    new_pages = set(os.path.relpath(path, new) for path in new_pages)
    new_images = set(os.path.relpath(path, new) for path in new_images)

    # figure out which images are newly added, deleted, and common
    logger.info(f"Separating images into new, deleted, and common")
    add_images = new_images.setdiff(old_images)
    logger.info(f"Newly added images: {add_images}")
    del_images = old_images.setdiff(new_images)
    logger.info(f"Deleted pages: {del_pages}")
    com_images = new_images.intersection(old_images)
    logger.info(f"Common pages: {com_images}")

    # highlight the newly added images, diff the others
    logger.info(f"Highlighting new images")
    for img in add_images:
        wd.image.highlight_add(os.path.join(new, img), os.path.join(diff, img))
    logger.info(f"Highlighting deleted images")
    for img in del_images:
        wd.image.highlight_del(os.path.join(old, img), os.path.join(diff, img))
    logger.info(f"Diffing common images")
    diff_images = add_images.union(del_images)
    for img in com_images:
        is_diff = wd.image.diff(os.path.join(old,img), os.path.join(new,img), os.path.join(diff,img))
        if is_diff:
            diff_images.add(img)

    # figure out which pages are newly added, deleted, and common
    logger.info(f"Separating pages into new, deleted, and common")
    add_pages = new_pages.setdiff(old_pages)
    logger.info(f"Newly added pages: {add_pages}")
    del_pages = old_pages.setdiff(new_pages)
    logger.info(f"Deleted pages: {del_pages}")
    com_pages = new_pages.intersection(old_pages)
    logger.info(f"Common pages: {com_pages}")

    # diff the common pages
    logger.info(f"Diffing common website pages")
    diff_pages = set()
    for page in com_pages:
        # TODO: account for diff'd images in is_diff here
        is_diff = wd.page.diff(os.path.join(old, page), os.path.join(new, page), diff_images, root, os.path.join(diff, page))
        if is_diff:
            diff_pages.add(page)

    # TODO
    ## loop over all pages, modifying <a> tags that point to pages with diffs with highlights
    #logger.info(f"Highlighting links to diff'd pages")
    #for page in new_pages.union(old_pages):
    #    wd.page.highlight_links(page, diff, add_pages, diff_pages)

def main():
    _main()


