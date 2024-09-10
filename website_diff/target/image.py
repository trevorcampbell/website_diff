from PIL import Image, ImageEnhance, ImageChops, ImageOps
import numpy as np
from loguru import logger
import os

def diff(filepath_old, filepath_new, filepath_out):
    if not _img_exists(filepath_old, filepath_new):
        return False

    img_old = Image.open(filepath_old).convert("RGB")
    img_new = Image.open(filepath_new).convert("RGB")
    img_diff = ImageChops.difference(img_old, img_new)
    if img_diff.getbbox() is None:
        # no diff, just save img_new to filepath_out
        img_new.save(filepath_out)
        return False
    else:
        # diff, add a yellow border and highlight differences in bright red
        img_overlay = ImageChops.overlay(img_old.convert("RGBA"), img_new.convert("RGBA"))
        img_overlay_np = np.array(img_overlay)
        img_overlay_np[ np.fabs(np.array(img_diff)).sum(axis=2) != 0 ] = np.array([255,0,0,0])
        img_overlay = Image.fromarray(img_overlay_np)
        img_bordered = ImageOps.expand(img_overlay, border=10, fill='yellow')
        img_bordered.convert("RGB").save(filepath_out)
        return True


def _img_exists(filepath_old, filepath_new):
    result=True
    if not os.path.isfile(filepath_old):
        logger.info(f"{filepath_old} is missing")
        result=False
    elif not os.path.isfile(filepath_new):
        logger.info(f"{filepath_new} is missing")
        result=False
    return result

def highlight_add(filepath, filepath_out):
    _highlight_image(filepath, filepath_out, "limegreen", 0.5)

def highlight_del(filepath, filepath_out):
    _highlight_image(filepath, filepath_out, "firebrick", 0.5)

def _highlight_image(filepath, filepath_out, color, alpha):
    img = Image.open(filepath)
    bw = img.convert("LA").convert("RGBA")
    overlay = Image.new("RGBA", img.size, color = color)
    blended = Image.blend(bw, overlay, alpha)
    blended.convert("RGB").save(filepath_out)
