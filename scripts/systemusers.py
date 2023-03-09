import os
import sys
from __init__systemusers import *
from rn_stagehistories import RnStagehistories


class Systemusers(RnStagehistories):
    pass


if __name__ == "__main__":
    systemusers: Systemusers = Systemusers(os.path.abspath(sys.argv[1]), sys.argv[2], HEADERS_ENG,
                                           LIST_OF_FLOAT_TYPE, LIST_OF_BOOL_TYPE, LIST_OF_INT_TYPE,
                                           LIST_OF_DATE_TYPE)
    systemusers.main(__file__)
