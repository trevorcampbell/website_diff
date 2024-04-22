import vl_convert as vlc
from json import JSONDecoder
from loguru import logger
from bs4 import BeautifulSoup


def render(rootdir, relpath, soup, selector):
    for root_elem in soup.select_all(selector):
        for viz in root_elem.select_all('.vega-embed'):
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
            jscript = script.content
            json_start_posn = jscript.find('{"$schema"')
            if json_start_posn == -1:
                logger.warning(f"Unexpected javascript in viz element. Can't find the json start. Skipping {jscript}")
                continue
            json_with_trailing = jscript[json_start_posn:]
            # now parse using a json decoder (which will ignore trailing text automatically)
            try:
                data, end_index = decoder.raw_decode(json_with_trailing)
            except:
                logger.warning(f"Caught unexpected error while trying to parse JSON. skipping {json_with_trailing}")
                continue
            # now render the json to an image
            # TODO determine if it's vegalite or vega
            png_data = vlc.vega_to_png(vg_spec=data, scale=2)
            #png_data = vlc.vegalite_to_png(vl_spec=data, scale=2)

            # write the image to disk
            png_relpath = viz_id+".png"
            png_path = os.path.join(os.path.dirname(os.path.join(rootdir, relpath)), png_relpath)
            if os.path.exists(png_path):
                logger.error(f"Existing png path! {png_path}")
                continue
            with open(png_path, "w") as f:
                f.write(png_data)

            # modify the soup to load the png
            script.decompose()
            new_img = soup.new_tag("img", src=f"{png_relpath}")
            viz.replace_with(new_img)

            # done!