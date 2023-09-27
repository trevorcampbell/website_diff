from PIL import Image, ImageEnhance, ImageChops, ImageOps

def diff(filepath_old, filepath_new, filepath_out):
    img_old = Image.open(filepath_old)
    img_new = Image.open(filepath_new)
    img_diff = ImageChops.difference(img_old, img_new)
    if img_diff.getbbox() is None:
        # no diff, just save img_new to filepath_out
        img_new.save(filepath_out)
        return False
    else:
        # diff, add a yellow border and highlight differences in bright red
        img_overlay = ImageChops.overlay(img_old, img_new)
        for i in range(img_overlay.size[0]):
            for j in range(img_overlay.size[1]):
                if img_diff[i,j] != (0,0,0):
                    img_overlay[i,j] = (255,0,0)
        img_bordered = ImageOps.expand(img_overlay, border=10, fill='yellow')
        img_bordered.save(filepath_out)
        return True

def highlight_add(filepath, filepath_out):
    _highlight_image(filepath, filepath_out, "limegreen", 0.5)

def highlight_del(filepath, filepath_out):
    _highlight_image(filepath, filepath_out, "firebrick", 0.5)

def _highlight_image(filepath, filepath_out, color, alpha):
    img = Image.open(filepath)
    bw = ImageEnhance.Color(img).enhance(0.0)
    overlay = Image.new("RGBA", img.size, color = color)
    blended = Image.blend(bw, overlay, alpha)
    blended.save(filepath_out)
