import os
import sys
from settings_tender_platform import *
from rn_stagehistories import RnStagehistories


class RnTenderPlatforms(RnStagehistories):
    pass


if __name__ == "__main__":
    rn_tenderplatforms: RnTenderPlatforms = RnTenderPlatforms(
        os.path.abspath(sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    rn_tenderplatforms.main(__file__)
