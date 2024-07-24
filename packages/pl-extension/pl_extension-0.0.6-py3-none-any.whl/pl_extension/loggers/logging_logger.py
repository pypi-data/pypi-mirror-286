import logging
import os
from typing import List

from pl_extension.utilities.logger import setup_logger
from pl_extension.utilities.rand import time_string

from lightning.pytorch.loggers.logger import Logger
from lightning.pytorch.utilities import rank_zero_only
from lightning.fabric.utilities.cloud_io import get_filesystem, _is_dir

__all__ = ["LoggingLogger"]


class LoggingLogger(Logger):

    """
    Logging logger.

    Args:
        root_dir: local logs save path.
        prefix: log data prefix, default is 'pl'
        skip_metrics: skip certain metric, useful for iter-wise metrics.

    Example::

        from pl_extension.loggers import LoggingLogger
        logging_logger = LoggingLogger(logdir='logs', prefix='pl_extension')
        trainer = Trainer(logger=[logging_logger])

    """

    def __init__(
        self,
        root_dir: str = ".pl_extension_logs",
        *,
        version: str = None,
        prefix: str = "pl",
        name: str = "pint_logger",
        skip_metrics: List = [],
        level=logging.INFO,
    ):
        super().__init__()
        root_dir = os.fspath(root_dir)
        self._root_dir = root_dir
        self._version = version
        self._name = name
        self._skip_metrics = skip_metrics
        self._level = level
        self._prefix = prefix
        self._fs = get_filesystem(root_dir)

    def __getattr__(self, name):
        if name == "logger":
            self.experiment.warning(
                "xxx.logger is deprecated, " "please use xxx.experiment instead"
            )
            return self.experiment

    @property
    @rank_zero_only
    def experiment(self):
        if self._experiment is not None:
            return self._experiment
        
        if self.root_dir:
            self._fs.makedirs(self.log_dir, exist_ok=True)
        logfile = os.path.join(self.log_dir, f"logginglogger.log")
        self._experiment = setup_logger(logfile, name=self._prefix, level=self._level)
        return self._experiment

    @rank_zero_only
    def info(self, *args, **kwargs):
        self._experiment.info(*args, **kwargs)

    @rank_zero_only
    def warning(self, *args, **kwargs):
        self._experiment.warning(*args, **kwargs)

    @rank_zero_only
    def error(self, *args, **kwargs):
        self._experiment.error(*args, **kwargs)

    @rank_zero_only
    def log_metrics(self, metrics, step):
        # skip metric in list
        metrics = {
            k: metrics[k] for k in metrics if k not in self._skip_metrics
        }
        _str = ""
        if "epoch" in metrics:
            _str += "Epoch[%d] " % metrics.pop("epoch")
        if "iter" in metrics:
            _str += "Iter[%d] " % metrics.pop("iter")
        else:
            _str += "Step[%d] " % step
        if "speed" in metrics:
            _str += "Speed: %.2f samples/sec, " % metrics.pop("speed")
        for k in metrics:
            if isinstance(metrics[k], int):
                _format = "%s=%d, "
            elif isinstance(metrics[k], float):
                if k == "lr":
                    _format = "%s=%.6f, "
                else:
                    _format = "%s=%.4f, "
            else:
                raise ValueError(f"Unknown value type: {type(metrics[k])}")
            _str += _format % (k, metrics[k])
        if _str:
            _str = _str[:-2]
            self.experiment.info(_str)

    @rank_zero_only
    def log_hyperparams(self, params):
        pass

    @property
    def name(self):
        return self._name

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def version(self):
        if self._version is None:
            self._version = self._get_next_version()
        return self._version

    def _get_next_version(self):
        save_dir = os.path.join(self.root_dir, self.name)
        try:
            listdir_info = self._fs.listdir(save_dir)
        except OSError as e:
            return 0

        existing_versions = []
        for listing in listdir_info:
            d = listing["name"]
            bn = os.path.basename(d)
            if _is_dir(self._fs, d) and bn.starswith("version_"):
                dir_ver = bn.split("_")[1].replace("/", "")
                if dir_ver.isdigit():
                    existing_versions.append(int(dir_ver))
        if len(existing_versions) == 0:
            return 0
        return max(existing_versions) + 1
    
    @property
    def log_dir(self) -> str:
        version = self.version if isinstance(self.version, str) else f"version_{self.version}"
        log_dir = os.path.join(self.root_dir, self.name, version)
        log_dir = os.path.expandvars(log_dir)
        log_dir = os.path.expanduser(log_dir)
        return log_dir

