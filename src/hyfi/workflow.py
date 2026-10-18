"""Workflows: an ordered list of steps, each a callable built with Hydra ``instantiate``.

.. code-block:: yaml

    # conf/workflow/demo.yaml
    name: demo
    steps:
      - run: mypkg.io.load_csv
        with: {path: data/in.csv}
      - run: mypkg.clean.clean      # gets the previous result as its first argument
      - run: mypkg.io.save
        with: {path: out.csv}
        pipe: true
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from hydra.utils import get_object
from pydantic import BaseModel, ConfigDict, Field, model_validator

from hyfi.config import instantiate


class Step(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    name: str = ""
    run: str
    with_: dict[str, Any] = Field(default_factory=dict, alias="with")
    pipe: bool = True

    @model_validator(mode="after")
    def _default_name(self) -> Step:
        if not self.name:
            self.name = self.run.rsplit(".", 1)[-1]
        return self


class Workflow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = "workflow"
    steps: list[Step] = Field(default_factory=list)


class StepRecord(BaseModel):
    name: str
    run: str
    status: str = "pending"  # pending | ok | error | skipped
    seconds: float | None = None
    error: str | None = None


class WorkflowError(RuntimeError):
    def __init__(self, message: str, records: list[StepRecord]):
        super().__init__(message)
        self.records = records


def plan(workflow: Workflow) -> list[dict[str, Any]]:
    """Resolve every step target without calling it. ``ok`` is False when the import fails."""
    out = []
    for step in workflow.steps:
        entry: dict[str, Any] = {
            "name": step.name,
            "run": step.run,
            "with": step.with_,
            "pipe": step.pipe,
            "ok": True,
            "error": None,
        }
        try:
            get_object(step.run)
        except Exception as e:  # get_object wraps import failures in various types
            entry["ok"] = False
            entry["error"] = f"{type(e).__name__}: {e}"
        out.append(entry)
    return out


def execute(
    workflow: Workflow,
    on_record: Callable[[StepRecord], None] | None = None,
) -> tuple[Any, list[StepRecord]]:
    """Run the steps in order and return the last result and one record per step.

    With ``pipe`` (the default) a step receives the previous step's result as its first positional
    argument when that result is not None. On failure the remaining steps are marked ``skipped``
    and :class:`WorkflowError` carries the records.
    """
    records = [StepRecord(name=s.name, run=s.run) for s in workflow.steps]
    prev: Any = None
    for i, (step, rec) in enumerate(zip(workflow.steps, records, strict=True)):
        args = (prev,) if step.pipe and prev is not None else ()
        started = time.perf_counter()
        try:
            prev = instantiate({"_target_": step.run, **step.with_}, *args)
        except Exception as e:
            rec.status, rec.error = "error", f"{type(e).__name__}: {e}"
            rec.seconds = round(time.perf_counter() - started, 6)
            for later in records[i + 1 :]:
                later.status = "skipped"
            if on_record:
                on_record(rec)
            raise WorkflowError(f"step {step.name!r} failed: {rec.error}", records) from e
        rec.status, rec.seconds = "ok", round(time.perf_counter() - started, 6)
        if on_record:
            on_record(rec)
    return prev, records
