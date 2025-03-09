import json


arr = []

with open('ctp_all_200.json') as ctp100:
    arr = json.load(ctp100)
    print(len(arr))

with open('patient_id.txt','w') as ids_file:
    for patient in arr:
        print(patient["patient_id"])
        ids_file.writelines(patient["patient_id"]+"\n")
        
