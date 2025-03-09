import os
import os.path as osp
import sys
import pydicom as pd



def defreeze(path):
    
    for case in os.listdir(path):
        series_cls = {}
        case_path = osp.join(path, case)
        if osp.isdir(case_path):

            print(case_path)
            dicom_list = os.listdir(case_path)
            handled_set = ('LEFT','RIGHT', 'TARGET')
            interset = set(dicom_list).intersection(handled_set)
            if len(interset) > 0:
                continue
            for dicom in dicom_list:
                dicom_path = osp.join(path, case, dicom)
                try:
                    dobj = pd.read_file(dicom_path)
                    seriesname = dobj[0x0049, 0x1023].value
                    seriesperc = dobj[0x0020, 0x9241].value
                    seriesinstanceuid = dobj[0x0020,0x000e].value
                    instancenumber = dobj[0x0020,0x0013].value
                    # print(location)
                    if seriesname not in series_cls:
                        series_cls.setdefault(seriesname, [])
                    else:
                        series_cls[seriesname].append({"dicom_path": dicom_path, "instancenumber": int(instancenumber), "seriesperc": seriesperc})
                    print(dicom_path)
                    print(seriesname)
                    print(seriesperc)
                    print(instancenumber)
                except KeyError as e:
                    print('e')
        else:
            print('not a dicom') 
        print(series_cls)
        for name, dicoms in series_cls.items():
            print(name)
    
            os.mkdir(osp.join(case_path, name))
            dicoms.sort(key=lambda ele : ele["instancenumber"])
            for idx, ele in enumerate(dicoms):
                print(idx)
                old_dicom_path = ele["dicom_path"]
                old_dicom_per = str(ele["seriesperc"])
                print(old_dicom_path)
                ds = pd.dcmread(old_dicom_path)
                ds.InstanceNumber = idx + 1
                old_series_instanceUID = str(ds.SeriesInstanceUID)
                ds.SeriesInstanceUID = f'{old_series_instanceUID}.{old_dicom_per}'
                ds.SeriesDescription = f'Phase {old_dicom_per}%'
                ds.save_as(osp.join(case_path, name, f'{idx}.dcm'))


if __name__ == '__main__':
    root = sys.argv[1]
    defreeze(root)