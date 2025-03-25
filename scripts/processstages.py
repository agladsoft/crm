import os
import sys
from settings_processstages import *
from rn_stagehistories import RnStagehistories


class ProcesStages(RnStagehistories):
    pass


if __name__ == "__main__":
    proces_stages: ProcesStages = ProcesStages(
        os.path.abspath(sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    proces_stages.main(__file__)
