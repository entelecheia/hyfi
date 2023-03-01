"""Google Colab utilities."""
import os

from .env import set_osenv
from .logging import getLogger

logger = getLogger(__name__)


def mount_google_drive(
    workspace: str = None,
    project: str = None,
    mountpoint: str = "/content/drive",
    force_remount: bool = False,
    timeout_ms: int = 120000,
) -> None:
    """Mount Google Drive to Colab."""
    try:
        from google.colab import drive

        drive.mount(mountpoint, force_remount=force_remount, timeout_ms=timeout_ms)

        if isinstance(workspace, str):
            if not workspace.startswith(os.path.sep) and not workspace.startswith(".."):
                workspace = os.path.join(mountpoint, workspace)
            set_osenv("HYFI_WORKSPACE_ROOT", workspace)
            logger.info(f"Setting HYFI_WORKSPACE_ROOT to {workspace}")
        if isinstance(project, str):
            set_osenv("HYFI_PROJECT_NAME", project)
            logger.info(f"Setting HYFI_PROJECT_NAME to {project}")
    except ImportError:
        logger.warning("Google Colab not detected.")
