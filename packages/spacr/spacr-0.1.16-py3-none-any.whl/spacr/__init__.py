from spacr.version import version, version_str
import logging
import torch

from . import core
from . import io
from . import utils
from . import settings
from . import plot
from . import measure
from . import sim
from . import sequencing
from . import timelapse
from . import deep_spacr
from . import app_annotate
from . import gui_utils
from . import app_make_masks
from . import app_make_masks_v2
from . import app_mask
from . import app_measure
from . import app_classify
from . import logger


__all__ = [
    "core",
    "io",
    "utils",
    "settings",
    "plot",
    "measure",
    "sim",
    "sequencing"
    "timelapse",
    "deep_spacr",
    "app_annotate",
    "gui_utils",
    "app_make_masks",
    "app_make_masks_v2",
    "app_mask",
    "app_measure",
    "app_classify",
    "logger"
]

# Check for CUDA GPU availability
if torch.cuda.is_available():
    from . import graph_learning
    __all__.append("graph_learning")
    logging.info("CUDA GPU detected. Graph learning module loaded.")
else:
    logging.info("No CUDA GPU detected. Graph learning module not loaded.")

logging.basicConfig(filename='spacr.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
