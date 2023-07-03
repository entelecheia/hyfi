"""Image utils."""
import io
import os
import platform
from pathlib import Path
from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rc
from PIL import Image, ImageFont

from hyfi.utils.iolibs import IOLIBs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


def scale_image(
    image: Image.Image,
    max_width: Optional[int] = 0,
    max_height: Optional[int] = 0,
    max_pixels: Optional[int] = 0,
    scale: Optional[float] = 1.0,
    resize_to_multiple_of: Optional[int] = 0,
    resample: int = Image.LANCZOS,
) -> Image.Image:
    """Scale image to have at most `max_pixels` pixels."""
    if resize_to_multiple_of is None:
        resize_to_multiple_of = 0

    w, h = image.size

    max_width = max_width or 0
    max_height = max_height or 0
    max_pixels = max_pixels or 0
    if max_width <= 0 and max_height > 0:
        max_width = int(w * max_height / h)
    elif max_height <= 0 and max_width > 0:
        max_height = int(h * max_width / w)

    if max_width > 0 and max_height > 0:
        max_pixels = max_width * max_height

    scale = np.sqrt(max_pixels / (w * h)) if max_pixels > 0 else scale or 1.0
    max_width = int(w * scale)
    max_height = int(h * scale)
    if resize_to_multiple_of > 0:
        max_width = (max_width // resize_to_multiple_of) * resize_to_multiple_of
        max_height = (max_height // resize_to_multiple_of) * resize_to_multiple_of

    if scale < 1.0 or w > max_width or h > max_height:
        image = image.resize((max_width, max_height), resample=resample)  # type: ignore
    return image


def load_image(
    image_or_uri: Union[str, Image.Image],
    max_width: Optional[int] = 0,
    max_height: Optional[int] = 0,
    max_pixels: Optional[int] = 0,
    scale: Optional[float] = 1.0,
    resize_to_multiple_of: Optional[int] = 0,
    crop_box=None,
    mode="RGB",
    **kwargs,
) -> Image.Image:
    """Load image from file or URI."""
    from PIL import Image

    if max_width is None:
        max_width = 0
    if max_height is None:
        max_height = 0
    if max_pixels is None:
        max_pixels = 0
    if isinstance(image_or_uri, Image.Image):
        img = image_or_uri.convert(mode)
    elif Path(image_or_uri).is_file():
        img = Image.open(image_or_uri).convert(mode)
    else:
        img = Image.open(io.BytesIO(IOLIBs.read(image_or_uri, **kwargs))).convert(mode)
    img = scale_image(
        img,
        max_width=max_width,
        max_height=max_height,
        max_pixels=max_pixels,
        scale=scale,
        resize_to_multiple_of=resize_to_multiple_of,
    )
    if crop_box is not None:
        img = img.crop(crop_box)
    return img


def load_images(
    images_or_uris: List[Union[str, Image.Image]],
    max_width: Optional[int] = 0,
    max_height: Optional[int] = 0,
    max_pixels: Optional[int] = 0,
    scale: Optional[float] = 1.0,
    resize_to_multiple_of: Optional[int] = 0,
    crop_to_min_size: bool = False,
    mode: str = "RGB",
    **kwargs,
) -> List[Image.Image]:
    """Load images from files or URIs."""
    imgs = [
        load_image(
            image_or_uri,
            max_width=max_width,
            max_height=max_height,
            max_pixels=max_pixels,
            scale=scale,
            resize_to_multiple_of=resize_to_multiple_of,
            mode=mode,
            **kwargs,
        )
        for image_or_uri in images_or_uris
    ]
    if crop_to_min_size:
        min_width = min(img.width for img in imgs)
        min_height = min(img.height for img in imgs)
        if resize_to_multiple_of is not None:
            min_width = (min_width // resize_to_multiple_of) * resize_to_multiple_of
            min_height = (min_height // resize_to_multiple_of) * resize_to_multiple_of
        imgs = [img.crop((0, 0, min_width, min_height)) for img in imgs]

    return imgs


def get_image_font(
    fontname: Optional[str] = None,
    fontsize: int = 12,
    lang: str = "en",
):
    """Get font for PIL image."""
    fontname, fontpath = get_plot_font(set_font_for_matplot=False, fontname=fontname)
    return ImageFont.truetype(fontpath, fontsize) if fontpath else None


def get_default_system_font(
    fontname: Optional[str] = None,
    fontpath: Optional[str] = None,
    lang: str = "ko",
    verbose: bool = False,
):
    if platform.system() == "Darwin":
        default_fontname = "AppleGothic.ttf" if lang == "ko" else "Arial.ttf"
        fontname = fontname or default_fontname
        fontpath = os.path.join("/System/Library/Fonts/Supplemental/", fontname)
    elif platform.system() == "Windows":
        default_fontname = "malgun.ttf" if lang == "ko" else "arial.ttf"
        fontname = fontname or default_fontname
        fontpath = os.path.join("c:/Windows/Fonts/", fontname)
    elif platform.system() == "Linux":
        default_fontname = "NanumGothic.ttf" if lang == "ko" else "DejaVuSans.ttf"
        fontname = fontname or default_fontname
        if fontname.lower().startswith("nanum"):
            fontpath = os.path.join("/usr/share/fonts/truetype/nanum/", fontname)
        else:
            fontpath = os.path.join("/usr/share/fonts/truetype/", fontname)
    if fontpath and not Path(fontpath).is_file():
        paths = find_font_file(fontname)
        fontpath = paths[0] if len(paths) > 0 else ""
    if verbose:
        logger.info(f"Font path: {fontpath}")
    return fontname, fontpath


def get_plot_font(
    set_font_for_matplot: bool = True,
    fontpath: Optional[str] = None,
    fontname: Optional[str] = None,
    lang: str = "en",
    verbose: bool = False,
):
    """Get font for plot"""
    if fontname and not fontname.endswith(".ttf"):
        fontname += ".ttf"
    if not fontpath:
        fontname, fontpath = get_default_system_font(fontname, fontpath, lang, verbose)

    if fontpath and Path(fontpath).is_file():
        font_manager.fontManager.addfont(fontpath)
        fontname = font_manager.FontProperties(fname=fontpath).get_name()  # type: ignore

        if set_font_for_matplot and fontname:
            rc("font", family=fontname)
            plt.rcParams["axes.unicode_minus"] = False
            if verbose:
                font_family = plt.rcParams["font.family"]
                logger.info(f"font family: {font_family}")
        if verbose:
            logger.info(f"font name: {fontname}")
    else:
        logger.warning(f"Font file does not exist at {fontpath}")
        fontname = ""
        fontpath = ""
        if platform.system() == "Linux":
            font_install_help = """
            apt install fontconfig
            apt install fonts-nanum
            fc-list | grep -i nanum
            """
            print(font_install_help)
    return fontname, fontpath


def find_font_file(query):
    """Find font file by query string"""
    return list(
        filter(
            lambda path: query in os.path.basename(path),
            font_manager.findSystemFonts(),
        )
    )
