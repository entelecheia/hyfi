"""
    Configuration for function calls.
"""
from pathlib import Path
from typing import Any, Dict, Optional

from hyfi.composer import BaseModel, Composer
from hyfi.core import global_hyfi
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class Run(BaseModel):
    """Run Configuration"""

    _config_group_: str = "/run"
    _auto_populate_ = True
    _target_: Optional[str] = None
    _partial_: bool = True

    @property
    def config(self) -> Dict[str, Any]:
        return {
            k: v
            for k, v in self.model_extra.items()
            if not k.startswith("_") or k in ["_target_", "_partial_"]
        }

    @property
    def kwargs(self) -> Dict[str, Any]:
        return {k: v for k, v in self.model_extra.items() if not k.startswith("_")}

    @property
    def target(self) -> str:
        return self._target_

    def generate_config(
        self,
        config_name: Optional[str] = None,
        config_path: str = None,
        config_root: Optional[str] = None,
        save: bool = True,
    ) -> Dict[str, Any]:
        """
        Saves a HyFI config for itself.

        Args:
            config_name (Optional[str]): The name of the config. If not provided, the name of the target will be used.
            config_path (Optional[str]): The path to save the config to (relative to the config root). Defaults to "run".
            config_root (Optional[str]): The root of the config path. If not provided, the global hyfi config directory will be used.
            **kwargs_for_target: Keyword arguments to pass to the target.
        """
        # if self.target is None:
        #     raise ValueError("Cannot generate config for RunConfig without a target.")

        cfg = self.sanitized_config(self.config)

        if not save:
            return cfg

        config_name = config_name or self._config_name_ or self._target_.split(".")[-1]
        filename = f"{config_name}.yaml"
        config_root = config_root or global_hyfi.config_root
        _config_group_ = self._config_group_
        if _config_group_ and _config_group_.startswith("/"):
            _config_group_ = _config_group_[1:]
        config_path = config_path or _config_group_ or "test"
        config_path = Path(config_root) / config_path
        config_path.mkdir(parents=True, exist_ok=True)
        config_path /= filename
        Composer.save(cfg, config_path)
        logger.info("Saved HyFI config for %s to %s.", self._target_, config_path)
        return cfg
