from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Sequence

from loguru import logger
from pdm.backend.base import Context
from pyfuture.hooks import pdm as pyfuture_pdm_hooks
from pyfuture.utils import get_target


class PyFutureBuildHook:
    def __init__(self) -> None:
        self.target_str = None

    @property
    def target(self) -> tuple[int, int]:
        return get_target(self.target_str)

    def pdm_build_hook_enabled(self, context: Context):
        hook_config = pyfuture_pdm_hooks.get_hook_config(context)
        if context.target == "editable":
            if sys.version_info[:2] < (3, 12):
                raise RuntimeError("PyFuture cannot be installed by editable mode in Python < 3.12")
            elif self.target < (3, 12):
                # TODO: support editable
                # enable_editable = hook_config.get("enable_editable", True)
                # return context.target == "wheel" or (not enable_editable and context.target == "editable")
                logger.warning("Target config is ignored in editable mode")
                self.target_str = "py312"
        else:
            self.target_str = pyfuture_pdm_hooks.get_target_str(hook_config)
        return context.target == "wheel"

    def pdm_build_initialize(self, context: Context) -> None:
        pyfuture_pdm_hooks.pdm_build_initialize(context, self.target_str)

    def pdm_build_update_files(self, context: Context, files: dict[str, Path]) -> None:
        pyfuture_pdm_hooks.pdm_build_update_files(context, files, self.target)
