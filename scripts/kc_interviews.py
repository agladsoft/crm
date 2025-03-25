import os
import sys
from settings_kc_interviews import *
from rn_stagehistories import RnStagehistories


class KcInterviews(RnStagehistories):
    pass


if __name__ == "__main__":
    kc_interviews: KcInterviews = KcInterviews(
        os.path.abspath(sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    kc_interviews.main(__file__)
