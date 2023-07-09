"""
Graphics functions
"""


class GRAPHICs:
    ###############################
    # Graphics functions
    ###############################
    @staticmethod
    def collage(
        images_or_uris,
        collage_filepath=None,
        ncols=3,
        max_images=12,
        collage_width=1200,
        padding: int = 10,
        bg_color: str = "black",
        crop_to_min_size=False,
        show_filename=False,
        filename_offset=(5, 5),
        fontname=None,
        fontsize=12,
        fontcolor="#000",
        **kwargs,
    ):
        from hyfi.graphics.collage import collage as _collage

        return _collage(
            images_or_uris,
            collage_filepath=collage_filepath,
            ncols=ncols,
            max_images=max_images,
            collage_width=collage_width,
            padding=padding,
            bg_color=bg_color,
            crop_to_min_size=crop_to_min_size,
            show_filename=show_filename,
            filename_offset=filename_offset,
            fontname=fontname,
            fontsize=fontsize,
            fontcolor=fontcolor,
            **kwargs,
        )

    @staticmethod
    def make_gif(
        image_filepaths=None,
        filename_patterns: str = "",
        base_dir: str = "",
        output_filepath: str = "",
        duration: int = 100,
        loop: int = 0,
        width: int = 0,
        optimize: bool = True,
        quality: int = 50,
        show: bool = False,
        force: bool = False,
        **kwargs,
    ):
        from hyfi.graphics.motion import make_gif as _make_gif

        return _make_gif(
            image_filepaths=image_filepaths,
            filename_patterns=filename_patterns,
            base_dir=base_dir,
            output_filepath=output_filepath,
            duration=duration,
            loop=loop,
            width=width,
            optimize=optimize,
            quality=quality,
            show=show,
            force=force,
            **kwargs,
        )

    @staticmethod
    def get_image_font(fontname: str = "", fontsize: int = 12):
        from hyfi.graphics.utils import get_image_font

        return get_image_font(fontname, fontsize)

    @staticmethod
    def load_image(
        image_or_uri,
        max_width: int = 0,
        max_height: int = 0,
        max_pixels: int = 0,
        scale: float = 1.0,
        resize_to_multiple_of: int = 0,
        crop_box=None,
        mode="RGB",
        **kwargs,
    ):
        from hyfi.graphics.utils import load_image

        return load_image(
            image_or_uri,
            max_width,
            max_height,
            max_pixels,
            scale,
            resize_to_multiple_of,
            crop_box,
            mode,
            **kwargs,
        )

    @staticmethod
    def scale_image(
        image,
        max_width: int = 0,
        max_height: int = 0,
        max_pixels: int = 0,
        scale: float = 1.0,
        resize_to_multiple_of: int = 8,
        resample: int = 1,
    ):
        """
        Scale an image to a maximum width, height, or number of pixels.

        resample:   Image.NEAREST (0), Image.LANCZOS (1), Image.BILINEAR (2),
                    Image.BICUBIC (3), Image.BOX (4) or Image.HAMMING (5)
        """
        from hyfi.graphics.utils import scale_image

        return scale_image(
            image,
            max_width,
            max_height,
            max_pixels,
            scale,
            resize_to_multiple_of,
            resample,
        )
