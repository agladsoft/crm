import os
import sys
from scripts.main import CRM
from scripts.schema_opportunitysalesprocesses import *


class OpportunitySalesProcesses(CRM):
    pass


if __name__ == "__main__":
    opportunity_sales_processes: OpportunitySalesProcesses = OpportunitySalesProcesses(
        os.path.abspath(sys.argv[1]),
        sys.argv[2],
        HEADERS_ENG,
        LIST_OF_FLOAT_TYPE,
        LIST_OF_BOOL_TYPE,
        LIST_OF_INT_TYPE,
        LIST_OF_DATE_TYPE
    )
    opportunity_sales_processes.main(__file__)
