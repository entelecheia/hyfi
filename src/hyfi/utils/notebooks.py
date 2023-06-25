"""Utilities for working with notebooks.""" ""
import contextlib
import logging
import os
import sys

from hyfi.utils.envs import ENVs
from hyfi.utils.iolibs import IOLIBs

logger = logging.getLogger(__name__)


class NBs:
    @staticmethod
    def is_notebook():
        """Check if the code is running in a notebook."""
        try:
            get_ipython  # type: ignore
        except NameError:
            return False
        # pylint: disable=undefined-variable
        shell_type = get_ipython().__class__.__name__  # type: ignore # noqa
        # logger.info(f"shell type: {shell_type}")
        return shell_type in ["ZMQInteractiveShell", "Shell"]

    @staticmethod
    def is_colab():
        """Check if the code is running in Google Colab."""
        is_colab = "google.colab" in sys.modules
        if is_colab:
            logger.info("Google Colab detected.")
        else:
            logger.info("Google Colab not detected.")
        return is_colab

    @staticmethod
    def get_display():
        """Get the display object for the current environment."""
        try:
            from ipywidgets import Output
        except ImportError:
            logger.info("ipywidgets not installed.")
            return None

        return Output() if NBs.is_notebook() else None

    @staticmethod
    def clear_output(wait=False):
        """Clear the output of the current notebook."""
        from IPython import display

        if NBs.is_notebook():
            display.clear_output(wait=wait)

    @staticmethod
    def display(
        *objs,
        include=None,
        exclude=None,
        metadata=None,
        transient=None,
        display_id=None,
        **kwargs,
    ):
        """Display an object in the current notebook."""
        from IPython import display

        if NBs.is_notebook() and objs is not None:
            return display.display(
                *objs,
                include=include,
                exclude=exclude,
                metadata=metadata,
                transient=transient,
                display_id=display_id,
                **kwargs,
            )

    @staticmethod
    def display_image(
        data=None,
        url=None,
        filename=None,
        format=None,
        embed=None,
        width=None,
        height=None,
        retina=False,
        unconfined=False,
        metadata=None,
        **kwargs,
    ):
        """
        Display an image, which can be given as raw data or a URL.

        Parameters
        ----------
        data : unicode, str or bytes
            The raw image data or a URL or filename to load the data from.
            This always results in embedded image data.
        url : unicode
            A URL to download the data from. If you specify `url=`,
            the image data will not be embedded unless you also specify `embed=True`.
        filename : unicode
            Path to a local file to load the data from.
            Images from a file are always embedded.
        format : unicode
            The format of the image data (png/jpeg/jpg/gif). If a filename or URL is given
            for format will be inferred from the filename extension.
        embed : bool
            Should the image data be embedded using a data URI (True) or be
            loaded using an <img> tag. Set this to True if you want the image
            to be viewable later with no internet connection in the notebook.

            Default is `True`, unless the keyword argument `url` is set, then
            default value is `False`.

            Note that QtConsole is not able to display images if `embed` is set to `False`
        width : int
            Width in pixels to which to constrain the image in html
        height : int
            Height in pixels to which to constrain the image in html
        retina : bool
            Automatically set the width and height to half of the measured
            width and height.
            This only works for embedded images because it reads the width/height
            from image data.
            For non-embedded images, you can just set the desired display width
            and height directly.
        unconfined: bool
            Set unconfined=True to disable max-width confinement of the image.
        metadata: dict
            Specify extra metadata to attach to the image.

        """
        from IPython import display

        if NBs.is_notebook():
            img = display.Image(
                data=data,
                url=url,
                filename=filename,
                format=format,
                embed=embed,
                width=width,
                height=height,
                retina=retina,
                unconfined=unconfined,
                metadata=metadata,
                **kwargs,
            )
            return display.display(img)

    @staticmethod
    def hide_code_in_slideshow():
        """Hide code in slideshow."""
        import binascii

        from IPython import display

        uid = binascii.hexlify(os.urandom(8)).decode()
        html = """<div id="%s"></div>
        <script type="text/javascript">
            $(function(){
                var p = $("#%s");
                if (p.length==0) return;
                while (!p.hasClass("cell")) {
                    p=p.parent();
                    if (p.prop("tagName") =="body") return;
                }
                var cell = p;
                cell.find(".input").addClass("hide-in-slideshow")
            });
        </script>""" % (
            uid,
            uid,
        )
        display.display_html(html, raw=True)

    @staticmethod
    def colored_str(s, color="black"):
        """Colored string."""
        # return "<text style=color:{}>{}</text>".format(color, s)
        return "<text style=color:{}>{}</text>".format(color, s.replace("\n", "<br>"))

    @staticmethod
    def cprint(str_tuples):
        from IPython.core.display import HTML as html_print
        from IPython.display import display

        display(
            html_print(
                " ".join([NBs.colored_str(ti, color=ci) for ti, ci in str_tuples])
            )
        )

    @staticmethod
    def create_dropdown(
        options, value, description, disabled=False, style=None, layout=None, **kwargs
    ):
        """Create a dropdown widget."""
        import ipywidgets as widgets

        if style is None:
            style = {"description_width": "initial"}

        layout = (
            widgets.Layout(width="auto") if layout is None else widgets.Layout(**layout)
        )
        return widgets.Dropdown(
            options=options,
            value=value,
            description=description,
            disabled=disabled,
            style=style,
            layout=layout,
            **kwargs,
        )

    @staticmethod
    def create_textarea(
        value,
        description,
        placeholder="",
        disabled=False,
        style=None,
        layout=None,
        **kwargs,
    ):
        """Create a textarea widget."""
        import ipywidgets as widgets

        if style is None:
            style = {"description_width": "initial"}

        layout = (
            widgets.Layout(width="auto") if layout is None else widgets.Layout(**layout)
        )
        return widgets.Textarea(
            value=value,
            placeholder=placeholder,
            description=description,
            disabled=disabled,
            style=style,
            layout=layout,
            **kwargs,
        )

    @staticmethod
    def create_button(
        description, button_style="", icon="check", layout=None, **kwargs
    ):
        """Create a button widget."""
        import ipywidgets as widgets

        layout = (
            widgets.Layout(width="auto") if layout is None else widgets.Layout(**layout)
        )
        return widgets.Button(
            description=description,
            button_style=button_style,
            icon=icon,
            layout=layout,
            **kwargs,
        )

    @staticmethod
    def create_radiobutton(
        options,
        description,
        value=None,
        disabled=False,
        style=None,
        layout=None,
        **kwargs,
    ):
        """Create a radiobutton widget."""
        import ipywidgets as widgets

        if style is None:
            style = {"description_width": "initial"}

        layout = (
            widgets.Layout(width="auto") if layout is None else widgets.Layout(**layout)
        )
        return widgets.RadioButtons(
            options=options,
            value=value,
            description=description,
            disabled=disabled,
            style=style,
            layout=layout,
            **kwargs,
        )

    @staticmethod
    def create_image(
        filename=None,
        format=None,
        width=None,
        height=None,
        **kwargs,
    ):
        """Create an image widget."""
        import ipywidgets as widgets

        # from urllib.request import urlopen

        if filename is None:
            url = "https://assets.entelecheia.cc/img/placeholder.png"
            # img = urlopen(url).read()
            img = IOLIBs.read(url)
            _format = "png"
        else:
            img = IOLIBs.read(filename)
            _format = format or filename.split(".")[-1]
        return widgets.Image(
            value=img,
            format=_format,
            width=width,
            height=height,
            **kwargs,
        )

    @staticmethod
    def create_floatslider(
        min=0.0,
        max=1.0,
        step=0.1,
        value=None,
        description="",
        disabled=False,
        continuous_update=False,
        orientation="horizontal",
        readout=True,
        readout_format=".1f",
        style=None,
        layout=None,
        **kwargs,
    ):
        """Create a float slider widget."""
        if style is None:
            style = {"description_width": "initial"}
        import ipywidgets as widgets

        layout = (
            widgets.Layout(width="auto") if layout is None else widgets.Layout(**layout)
        )
        return widgets.FloatSlider(
            min=min,
            max=max,
            step=step,
            value=value,
            description=description,
            disabled=disabled,
            continuous_update=continuous_update,
            orientation=orientation,
            readout=readout,
            readout_format=readout_format,
            style=style,
            layout=layout,
            **kwargs,
        )

    @staticmethod
    def load_extentions(exts=None):
        """Load extentions."""
        if exts is None:
            exts = ["autotime"]
        if not NBs.is_notebook():
            return
        with contextlib.suppress(ImportError):
            from IPython.core.getipython import get_ipython

            ip = get_ipython()
            if ip is None:
                return
            try:
                loaded = ip.extension_manager.loaded
                for ext in exts:
                    if ext not in loaded:
                        ip.extentension_manager.load_extension(ext)
            except AttributeError:
                for ext in exts:
                    try:
                        ip.magic(f"load_ext {ext}")
                    except ModuleNotFoundError:
                        logger.info("Extension %s not found. Install it first.", ext)

    @staticmethod
    def set_matplotlib_formats(*formats, **kwargs):
        """Set matplotlib formats."""
        if NBs.is_notebook():
            from IPython.core.display import set_matplotlib_formats

            set_matplotlib_formats(*formats, **kwargs)

    @staticmethod
    def mount_google_drive(
        project_root: str = "",
        project_name: str = "",
        mountpoint: str = "/content/drive",
        force_remount: bool = False,
        timeout_ms: int = 120000,
    ) -> None:
        """Mount Google Drive to Colab."""
        try:
            from google.colab import drive  # type: ignore

            drive.mount(mountpoint, force_remount=force_remount, timeout_ms=timeout_ms)

            if project_root:
                if not project_root.startswith(
                    os.path.sep
                ) and not project_root.startswith(".."):
                    project_root = os.path.join(mountpoint, project_root)
                ENVs.set_osenv("HYFI_PROJECT_ROOT", project_root)
                logger.info(f"Setting HYFI_PROJECT_ROOT to {project_root}")
            if project_name:
                ENVs.set_osenv("HYFI_PROJECT_NAME", project_name)
                logger.info(f"Setting HYFI_PROJECT_NAME to {project_name}")
        except ImportError:
            logger.warning("Google Colab not detected.")
