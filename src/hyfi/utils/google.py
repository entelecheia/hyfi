"""Google Colab utilities."""
import os

from hyfi.utils.env import set_osenv
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


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
            if not project_root.startswith(os.path.sep) and not project_root.startswith(
                ".."
            ):
                project_root = os.path.join(mountpoint, project_root)
            set_osenv("HYFI_PROJECT_ROOT", project_root)
            logger.info(f"Setting HYFI_PROJECT_ROOT to {project_root}")
        if project_name:
            set_osenv("HYFI_PROJECT_NAME", project_name)
            logger.info(f"Setting HYFI_PROJECT_NAME to {project_name}")
    except ImportError:
        logger.warning("Google Colab not detected.")
