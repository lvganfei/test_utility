import pydicom
import shutil
import os
import sys


def get_dicom_info(path="/data1/data/source/thoracic", tag_name="Rows", tag_value="512"):
    for case in os.listdir(path):
        if os.path.isdir(os.path.join(path, case)):
            case_path = os.path.join(path, case)
            for dcm in os.listdir(case_path):
                if 'dcm' in dcm:
                    ds = pydicom.dcmread(os.path.join(case_path, dcm))
                    print(ds)
                    if ds[tag_name] == tag_value:
                        print('value match')
                        print(case_path)
                    else:
                        print('not match')
                    break
                else:
                    print('next')


if __name__ == "__main__":
    args=sys.argv
    print(args)
    path = args[1]
    name = args[2]
    specialVal= args[3]
    get_dicom_info(path, name, specialVal)
