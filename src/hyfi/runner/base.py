from typing import Dict, List, Optional, Union

from hyfi.pipeline.config import RunningCalls, RunningConfig, get_running_configs
from hyfi.run import RunConfig
from hyfi.task import TaskConfig
from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BaseRunner(TaskConfig):
    _config_group_: str = "/runner"
    _config_name_: str = "__init__"

    calls: Optional[List[Union[str, Dict]]] = []

    def __call__(self) -> None:
        self.run()

    def run(self):
        self.run_calls()

    def get_running_calls(self) -> RunningCalls:
        return get_running_configs(self.calls or [])

    def run_call(self, rc: RunningConfig) -> None:
        method_ = getattr(self, rc.uses, None)
        if method_ and callable(method_):
            method_(**rc.run_kwargs)

    def run_calls(self):
        """
        Run the calls specified in the runner
        """
        calls = self.get_running_calls()
        if self.verbose:
            logger.info("Running %s call(s)", len(calls))
        # Run all tasks in the workflow.
        with elapsed_timer(format_time=True) as elapsed:
            for rc in calls:
                logger.info("Running call [%s] with [%s]", rc.uses, rc.run_kwargs)
                self.run_call(rc)
            if self.verbose:
                logger.info(
                    " >> elapsed time for the workflow with %s tasks: %s",
                    len(self.tasks or []),
                    elapsed(),
                )


class TestRunner(BaseRunner):
    _config_name_: str = "__test__"
    load_args: RunConfig = RunConfig(_config_name_="load_data")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def hello(self, **kwargs):
        print("Hello World!", kwargs)

    def world(self, **kwargs):
        print("World Hello!", kwargs)
