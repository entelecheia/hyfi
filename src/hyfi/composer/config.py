"""
    HiFY Base Config
"""
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from omegaconf import DictConfig

from hyfi.utils.logging import LOGGING

from .composer import Composer
from .model import BaseModel

logger = LOGGING.getLogger(__name__)


class BaseConfig(BaseModel):
    """
    Base class for all config classes.
    """

    _config_name_: str = "__init__"
    _auto_populate_: bool = True

    verbose: bool = False

    _init_args_: Dict[str, Any] = {}
    _property_set_methods_: Dict[str, str] = {}
    _subconfigs_: Dict[str, Any] = {}

    def __init__(self, **config_kwargs):
        logger.debug(
            "init %s with %s args", self.__class__.__name__, len(config_kwargs)
        )
        super().__init__(**config_kwargs)
        # self.initialize_subconfigs(config_kwargs)
        self._init_args_ = config_kwargs.copy()

    def __setattr__(self, key, val):
        """
        Overrides the default __setattr__ method to allow for custom property set methods.

        Args:
            key (str): The name of the attribute to set.
            val (Any): The value to set the attribute to.
        """
        if method := self._property_set_methods_.get(key):  # type: ignore
            # logger.info(
            #     "Setting %s to %s",
            #     key,
            #     val if isinstance(val, (str, int)) else type(val),
            # )
            getattr(self, method)(val)
        super().__setattr__(key, val)

    # def initialize_subconfigs(self, config_kwargs: Dict[str, Any]):
    #     """
    #     Initializes subconfigs with the given config data.
    #     The function updates the object's dictionary with the given config data,
    #     after excluding any attributes specified in the object's `exclude` list.

    #     Args:
    #         config_kwargs (Dict[str, Any]): The config data to initialize the subconfigs with.

    #     Returns:
    #         None
    #     """
    #     self._subconfigs_ = self._subconfigs_ or {}
    #     for name, config in self._subconfigs_.items():
    #         if name in config_kwargs and isinstance(config_kwargs[name], dict):
    #             cfg = config_kwargs[name]
    #             logger.debug("Initializing subconfig %s with %s", name, cfg)
    #             setattr(self, name, config.model_validate(cfg))

    def export_config(
        self,
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
    ) -> Dict[str, Any]:
        """
        Export the configuration to a dictionary.

        Args:
            exclude (Optional[Union[str, List[str], Set[str], None]]): Keys to exclude from the saved configuration.
                Defaults to None.
            exclude_none (bool): Whether to exclude keys with None values. Defaults to True.
            only_include (Optional[Union[str, List[str], Set[str], None]]): Keys to include in the saved configuration.
                Defaults to None.

        Returns:
            Dict[str, Any]: The configuration dictionary.
        """
        if not exclude:
            exclude = self._exclude_  # type: ignore
        if isinstance(exclude, str):
            exclude = [exclude]
        if exclude is None:
            exclude = []
        if isinstance(only_include, str):
            only_include = [only_include]
        if only_include is None:
            only_include = []

        config = self.model_dump(exclude=exclude, exclude_none=exclude_none)  # type: ignore
        if only_include:
            config = {key: config[key] for key in only_include if key in config}

        return config

    def save_config(
        self,
        filepath: Union[str, Path],
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
    ) -> str:
        """
        Save the batch configuration to file.

        Args:
            filepath ([Union[str, Path]): The filepath to save the configuration to.
            exclude (Optional[Union[str, List[str], Set[str], None]]): Keys to exclude from the saved configuration.
                Defaults to None.
            exclude_none (bool): Whether to exclude keys with None values. Defaults to True.
            only_include (Optional[Union[str, List[str], Set[str], None]]): Keys to include in the saved configuration.
                Defaults to None.

        Returns:
            str: The filename of the saved configuration.
        """
        logger.info("Saving config to %s", filepath)

        config_to_save = self.export_config(
            exclude=exclude, exclude_none=exclude_none, only_include=only_include
        )

        Composer.save(config_to_save, filepath)
        return str(filepath)

    def save_config_as_json(
        self,
        filepath: Union[str, Path],
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
    ) -> str:
        def dumper(obj):
            return Composer.to_dict(obj) if isinstance(obj, DictConfig) else str(obj)

        config_to_save = self.export_config(
            exclude=exclude, exclude_none=exclude_none, only_include=only_include
        )
        logger.info("Saving config to %s", filepath)
        Composer.save_json(config_to_save, filepath, default=dumper)
        return str(filepath)

    def print_config(
        self,
    ):
        Composer.print(self.model_dump())
