import click
import sys
import traceback
import os
import shutil
import website_diff as wd
from loguru import logger

@click.command()
@click.option('-o', '--old', help='A directory containing the old version of the website (index.html should be in this directory).', required=True)
@click.option('-n', '--new', help='A directory containing the new version of the website (index.html should be in this directory).', required=True)
@click.option('-d', '--diff', help='A path to a new directory that will contain the diffed version of the website (this directory should not exist yet).', required=True)
@click.option('-s', '--selector', default='html', help='A BeautifulSoup selector for the main content of the page. website_diff will only search inside these elements for diffs')
@click.option('-i', '--index', default='index.html', help='The main html page filename')
def main(old, new, diff, selector, index):
    # get paths for js/css files
    this_dir, this_filename = os.path.split(__file__)
    diffjs_path = os.path.join(this_dir, "static/website_diff.js")
    diffcss_path = os.path.join(this_dir, "static/website_diff.css")

    # set log level to suppress debug messages
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    # copy over the new directory to the diff directory
    # also ensure directory doesn't exist before this code runs
    # copy the js/css to all subdirs (just brute forcing this for now...)
    logger.info(f"Preparing new website directory at {diff}")
    shutil.copytree(old, diff)
    shutil.copytree(new, diff, dirs_exist_ok=True)
    for r, _, _ in os.walk(diff):
        shutil.copy2(diffjs_path, r)
        shutil.copy2(diffcss_path, r)

    try:
        # crawl the old/new websites for pages
        logger.info(f"Crawling old website at {old}")
        old_pages = wd.crawler.crawl(os.path.join(old, 'index.html'), selector)
        logger.info(f"Crawling new website at {new}")
        new_pages = wd.crawler.crawl(os.path.join(new, 'index.html'), selector)

        # convert paths to relative
        old_pages = {os.path.relpath(path, old) : soup for (path, soup) in old_pages.items()}
        new_pages = {os.path.relpath(path, new) : soup for (path, soup) in new_pages.items()}

        # perform render tasks, gather diff targets for old pages
        old_targets = {}
        for relpath in old_pages:
            print(f"Rendering page {os.path.join(old, relpath)}")
            for task in render.tasks:
                print(f"Performing render task: {task}")
                wd.render.tasks[task](old, relpath, old_pages[relpath], selector)
            print(f"Gathering diff targets from page {os.path.join(old, relpath)}")
            for item in target.items:
                print(f"Gathering item: {item}")
                old_targets[item] = wd.target.items[item].gather(old, relpath, old_pages[relpath], selector)
                # TODO immediately diff it to avoid memory blowup
                # TODO add "diff" tag to page above if a diff is found
                # TODO render both new and old prior to doing item diffs

        # perform render tasks, gather diff targets for new pages
        new_targets = {}
        for relpath in new_pages:
            print(f"Rendering page {os.path.join(new, relpath)}")
            for task in render.tasks:
                print(f"Render task: {task}")
                wd.render.tasks[task](new, relpath, new_pages[relpath], selector)
            print(f"Gathering diff targets from page {os.path.join(new, relpath)}")
            for item in target.items:
                print(f"Gathering item: {item}")
                new_targets[item] = wd.target.items[item].gather(new, relpath, new_pages[relpath], selector)

        # figure out which images are newly added, deleted, and common
        logger.info(f"Separating images into new, deleted, and common")
        add_images = new_images - old_images
        logger.info(f"{len(add_images)} newly added images")
        del_images = old_images - new_images
        logger.info(f"{len(del_images)} deleted images")
        com_images = new_images.intersection(old_images)
        logger.info(f"{len(com_images)} common images")

        # highlight the newly added images, diff the others
        logger.info(f"Highlighting new images")
        for img in add_images:
            logger.info(f"Highlighting new image {img}")
            wd.image.highlight_add(os.path.join(new, img), os.path.join(diff, img))
        logger.info(f"Highlighting deleted images")
        for img in del_images:
            logger.info(f"Highlighting deleted image {img}")
            wd.image.highlight_del(os.path.join(old, img), os.path.join(diff, img))
        logger.info(f"Diffing common images")
        diff_images = add_images.union(del_images)
        for img in com_images:
            logger.info(f"Diffing image {img}")
            is_diff = wd.image.diff(os.path.join(old,img), os.path.join(new,img), os.path.join(diff,img))
            logger.info(f"Image diff {img}: {'difference!' if is_diff else 'same'}")
            if is_diff:
                diff_images.add(img)

        # figure out which pages are newly added, deleted, and common
        logger.info(f"Separating pages into new, deleted, and common")
        add_pages = new_pages - old_pages
        logger.info(f"{len(add_pages)} newly added pages")
        del_pages = old_pages - new_pages
        logger.info(f"{len(del_pages)} deleted pages")
        com_pages = new_pages.intersection(old_pages)
        logger.info(f"{len(com_pages)} common pages")

        # diff the common pages
        logger.info(f"Diffing common website pages")
        diff_pages = set()
        for page in com_pages:
            logger.info(f"Diffing page {page}")
            is_diff = wd.page.diff(os.path.join(old, page), os.path.join(new, page), diff_images, root, diff, os.path.join(diff, page))
            logger.info(f"Page diff {page}: {'difference!' if is_diff else 'same'}")
            if is_diff:
                diff_pages.add(page)

        # TODO
        ## loop over all pages, modifying <a> tags that point to pages with diffs with highlights
        #logger.info(f"Highlighting links to diff'd pages")
        #for page in new_pages.union(old_pages):
        #    wd.page.highlight_links(page, diff, add_pages, diff_pages)
    except Exception:
        # print the exception
        print(traceback.format_exc())

        # cleanup diff dir if there was a failure
        print(f"Cleaning up directory {diff}")
        shutil.rmtree(diff)
