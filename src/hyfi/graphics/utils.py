"""Image utils."""
import io
import os
import platform
from pathlib import Path
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rc
from PIL import Image, ImageDraw, ImageFont

from hyfi.utils.iolibs import IOLIBs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class GUTILs:
    """Image utils."""

    @staticmethod
    def get_grid_size(
        num_images: int,
        num_cols: Optional[int] = None,
        num_rows: Optional[int] = None,
        truncate: bool = True,
        fit_to_grid: bool = True,
    ) -> Tuple[int, int, int]:
        """Get number of rows and columns for a grid of images.

        Args:
            num_images (int): Number of images.
            num_cols (int, optional): Number of columns. Defaults to None.
            num_rows (int, optional): Number of rows. Defaults to None.
            truncate (bool, optional): Truncate number of images to fit grid. Defaults to True. If False, the number of images will be increased to fit the grid.

        Returns:
            Tuple[int, int, int]: Number of images, columns and rows.
        """
        if not num_cols and num_images % num_cols != 0 and truncate:
            num_images = (num_images // num_cols) * num_cols
        if not num_cols or num_cols > num_images or num_cols < 1:
            num_cols = num_images // 2
        num_rows = num_images // num_cols

        return num_images, num_cols, num_rows

    @staticmethod
    def scale_image(
        image: Image.Image,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        max_pixels: Optional[int] = None,
        scale: float = 1.0,
        resize_to_multiple_of: Optional[int] = None,
        resample: int = Image.LANCZOS,
    ) -> Image.Image:
        """Scale image to have at most `max_pixels` pixels.

        Args:
            image: PIL image.
            max_width: Maximum width.
            max_height: Maximum height.
            max_pixels: Maximum number of pixels.
            scale: Scale factor.
            resize_to_multiple_of: Resize to multiple of this value.
            resample: Resampling filter.

        Returns:
            PIL image.
        """

        w, h = image.size

        if not max_width and max_height:
            max_width = int(w * max_height / h)
        elif not max_height and max_width:
            max_height = int(h * max_width / w)
        else:
            max_width = max_width or w
            max_height = max_height or h

        if max_width and max_height:
            max_pixels = max_width * max_height

        scale = np.sqrt(max_pixels / (w * h)) if max_pixels > 0 else scale or 1.0
        max_width = int(w * scale)
        max_height = int(h * scale)
        if resize_to_multiple_of:
            max_width = (max_width // resize_to_multiple_of) * resize_to_multiple_of
            max_height = (max_height // resize_to_multiple_of) * resize_to_multiple_of

        if scale < 1.0 or w > max_width or h > max_height:
            image = image.resize((max_width, max_height), resample=resample)  # type: ignore
        return image

    @staticmethod
    def load_image_as_ndarray(
        image_or_uri: Union[str, Path, Image.Image],
    ) -> np.ndarray:
        """Load image from file or URI."""
        return np.asarray(GUTILs.load_image(image_or_uri))

    @staticmethod
    def load_image(
        image_or_uri: Union[str, Path, Image.Image],
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        max_pixels: Optional[int] = None,
        scale: float = 1.0,
        resize_to_multiple_of: Optional[int] = None,
        crop_box: Optional[Tuple[int, int, int, int]] = None,
        mode: str = "RGB",
        **read_kwargs,
    ) -> Image.Image:
        """Load image from file or URI."""
        from PIL import Image

        if isinstance(image_or_uri, Image.Image):
            img = image_or_uri.convert(mode)
        elif Path(image_or_uri).is_file():
            img = Image.open(image_or_uri).convert(mode)
        else:
            img = Image.open(
                io.BytesIO(IOLIBs.read(image_or_uri, **read_kwargs))
            ).convert(mode)
        img = GUTILs.scale_image(
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

    @staticmethod
    def load_images(
        images_or_uris: List[Union[str, Image.Image]],
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        max_pixels: Optional[int] = None,
        scale: float = 1.0,
        resize_to_multiple_of: Optional[int] = None,
        crop_to_min_size: bool = False,
        mode: str = "RGB",
        **kwargs,
    ) -> List[Image.Image]:
        """Load images from files or URIs."""
        imgs = [
            GUTILs.load_image(
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
                min_height = (
                    min_height // resize_to_multiple_of
                ) * resize_to_multiple_of
            imgs = [img.crop((0, 0, min_width, min_height)) for img in imgs]

        return imgs

    @staticmethod
    def get_image_font(
        fontname: Optional[str] = None,
        fontsize: int = 12,
    ) -> Optional[ImageFont.ImageFont]:
        """Get font for PIL image."""
        fontname, fontpath = GUTILs.get_plot_font(
            fontname=fontname,
            set_font_for_matplot=False,
        )
        return ImageFont.truetype(fontpath, fontsize) if fontpath else None

    @staticmethod
    def get_default_system_font(
        fontname: Optional[str] = None,
        fontpath: Optional[str] = None,
        lang: str = "ko",
        verbose: bool = False,
    ) -> Tuple[str, str]:
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
            paths = GUTILs.find_font_file(fontname)
            fontpath = paths[0] if len(paths) > 0 else ""
        if verbose:
            logger.info(f"Font path: {fontpath}")
        return fontname, fontpath

    @staticmethod
    def get_plot_font(
        fontpath: Optional[str] = None,
        fontname: Optional[str] = None,
        lang: str = "en",
        set_font_for_matplot: bool = True,
        verbose: bool = False,
    ) -> Tuple[str, str]:
        """Get font for plot

        Args:
            fontpath: Font file path
            fontname: Font name
            lang: Language
            set_font_for_matplot: Set font for matplot
            verbose: Verbose mode

        Returns:
            Tuple of font name and font path

        """
        if fontname and not fontname.endswith(".ttf"):
            fontname += ".ttf"
        if not fontpath:
            fontname, fontpath = GUTILs.get_default_system_font(
                fontname, fontpath, lang, verbose
            )

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

    @staticmethod
    def find_font_file(query: str) -> List[str]:
        """Find font file by query string"""
        return list(
            filter(
                lambda path: query in os.path.basename(path),
                font_manager.findSystemFonts(),
            )
        )

    @staticmethod
    def convert_figure_to_image(
        fig: plt.Figure,
        dpi: int = 300,
    ):
        """Convert a Matplotlib figure to a PIL Image and return it"""
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", pad_inches=0)
        buf.seek(0)
        return Image.open(buf)

    @staticmethod
    def print_filename_on_image(
        image_or_uri,
        print_filename: bool = False,
        filename: Optional[str] = None,
        filename_offset: Tuple[float, float] = (5, 5),
        fontname: Optional[str] = None,
        fontsize: int = 12,
        fontcolor: Optional[str] = None,
    ) -> Image.Image:
        """
        Convert an image to a PIL Image.

        Args:
            image_or_uri: The image or image URI.
            print_filename: Whether to print the filename on the image.
            filename: The filename to show on the image.
            filename_offset: The offset of the filename from the top left corner.
            fontname: The font name to use for the filename.
            fontsize: The font size to use for the filename.
            fontcolor: The font color to use for the filename.

        Returns:
            The PIL Image.
        """
        img = GUTILs.load_image(image_or_uri)
        if isinstance(image_or_uri, str) and filename is None:
            filename = os.path.basename(image_or_uri)
        if print_filename and filename:
            font = GUTILs.get_image_font(fontname, fontsize)
            draw = ImageDraw.Draw(img)
            draw.text(filename_offset, filename, font=font, fill=fontcolor)

        # img = img.convert("RGB")
        # img = np.array(img)
        return img

    @staticmethod
    def get_ticks_from_lim(
        lim: Tuple[float, float],
        num_ticks: int,
    ) -> np.ndarray:
        """
        Get n evenly spaced ticks from lim.

        Args:
            lim: Tuple of (min, max) values.
            num_ticks: Number of ticks to get.

        Returns:
            Array of ticks.
        """
        ticks = np.linspace(lim[0], lim[1], num_ticks + 1)
        ticks = ticks - (ticks[1] - ticks[0]) / 2
        ticks[0] = lim[0]
        return ticks

    @staticmethod
    def save_adjusted_subplots(
        fig: plt.Figure,
        output_file: str,
        left: float = 0.1,
        right: float = 0.9,
        bottom: float = 0.1,
        top: float = 0.9,
        wspace: float = 0,
        hspace: float = 0,
        tight_layout: bool = True,
        bbox_inches: str = "tight",
        pad_inches: float = 0,
        transparent: bool = True,
        dpi: int = 300,
        verbose: bool = True,
    ):
        """Save subplots after adjusting the figure

        Args:
            fig: Figure
            output_file: Output file path
            left: Left
            right: Right
            bottom: Bottom
            top: Top
            wspace: Wspace
            hspace: Hspace
            tight_layout: Tight layout
            bbox_inches: Bbox inches
            pad_inches: Pad inches
            transparent: Transparent
            dpi: DPI
            verbose: Verbose mode
        """

        # make the figure look better
        fig.subplots_adjust(
            left=left,
            right=right,
            bottom=bottom,
            top=top,
            wspace=wspace,
            hspace=hspace,
        )
        if tight_layout:
            fig.tight_layout()

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            output_file,
            dpi=dpi,
            bbox_inches=bbox_inches,
            pad_inches=pad_inches,
            transparent=transparent,
        )
        if verbose:
            logger.info("Saved subplots to %s", output_file)
