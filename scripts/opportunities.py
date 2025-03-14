import os
import sys
from scripts.main import CRM
from scripts.schema_opportunities import *


class Opportunities(CRM):
    pass


if __name__ == "__main__":
    opportunities: Opportunities = Opportunities(
        os.path.abspath(sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    opportunities.main(__file__)
