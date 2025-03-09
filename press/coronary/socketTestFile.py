import os
import shutil
from press.DTO import ProductDataClass
import random


class CoronaryTestCase(ProductDataClass):

    def __init__(self):
        ProductDataClass.__init__(self)

    def get_mysql_case(self):
        return [case.case_num for case in
                self.coronary_session.query(
                    self.coronary_cases).filter(
                    self.coronary_cases.state.in_(["2", "4", "5"])).all()]


def make_file(case_list):
    """
    :param case_list:
    :return:
    test_sample_T20200303122918H224f44300b2e1ea9,Cpr,tree1_01,0
    test_sample_T20200303122918H224f44300b2e1ea9,straight,tree1_01,0
    test_sample_T20200303122918H224f44300b2e1ea9,shortAxis,tree1_01,1
    {Cpr:2,straight:4,shortAxis:5}
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webSocketTest.txt")
    if os.path.exists(file_path):
        os.remove(file_path)
    for case in case_list[0:1]:
        case_list_info = []
        for image_type in ["2", "4", "5"]:
            for tree in ["tree1_01", "tree1_02", "tree1_03"]:
                position = 0
                while True:
                    if image_type == "2":
                        case_list_info.append([case, image_type, tree, position])
                        position = position + 4
                        if position > 360:
                            break
                    elif image_type == "4":
                        case_list_info.append([case, image_type, tree, position])
                        position = position + 10
                        if position > 360:
                            break
                    else:
                        case_list_info.append([case, image_type, tree, position])
                        position = position + 1
                        if position > 100:
                            break
        with open(file_path, "a+") as file:
            for case_info in case_list_info:
                file.write(",".join([str(c) for c in case_info])+'\n')
    local_path = "/Users/jinjie/apache-jmeter-4.0/dependencies/userfile/webSocket.txt"
    if os.path.exists(local_path):
        shutil.copyfile(file_path, local_path)


def make_file_single(case_list):
    """
    :param case_list:
    :return:
    test_sample_T20200303122918H224f44300b2e1ea9,Cpr,tree1_01,0
    test_sample_T20200303122918H224f44300b2e1ea9,straight,tree1_01,0
    test_sample_T20200303122918H224f44300b2e1ea9,shortAxis,tree1_01,1
    {Cpr:2,straight:4,shortAxis:5}
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webSocketTest.txt")
    if os.path.exists(file_path):
        os.remove(file_path)
    case_list_info = []
    for case in case_list:
        case_list_info.append([case, random.choice(["2", "5"]), "tree1_01", "0"])
    with open(file_path, "a+") as file:
        for case_info in case_list_info[:10]:
            file.write(",".join([str(c) for c in case_info])+'\n')
    local_path = "/Users/jinjie/apache-jmeter-4.0/dependencies/userfile/webSocket.txt"
    if os.path.exists(local_path):
        shutil.copyfile(file_path, local_path)
    return case_list_info


if __name__ == '__main__':
    # make_file(CoronaryTestCase().get_mysql_case())
    print(make_file_single(CoronaryTestCase().get_mysql_case()))