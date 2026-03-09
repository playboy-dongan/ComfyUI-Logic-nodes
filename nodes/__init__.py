from .blocker import NODE_CLASS_MAPPINGS as _B, NODE_DISPLAY_NAME_MAPPINGS as _BD
from .preview_any import NODE_CLASS_MAPPINGS as _P, NODE_DISPLAY_NAME_MAPPINGS as _PD
from .judge import NODE_CLASS_MAPPINGS as _J, NODE_DISPLAY_NAME_MAPPINGS as _JD
from .switch import NODE_CLASS_MAPPINGS as _S, NODE_DISPLAY_NAME_MAPPINGS as _SD
from .switcher import NODE_CLASS_MAPPINGS as _SW, NODE_DISPLAY_NAME_MAPPINGS as _SWD
from .batch_combiner import NODE_CLASS_MAPPINGS as _BC, NODE_DISPLAY_NAME_MAPPINGS as _BCD
from .looper import NODE_CLASS_MAPPINGS as _L, NODE_DISPLAY_NAME_MAPPINGS as _LD
from .random_tool import NODE_CLASS_MAPPINGS as _R, NODE_DISPLAY_NAME_MAPPINGS as _RD
from .preview import NODE_CLASS_MAPPINGS as _UP, NODE_DISPLAY_NAME_MAPPINGS as _UPD
from .converter import NODE_CLASS_MAPPINGS as _C, NODE_DISPLAY_NAME_MAPPINGS as _CD
from .math_expression import NODE_CLASS_MAPPINGS as _M, NODE_DISPLAY_NAME_MAPPINGS as _MD
from .video_decompose import NODE_CLASS_MAPPINGS as _VD, NODE_DISPLAY_NAME_MAPPINGS as _VDD
from .video_compose import NODE_CLASS_MAPPINGS as _VC, NODE_DISPLAY_NAME_MAPPINGS as _VCD

NODE_CLASS_MAPPINGS = {**_B, **_P, **_J, **_S, **_SW, **_BC, **_L, **_R, **_UP, **_C, **_M, **_VD, **_VC}
NODE_DISPLAY_NAME_MAPPINGS = {**_BD, **_PD, **_JD, **_SD, **_SWD, **_BCD, **_LD, **_RD, **_UPD, **_CD, **_MD, **_VDD, **_VCD}
