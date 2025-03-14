import os
import sys
from scripts.main import CRM
from scripts.schema_kc_interviews import *


class KcInterviews(CRM):
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
