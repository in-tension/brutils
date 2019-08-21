


## to use BaseDict, import it directly
## from brutils.base_dict import BaseDict

from .misc import *
from . import arrs
import imp
imp.reload(arrs)
from .arrs import *
from .obj_attrs import *
from .tic_toc import *

from .bidirectional_iter import *

import platform
if platform.system() != 'Java' :
    from .plot_looper import *


