import os
import sys
from __init__opportunities import *
from rn_stagehistories import RnStagehistories


class Opportunities(RnStagehistories):
    pass


if __name__ == "__main__":
    input_file_path: str = os.path.abspath(sys.argv[1])
    output_folder: str = sys.argv[2]
    opportunities: Opportunities = Opportunities(input_file_path, output_folder,
                                                 HEADERS_ENG, LIST_OF_FLOAT_TYPE,
                                                 LIST_OF_BOOL_TYPE, LIST_OF_INT_TYPE,
                                                 LIST_OF_DATE_TYPE)
    parsed_data: list = opportunities.convert_csv_to_dict()
    divided_parsed_data: list = list(opportunities.divide_chunks(parsed_data, 50000))
    for index, chunk_parsed_data in enumerate(divided_parsed_data):
        for dict_data in chunk_parsed_data:
            opportunities.change_type(dict_data)
        opportunities.save_data_to_file(index, chunk_parsed_data)
