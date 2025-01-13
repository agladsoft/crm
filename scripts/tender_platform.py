import os
import sys
from settings_tender_platform import *
from rn_stagehistories import RnStagehistories


class TenderPlatform(RnStagehistories):
    pass


if __name__ == "__main__":
    tender_platform: TenderPlatform = TenderPlatform(
        os.path.abspath(sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    tender_platform.main(__file__)
