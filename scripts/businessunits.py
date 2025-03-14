import os
import sys
from scripts.main import CRM
from scripts.schema_businessunits import *


class Businessunits(CRM):
    pass


if __name__ == "__main__":
    businessunits: Businessunits = Businessunits(
        os.path.abspath(sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    businessunits.main(__file__)
