"""
    Configuration for HyFi Pipelines
"""
from typing import Any, Callable, Dict, List, Optional, Union

from hyfi.composer import (
    BaseModel,
    Composer,
    ConfigDict,
    field_validator,
    model_validator,
)
from hyfi.utils.envs import ENVs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BaseRun(BaseModel):
    """Run Configuration"""

    run: Optional[Union[str, Dict[str, Any]]] = {}
    verbose: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        validate_assignment=False,
        alias_generator=Composer.generate_alias_for_special_keys,
    )  # type: ignore

    @model_validator(mode="before")
    def validate_model_config_before(cls, data):
        # logger.debug("Validating model config before validating each field.")
        return Composer.replace_special_keys(Composer.to_dict(data))

    @property
    def run_config(self) -> Dict[str, Any]:
        if self.run and isinstance(self.run, str):
            return {"_target_": self.run}
        return Composer.to_dict(self.run) or {}

    @property
    def run_target(self) -> str:
        return self.run_config.get("_target_") or ""

    @property
    def run_kwargs(self) -> Dict[str, Any]:
        _kwargs = self.run_config.copy()
        _kwargs.pop("_target_", None)
        _kwargs.pop("_partial_", None)
        return _kwargs


class Running(BaseRun):
    """Running Configuration"""

    uses: str = ""


RunningSteps = List[Running]
RunningPipelines = List[Running]
RunningTasks = List[Running]
RunningCalls = List[Running]


class Pipe(BaseRun):
    """Pipe Configuration"""

    pipe_target: str = ""
    name: Optional[str] = ""
    desc: Optional[str] = ""
    env: Optional[Dict[str, Any]] = {}
    use_pipe_obj: bool = True
    pipe_obj_arg_name: Optional[str] = ""
    return_pipe_obj: bool = False
    # task: Optional[TaskConfig] = None

    def set_enviroment(self):
        if self.env:
            ENVs.check_and_set_osenv_vars(self.env)

    def get_pipe_func(self) -> Optional[Callable]:
        if self.pipe_target.startswith("lambda"):
            raise NotImplementedError("Lambda functions are not supported. (dangerous)")
            # return eval(self.pipe_target)
        elif self.pipe_target:
            return Composer.partial(self.pipe_target)
        else:
            return None

    def get_run_func(self) -> Optional[Callable]:
        run_cfg = self.run_config
        run_target = self.run_target
        if run_target and run_target.startswith("lambda"):
            raise NotImplementedError("Lambda functions are not supported. (dangerous)")
            # return eval(run_target)
        elif run_cfg:
            if self.pipe_obj_arg_name:
                run_cfg.pop(self.pipe_obj_arg_name)
            logger.info(
                "Returning partial function: %s with kwargs: %s", run_target, run_cfg
            )
            return Composer.partial(run_cfg)
        else:
            logger.warning("No function found for %s", self)
            return None


class DataframePipe(Pipe):
    columns_to_apply: Optional[Union[str, List[str]]] = []
    use_batcher: bool = True
    num_workers: int = 1

    @model_validator(mode="before")
    def _check_and_set_values(cls, data):
        num_workers = data.get("num_workers")
        if num_workers and num_workers > 1:
            data["use_batcher"] = True
        return data

    @property
    def columns(self) -> List[str]:
        if not self.columns_to_apply:
            return []
        return (
            [self.columns_to_apply]
            if isinstance(self.columns_to_apply, str)
            else self.columns_to_apply
        )


Pipes = List[Pipe]


class Pipeline(BaseRun):
    """Pipeline Configuration"""

    name: Optional[str] = ""
    steps: Optional[List[Union[str, Dict]]] = []
    initial_object: Optional[Any] = None
    use_task_as_initial_object: bool = False

    @field_validator("steps", mode="before")
    def steps_to_list(cls, v):
        """
        Convert a list of steps to a list

        Args:
            cls: class to use for conversion
            v: list of steps to convert

        Returns:
            list of steps converted to
        """
        return [v] if isinstance(v, str) else Composer.to_dict(v)

    def update_configs(
        self,
        rc: Union[Dict, Running],
    ):
        """
        Update running config with values from another config

        Args:
            rc: RunningConfig to update from
        """
        # If rc is a dict or dict it will be converted to RunningConfig.
        if isinstance(rc, dict):
            rc = Running(**rc)
        self.name = rc.name or self.name
        self.desc = rc.desc or self.desc

    def get_pipes(self) -> Pipes:
        """
        Get all pipes that this task is aware of

        Args:
            task: The task to use for the pipe

        Returns:
            A list of : class : `PipeConfig` objects
        """
        pipes: Pipes = []
        self.steps = self.steps or []
        # Add pipes to the pipeline.
        for rc in get_running_configs(self.steps):
            # Add a pipe to the pipeline.
            config = getattr(self, rc.uses, None)
            if isinstance(config, dict):
                pipe = Pipe(**Composer.update(config, rc.model_dump()))
                # Set the task to be used for the pipe.
                # if task is not None:
                #     pipe.task = task
                pipes.append(pipe)
        return pipes


Pipelines = List[Pipeline]


def get_running_configs(steps: list) -> List[Running]:
    """
    Parses and returns list of running configs

    Args:
        steps: list of config to parse

    Returns:
        list of : class : `RunningConfig` objects
    """
    RCs: List[Running] = []
    # Return the list of running RCs
    if not steps:
        logger.warning("No running configs provided")
        return RCs
    # Add running config to the list of running configs.
    for rc in steps:
        # Append a running config to the RCs list.
        if isinstance(rc, str):
            RCs.append(Running(uses=rc))
        elif isinstance(rc, dict):
            RCs.append(Running(**rc))
        else:
            raise ValueError(f"Invalid running config: {rc}")
    return RCs


def run_pipe(
    obj: Any,
    config: Union[Dict, Pipe],
) -> Any:
    """
    Run a pipe on an object

    Args:
        obj: The object to pipe on
        config: The configuration for the pipe

    Returns:
        The result of the pipe
    """
    # Create a PipeConfig object if not already a PipeConfig.
    if not isinstance(config, Pipe):
        config = Pipe(**Composer.to_dict(config))
    pipe_fn = config.get_pipe_func()
    # Return the object that is being used to execute the pipe function.
    if pipe_fn is None:
        logger.warning("No pipe function specified")
        return obj
    # Run a pipe with the pipe_fn
    if config.verbose:
        logger.info("Running a pipe with %s", config.pipe_target)
    # Apply pipe function to each object.
    if isinstance(obj, dict):
        objs = {}
        # Apply pipe to each object.
        for no, name in enumerate(obj):
            obj_ = obj[name]

            # Apply pipe to an object.
            if config.verbose:
                logger.info(
                    "Applying pipe to an object [%s], %d/%d",
                    name,
                    no + 1,
                    len(obj),
                )

            objs[name] = pipe_fn(obj_, config)
        return objs

    return pipe_fn(obj, config)
