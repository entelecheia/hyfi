import collections.abc
import json
import os
from enum import Enum
from pathlib import Path
from typing import IO, Any, Dict, List, Mapping, Tuple, Union

from omegaconf import DictConfig, ListConfig, OmegaConf, SCMode

from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

DictKeyType = Union[str, int, Enum, float, bool]


class CONFs:
    @staticmethod
    def select(
        cfg: Any,
        key: str,
        default: Any = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
    ):
        """
        Wrapper for OmegaConf. select value from a config object using a key.

        Args:
            cfg: Config node to select from
            key: Key to select
            default: Default value to return if key is not found
            throw_on_resolution_failure: Raise an exception if an interpolation
                resolution error occurs, otherwise return None
            throw_on_missing: Raise an exception if an attempt to select a missing key (with the value '???')
                is made, otherwise return None

        Returns:
            selected value or None if not found.
        """
        key = key.replace("/", ".")
        return OmegaConf.select(
            cfg,
            key=key,
            default=default,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
        )

    @staticmethod
    def to_dict(cfg: Any) -> Any:
        """
        Convert a config to a dict

        Args:
            cfg: The config to convert.

        Returns:
            The dict representation of the config.
        """
        # Convert a config object to a config object.
        if isinstance(cfg, dict):
            cfg = CONFs.to_config(cfg)
        # Returns a container for the given config.
        if isinstance(cfg, (DictConfig, ListConfig)):
            return OmegaConf.to_container(
                cfg,
                resolve=True,
                throw_on_missing=False,
                structured_config_mode=SCMode.DICT,
            )
        return cfg

    @staticmethod
    def to_config(cfg: Any) -> Union[DictConfig, ListConfig]:
        """
        Convert a config object to OmegaConf

        Args:
            cfg: The config to convert.

        Returns:
            A Config object that corresponds to the given config.
        """
        return OmegaConf.create(cfg)

    @staticmethod
    def print(cfg: Any, resolve: bool = True, **kwargs):
        """
        Prints the configuration object in a human-readable format.

        Args:
            cfg (Any): The configuration object to print.
            resolve (bool, optional): Whether to resolve the configuration object before printing. Defaults to True.
            **kwargs: Additional keyword arguments to pass to the pprint.pprint function.

        Returns:
            None
        """
        import pprint

        if CONFs.is_config(cfg):
            if resolve:
                pprint.pprint(CONFs.to_dict(cfg), **kwargs)
            else:
                pprint.pprint(cfg, **kwargs)
        else:
            print(cfg)

    @staticmethod
    def is_config(cfg: Any):
        """
        Determines whether the input object is a valid configuration object.

        Args:
            cfg (Any): The object to check.

        Returns:
            bool: True if the object is a valid configuration object, False otherwise.
        """
        return isinstance(cfg, (DictConfig, dict))

    @staticmethod
    def is_list(cfg: Any):
        """
        Determines whether the input object is a valid list configuration object.

        Args:
            cfg (Any): The object to check.

        Returns:
            bool: True if the object is a valid list configuration object, False otherwise.
        """
        return isinstance(cfg, (ListConfig, list))

    @staticmethod
    def load(file_: Union[str, Path, IO[Any]]) -> Union[DictConfig, ListConfig]:
        """
        Load a configuration file and return a configuration object.

        Args:
            file_ (Union[str, Path, IO[Any]]): The path to the configuration file or a file-like object.

        Returns:
            Union[DictConfig, ListConfig]: The configuration object.
        """
        return OmegaConf.load(file_)

    @staticmethod
    def save(config: Any, f: Union[str, Path, IO[Any]], resolve: bool = False) -> None:
        """
        Save a configuration object to a file.

        Args:
            config (Any): The configuration object to save.
            f (Union[str, Path, IO[Any]]): The path to the file or a file-like object.
            resolve (bool, optional): Whether to resolve the configuration object before saving. Defaults to False.
        """
        os.makedirs(os.path.dirname(str(f)), exist_ok=True)
        OmegaConf.save(config, f, resolve=resolve)

    @staticmethod
    def save_json(
        json_dict: dict,
        f: Union[str, Path, IO[Any]],
        indent=4,
        ensure_ascii=False,
        default=None,
        encoding="utf-8",
        **kwargs,
    ):
        """
        Save a dictionary to a JSON file.

        Args:
            json_dict (dict): The dictionary to save.
            f (Union[str, Path, IO[Any]]): The path to the file or a file-like object.
            indent (int, optional): The number of spaces to use for indentation. Defaults to 4.
            ensure_ascii (bool, optional): Whether to escape non-ASCII characters. Defaults to False.
            default (Any, optional): A function to convert non-serializable objects. Defaults to None.
            encoding (str, optional): The encoding to use. Defaults to "utf-8".
            **kwargs: Additional arguments to pass to json.dump().
        """
        f = str(f)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding=encoding) as f:
            json.dump(
                json_dict,
                f,
                indent=indent,
                ensure_ascii=ensure_ascii,
                default=default,
                **kwargs,
            )

    @staticmethod
    def load_json(f: Union[str, Path, IO[Any]], encoding="utf-8", **kwargs) -> dict:
        """
        Load a JSON file into a dictionary.

        Args:
            f (Union[str, Path, IO[Any]]): The path to the file or a file-like object.
            encoding (str, optional): The encoding to use. Defaults to "utf-8".
            **kwargs: Additional arguments to pass to json.load().

        Returns:
            dict: The dictionary loaded from the JSON file.
        """
        f = str(f)
        with open(f, "r", encoding=encoding) as f:
            return json.load(f, **kwargs)

    @staticmethod
    def update(_dict: Mapping[str, Any], _overrides: Mapping[str, Any]) -> Mapping:
        """
        Update a dictionary with overrides.

        Args:
            _dict (Mapping[str, Any]): The dictionary to update.
            _overrides (Mapping[str, Any]): The dictionary with overrides.

        Returns:
            Mapping: The updated dictionary.
        """
        for k, v in _overrides.items():
            if isinstance(v, collections.abc.Mapping):
                _dict[k] = CONFs.update((_dict.get(k) or {}), v)  # type: ignore
            else:
                _dict[k] = v  # type: ignore
        return _dict

    @staticmethod
    def replace_keys(_dict: Mapping[str, Any], old_key: str, new_key: str) -> Mapping:
        """
        Replace a key in a dictionary.

        Args:
            _dict (Mapping[str, Any]): The dictionary to update.
            old_key (str): The old key to replace.
            new_key (str): The new key to use.

        Returns:
            Mapping: The updated dictionary.
        """
        _new_dict = {}
        for k, v in _dict.items():
            key = new_key if k == old_key else k
            if isinstance(v, collections.abc.Mapping):
                _new_dict[key] = CONFs.replace_keys(v, old_key, new_key)
            else:
                _new_dict[key] = v
        return _new_dict

    @staticmethod
    def merge(
        *configs: Union[
            DictConfig,
            ListConfig,
            Dict[DictKeyType, Any],
            List[Any],
            Tuple[Any, ...],
            Any,
        ],
    ) -> Union[ListConfig, DictConfig]:
        """
        Merge a list of previously created configs into a single one.

        Args:
            *configs: Input configs.

        Returns:
            Union[ListConfig, DictConfig]: The merged config object.
        """
        return OmegaConf.merge(*configs)

    @staticmethod
    def merge_as_dict(
        *configs: Union[
            DictConfig,
            ListConfig,
            Dict[DictKeyType, Any],
            List[Any],
            Tuple[Any, ...],
            Any,
        ],
    ) -> Union[ListConfig, DictConfig]:
        """
        Merge a list of previously created configs into a single dictionary.

        Args:
            *configs: Input configs.

        Returns:
            Union[ListConfig, DictConfig]: The merged config object as a dictionary.
        """
        return CONFs.to_dict(OmegaConf.merge(*configs))

    @staticmethod
    def to_yaml(cfg: Any, resolve: bool = False, sort_keys: bool = False) -> str:
        """
        Convert the input config object to a YAML string.

        Args:
            cfg (Any): The input config object.
            resolve (bool, optional): Whether to resolve the config object before converting it to YAML. Defaults to False.
            sort_keys (bool, optional): Whether to sort the keys in the resulting YAML string. Defaults to False.

        Returns:
            str: The YAML string representation of the input config object.
        """
        if resolve:
            cfg = CONFs.to_dict(cfg)
        return OmegaConf.to_yaml(cfg, resolve=resolve, sort_keys=sort_keys)

    @staticmethod
    def to_container(
        cfg: Any,
        resolve: bool = False,
        throw_on_missing: bool = False,
        enum_to_str: bool = False,
        structured_config_mode: SCMode = SCMode.DICT,
    ):
        """
        Convert the input config object to a nested container (e.g. dictionary).

        Args:
            cfg (Any): The input config object.
            resolve (bool, optional): Whether to resolve the config object before converting it to a container. Defaults to False.
            throw_on_missing (bool, optional): Whether to throw an exception if a missing key is encountered. Defaults to False.
            enum_to_str (bool, optional): Whether to convert enum values to strings. Defaults to False.
            structured_config_mode (SCMode, optional): The structured config mode to use. Defaults to SCMode.DICT.

        Returns:
            The nested container (e.g. dictionary) representation of the input config object.
        """
        return OmegaConf.to_container(
            cfg,
            resolve=resolve,
            throw_on_missing=throw_on_missing,
            enum_to_str=enum_to_str,
            structured_config_mode=structured_config_mode,
        )

    @staticmethod
    def ensure_list(value):
        """
        Ensure that the given value is a list. If the value is None or an empty string, an empty list is returned.
        If the value is already a list, it is returned as is. If the value is a string, it is returned as a list
        containing only that string. Otherwise, the value is converted to a dictionary using the CONF.to_dict method
        and the resulting dictionary is returned as a list.

        Args:
            value (Any): The value to ensure as a list.

        Returns:
            List: The value as a list.
        """
        if not value:
            return []
        elif isinstance(value, str):
            return [value]
        return CONFs.to_dict(value)

    @staticmethod
    def ensure_kwargs(_kwargs, _fn):
        """
        Ensure that the given keyword arguments are valid for the given function.

        Args:
            _kwargs (dict): The keyword arguments to validate.
            _fn (callable): The function to validate the keyword arguments against.

        Returns:
            dict: The valid keyword arguments for the given function.
        """
        from inspect import getfullargspec as getargspec

        if callable(_fn):
            args = getargspec(_fn).args
            logger.info(f"args of {_fn}: {args}")
            return {k: v for k, v in _kwargs.items() if k in args}
        return _kwargs

    @staticmethod
    def pprint(cfg: Any, resolve: bool = True, **kwargs):
        CONFs.print(cfg, resolve=resolve, **kwargs)
