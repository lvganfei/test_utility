import os
import sys

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString


yaml = YAML()
yaml.preserve_quotes = True
yaml.explicit_start = True
print(os.getcwd())
product = sys.argv[1]
new_version = sys.argv[2]
yaml_path = sys.argv[3]

if (product == 'brightgate'):
    prd_key = ['spine', 'vessel', '3dviewer']


# version_path = os.path.join(os.getcwd(), 'main-prd.yml')
with open(yaml_path, 'r+', encoding='utf-8') as y_f:
    main_prd_obj = yaml.load(y_f.read())
    print(main_prd_obj)
    for key in prd_key:
        # print(main_prd_obj[key]['params']['alg_version'])
        main_prd_obj[key]['params']['alg_version'] = str(new_version)
    print(main_prd_obj)
    
    y_f.seek(0,0)
    y_f.truncate()
    yaml.dump(main_prd_obj, y_f)
    y_f.close()