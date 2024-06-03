import vl_convert as vlc
from json import JSONDecoder
from loguru import logger
from bs4 import BeautifulSoup
import os
import shutil

def extract_json_objects(text, decoder=JSONDecoder()):
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

def render(rootdir, relpath, soup, selector):
    for root_elem in soup.find_all(selector):
        for viz in root_elem.find_all('div', id=lambda x: x and x.startswith('altair-viz')):
            figparent = viz.find_parent('figure')
            if figparent is None:
                logger.warning(f"Found vega-embed but no figure parent. Skipping Element: {viz}")
                continue
            if 'altair-viz' not in viz.get('id'):
                logger.warning(f"Found vega-embed but not an altair viz. Skipping Element: {viz}")
                continue
            viz_id = figparent.get('id')
            logger.info(f"Found altair viz {viz} with id {viz_id}")
            # this is an altair viz; make sure the next element is a script tag with text/javascript type
            # that element will contain the json for the figure
            script = viz.find_next_sibling('script')
            if script.get('type') != 'text/javascript':
                logger.warning(f"Unexpected next script tag type; skipping")
                continue
            jscript = script.contents

            data = None
            for result in extract_json_objects(jscript[0]):
                if '$schema' in result:
                    data = result
            
            if data is None:
                logger.warning(f"Caught unexpected error while trying to parse JSON. skipping")
                continue

            # json_start_posn = jscript.find('{"$schema"')
            # if json_start_posn == -1:
            #     logger.warning(f"Unexpected javascript in viz element. Can't find the json start. Skipping {jscript}")
            #     continue
            # json_with_trailing = jscript[json_start_posn:]
            # # now parse using a json decoder (which will ignore trailing text automatically)
            # try:
            #     data, end_index = decoder.raw_decode(json_with_trailing)
            # except:
            #     logger.warning(f"Caught unexpected error while trying to parse JSON. skipping {json_with_trailing}")
            #     continue
            # now render the json to an image
            # TODO determine if it's vegalite or vega
            png_data = vlc.vega_to_png(vg_spec=data, scale=2)

            #png_data = vlc.vegalite_to_png(vl_spec=data, scale=2)

            # write the image to disk
            png_relpath = viz_id+".png"
            png_path = os.path.join(os.path.join(os.path.dirname(rootdir), relpath), png_relpath)
            if os.path.exists(png_path):
                logger.error(f"Existing png path! {png_path}")
                continue

            f = create_and_open(png_path, 'wb')
            if f is None:
                continue
            f.write(png_data)

            # modify the soup to load the png
            script.decompose()
            new_img = soup.new_tag("img", src=f"{os.path.join(relpath,png_relpath)}")
            viz.insert_after(new_img)

            # done!

def create_and_open(filepath, mode):
    if os.path.exists(filepath):
        logger.error(f"Existing file! {filepath}")
        return False
    os.makedirs(os.path.dirname(filepath),exist_ok=True)
    return open(filepath, mode)