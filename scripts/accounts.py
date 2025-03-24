import os
import sys
from settings_accounts import *
from rn_stagehistories import RnStagehistories


class Accounts(RnStagehistories):
    pass


if __name__ == "__main__":
    accounts: Accounts = Accounts(os.path.abspath(
        sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    accounts.main(__file__)
