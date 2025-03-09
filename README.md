``QA团队队测试用的脚本，小工具等等``
1. dicomUtils包含：脱敏脚本，推送dicom脚本
2. press包括压测脚本和相关配置文件

```python私有依赖库设置方法```

common libs for python projects

##upload lib
1. add config below to `~/.pypirc`
```
[distutils]
index-servers =
  privatepypi 

[privatepypi]
repository:http://103.211.47.132:3141
username:user
password:passw0rd
```
2. modify setup.py of projects like
```
from setuptools import setup

setup(
    name='message_xsend',
    packages=['src'],
    version='0.1',
)
```
3. upload lib with
```
cd YOUR_TARGET_LIB
python setup.py sdist upload -r privatepypi
```

##install lib
1. add `requirements_local.txt` in target project
2. install with
```
pip install -i http://103.211.47.132:3141/simple --trusted-host 103.211.47.132 -r requirements_local.txt
```

## Usage
```python
from sk_dicom_client import PushBody, DicomClient, OperateResult
client = DicomClient(endpoint='127.0.0.1', port=5004, prefix=None)
result: OperateResult = client.push(
    PushBody(
        ae_id='00000000-0000-0000-0000-000000000001', server_store={}, service_name='plt-dicom-service',
        workspace='/Users/chenliang/workspace/data/test_push'
    )
)
print(result.result)
```