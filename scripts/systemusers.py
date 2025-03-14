import os
import sys
from scripts.main import CRM
from scripts.schema_systemusers import *


class Systemusers(CRM):
    pass


if __name__ == "__main__":
    systemusers: Systemusers = Systemusers(
        os.path.abspath(sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    systemusers.main(__file__)
