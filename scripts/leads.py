import os
import sys
from scripts.main import CRM
from scripts.schema_leads import *


class Leads(CRM):
    pass


if __name__ == "__main__":
    leads: Leads = Leads(
        os.path.abspath(sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    leads.main(__file__)
