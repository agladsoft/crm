import os
import sys
from __init__account import *
from rn_stagehistories import RnStagehistories


class Account(RnStagehistories):
    pass


if __name__ == "__main__":
    account: Account = Account(os.path.abspath(sys.argv[1]), sys.argv[2], HEADERS_ENG,
                                           LIST_OF_FLOAT_TYPE, LIST_OF_BOOL_TYPE, LIST_OF_INT_TYPE,
                                           LIST_OF_DATE_TYPE)
    account.main(__file__)
