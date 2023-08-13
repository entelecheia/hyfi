"""Collage of images.""" ""
import math
import os
import textwrap
from pathlib import Path
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from hyfi.composer import BaseModel, ConfigDict
from hyfi.utils.logging import LOGGING

from .utils import GUTILs

logger = LOGGING.getLogger(__name__)


class Collage(BaseModel):
    """Collage of images."""

    image: Image.Image
    width: int
    height: int
    ncols: int
    nrows: int
    filepath: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class COLLAGE:
    @staticmethod
    def collage(
        images_or_uris: Union[
            List[Union[str, Path, Image.Image]], str, Path, Image.Image
        ],
        output_file: Optional[Union[str, Path]] = None,
        num_cols: Optional[int] = 3,
        num_images: Optional[int] = 12,
        collage_width: int = 1200,
        padding: int = 10,
        background_color: str = "black",
        crop_to_min_size: bool = False,
        show_filename: bool = False,
        filename_offset: Tuple[int, int] = (5, 5),
        fontname: Optional[str] = None,
        fontsize: int = 12,
        fontcolor: str = "#000",
        **kwargs,
    ) -> Optional[Collage]:
        """
        Create a collage of images.
        """

        if not isinstance(images_or_uris, list):
            images_or_uris = [images_or_uris]
        images_or_uris = [
            uri if isinstance(uri, Image.Image) else str(uri) for uri in images_or_uris
        ]

        if num_images:
            num_images = min(num_images, len(images_or_uris))
        else:
            num_images = len(images_or_uris)
        if num_images < 1:
            raise ValueError("max_images must be greater than 0")
        num_images, num_cols, nrows = GUTILs.get_grid_size(
            num_images, num_cols=num_cols
        )
        logger.info(
            "Creating collage of %d images in %d columns and %d rows",
            num_images,
            num_cols,
            nrows,
        )
        img_width = collage_width // num_cols
        collage_width = num_cols * img_width + padding * (num_cols + 1)

        # load images
        images = GUTILs.load_images(
            images_or_uris[:num_images],
            resize_to_multiple_of=None,
            crop_to_min_size=crop_to_min_size,
            max_width=img_width,
            **kwargs,
        )
        filenames = [
            os.path.basename(image_or_uri) if isinstance(image_or_uri, str) else None
            for image_or_uri in images_or_uris[:num_images]
        ]
        # convert images
        images = [
            GUTILs.print_filename_on_image(
                image,
                print_filename=show_filename,
                filename=filename,
                filename_offset=filename_offset,
                fontname=fontname,
                fontsize=fontsize,
                fontcolor=fontcolor,
            )
            for image, filename in zip(images, filenames)
        ]

        collage = COLLAGE.get_grid_of_images(
            images, num_cols, padding, background_color=background_color
        )
        if output_file:
            output_file = str(output_file)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            collage.image.save(output_file)
            collage.filepath = output_file
            logger.info("Saved collage to %s", output_file)
        return collage

    @staticmethod
    def label_collage(
        collage: Collage,
        collage_filepath=None,
        title: Optional[str] = None,
        title_fontsize: int = 10,
        xlabel=None,
        ylabel=None,
        xticklabels=None,
        yticklabels=None,
        xlabel_fontsize=12,
        ylabel_fontsize=12,
        dpi=100,
        fg_fontcolor="white",
        bg_color="black",
        caption=None,
        **kwargs,
    ) -> Collage:
        """
        Create a collage of images.
        """
        figsize = (collage.width / dpi, collage.height / dpi)
        ncols, nrows = collage.ncols, collage.nrows

        fig = plt.figure(figsize=figsize, dpi=dpi)
        fig.patch.set_facecolor(bg_color)  # type: ignore
        plt.imshow(np.array(collage.image))
        ax = plt.gca()
        plt.grid(False)
        if xlabel is None and ylabel is None:
            plt.axis("off")
        if title is not None:
            title = "\n".join(
                sum(
                    (
                        textwrap.wrap(
                            t, width=int(collage.width / 15 * 12 / title_fontsize)
                        )
                        for t in title.split("\n")
                    ),
                    [],
                )
            )
            ax.set_title(title, fontsize=title_fontsize, color=fg_fontcolor)
        if xlabel is not None:
            # plt.xlabel(xlabel, fontdict={"fontsize": xlabel_fontsize})
            ax.set_xlabel(xlabel, fontsize=xlabel_fontsize, color=fg_fontcolor)
        if ylabel is not None:
            # plt.ylabel(ylabel, fontdict={"fontsize": ylabel_fontsize})
            ax.set_ylabel(ylabel, fontsize=ylabel_fontsize, color=fg_fontcolor)
        if xticklabels is not None:
            # get ncols number of xticks from xlim
            xlim = ax.get_xlim()
            xticks = GUTILs.get_ticks_from_lim(xlim, ncols)
            ax.set_xticks(xticks, color=fg_fontcolor)
            xticklabels = [""] + xticklabels
            ax.set_xticklabels(
                xticklabels, fontsize=xlabel_fontsize, color=fg_fontcolor
            )
        if yticklabels is not None:
            # get nrows number of yticks from ylim
            ylim = ax.get_ylim()
            yticks = GUTILs.get_ticks_from_lim(ylim, nrows)
            ax.set_yticks(yticks, color=fg_fontcolor)
            yticklabels = [""] + yticklabels
            ax.set_yticklabels(
                yticklabels, fontsize=ylabel_fontsize, color=fg_fontcolor
            )

        plt.tight_layout()
        if caption is not None:
            plt.figtext(
                0.5,
                0.01,
                caption,
                wrap=True,
                horizontalalignment="center",
                fontsize=10,
                color=fg_fontcolor,
            )

        img = GUTILs.convert_figure_to_image(fig, dpi=dpi)
        img = GUTILs.scale_image(img, max_width=collage.width)
        plt.close()

        if collage_filepath is not None:
            collage_filepath = str(collage_filepath)
            os.makedirs(os.path.dirname(collage_filepath), exist_ok=True)
            # fig.savefig(collage_filepath, dpi=dpi, bbox_inches="tight", pad_inches=0)
            img.save(collage_filepath)
            # collage_image.save(collage_filepath)
            # log.info(f"Saved collage to {collage_filepath}")

        return Collage(
            image=img,
            filepath=collage_filepath,
            width=img.width,
            height=img.height,
            ncols=ncols,
            nrows=nrows,
        )

    @staticmethod
    def get_grid_of_images(
        images: List[Image.Image],
        num_cols: int = 3,
        padding: int = 10,
        background_color: str = "black",
    ) -> Collage:
        """
        Create a grid of images.
        """
        nrows = len(images) // num_cols
        assert len(images) == nrows * num_cols
        width, height = images[0].size
        grid_width = num_cols * width + padding * (num_cols + 1)
        grid_height = nrows * height + padding * (nrows + 1)
        collage = Image.new(
            "RGB", size=(grid_width, grid_height), color=background_color
        )
        for j, image in enumerate(images):
            x = j % num_cols
            y = j // num_cols
            collage.paste(
                image, (x * width + padding * (x + 1), y * height + padding * (y + 1))
            )
        return Collage(
            image=collage,
            width=grid_width,
            height=grid_height,
            ncols=num_cols,
            nrows=nrows,
        )

    @staticmethod
    def gallery_ndarray_images(
        array: np.ndarray,
        ncols: int = 7,
    ) -> np.ndarray:
        """
        Create a gallery of images from a numpy array.
        """
        nindex, height, width, intensity = array.shape
        nrows = nindex // ncols
        assert nindex == nrows * ncols
        return (
            array.reshape(nrows, ncols, height, width, intensity)
            .swapaxes(1, 2)
            .reshape(height * nrows, width * ncols, intensity)
        )

    @staticmethod
    def make_subplot_pages_from_images(
        images: List[Union[str, Path, np.ndarray, Image.Image]],
        num_images_per_page: int,
        num_cols: int,
        num_rows: Optional[int] = None,
        output_dir: Optional[Union[str, Path]] = None,
        output_file_format: str = "collage_p{page_num}.png",
        titles: Optional[List[str]] = None,
        title_fontsize: int = 10,
        title_color: str = "black",
        figsize: Optional[Tuple[float, float]] = None,
        width_multiple: float = 4,
        height_multiple: float = 2,
        sharex: bool = True,
        sharey: bool = True,
        squeeze: bool = True,
        dpi: int = 100,
        verbose: bool = False,
    ):
        """Make subplot pages from images.

        Args:
            images: List of images to be plotted.
            num_images_per_page: Number of images per page.
            num_cols: Number of columns.
            num_rows: Number of rows. If None, it will be calculated automatically.
            output_dir: Output directory.
            output_file_format: Output file format.
            titles: List of titles for each image.
            title_fontsize: Title fontsize.
            title_color: Title color.
            figsize: Figure size.
            width_multiple: Width multiple.
            height_multiple: Height multiple.
            sharex: Share x-axis.
            sharey: Share y-axis.
            squeeze: Squeeze.
            dpi: Dots per inch.
        """
        num_images = len(images)
        num_pages = math.ceil(num_images / num_images_per_page)
        for page_num in range(num_pages):
            start_idx = page_num * num_images_per_page
            end_idx = start_idx + num_images_per_page
            page_images = images[start_idx:end_idx]
            page_titles = titles[start_idx:end_idx] if titles else None
            page_output_file = (
                Path(output_dir) / output_file_format.format(page_num=page_num)
                if output_dir
                else None
            )
            if verbose:
                logger.info(
                    f"Making page {page_num + 1}/{num_pages} with {len(page_images)} images"
                )
                logger.info(f"Page titles: {page_titles}")
                logger.info(f"Page output file: {page_output_file}")
            COLLAGE.make_subplots_from_images(
                page_images,
                num_cols=num_cols,
                num_rows=num_rows,
                output_file=page_output_file,
                titles=page_titles,
                title_fontsize=title_fontsize,
                title_color=title_color,
                figsize=figsize,
                width_multiple=width_multiple,
                height_multiple=height_multiple,
                sharex=sharex,
                sharey=sharey,
                squeeze=squeeze,
                dpi=dpi,
                verbose=verbose,
            )

    @staticmethod
    def make_subplots_from_images(
        images: List[Union[str, Path, np.ndarray, Image.Image]],
        num_cols: int,
        num_rows: Optional[int] = None,
        output_file: Optional[Union[str, Path]] = None,
        titles: Optional[List[str]] = None,
        title_fontsize: int = 10,
        title_color: str = "black",
        figsize: Optional[Tuple[float, float]] = None,
        width_multiple: float = 4,
        height_multiple: float = 2,
        sharex: bool = True,
        sharey: bool = True,
        squeeze: bool = True,
        dpi: int = 100,
        verbose: bool = False,
    ):
        """Make subplots from images.

        Args:
            images: List of images to be plotted.
            num_cols: Number of columns.
            num_rows: Number of rows. If None, it will be calculated automatically.
            output_file: Output file path.
            titles: List of titles for each image.
            title_fontsize: Title fontsize.
            title_color: Title color.
            figsize: Figure size.
            sharex: Share x-axis or not.
            sharey: Share y-axis or not.
            squeeze: Squeeze or not.
            dpi: Dots per inch.
        """
        if num_rows is None:
            num_images = len(images)
            num_rows = math.ceil(num_images / num_cols)
        if figsize is None:
            figsize = (num_cols * width_multiple, num_rows * height_multiple)
        fig, axes = plt.subplots(
            num_rows,
            num_cols,
            figsize=figsize,
            sharex=sharex,
            sharey=sharey,
            squeeze=squeeze,
        )
        for i in range(num_cols * num_rows):
            ax = (
                axes[i % num_cols]
                if num_rows == 1
                else axes[i // num_cols, i % num_cols]
            )
            if i >= len(images):
                ax.set_visible(False)
                continue
            image = images[i]
            if isinstance(image, (str, Path)):
                image = GUTILs.load_image(image)
            ax.imshow(image)
            if titles:
                ax.set_title(titles[i], fontsize=title_fontsize, color=title_color)
            ax.axis("off")
        if output_file:
            GUTILs.save_adjusted_subplots(fig, output_file, dpi=dpi, verbose=verbose)
