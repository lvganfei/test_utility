import json
import sys

with open('/Users/xiaoyong/Documents/数据/jupiter_series.json', 'r') as source:
    raw = json.load(source)
    print(len(raw))

    tmpDict = {}
    # tempDict = {
    #     "0000032": [
    #         "1",
    #         "2"
    #     ]
    # }
    for patient in raw:
        if patient["patient_id"] in tmpDict:
            tmpDict[patient["patient_id"]].append(patient["series_instance_uid"])
        else:
            tmpDict[patient["patient_id"]] = []
            tmpDict[patient["patient_id"]].append(patient["series_instance_uid"])
    print(tmpDict)
    print(len(tmpDict))
    with open('./jupiter_patient_series.json','w') as final:
        final.write(json.dumps(tmpDict))