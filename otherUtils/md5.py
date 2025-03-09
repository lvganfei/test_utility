import hashlib
import sys

appid = 'cloud'
files = '["https://toc-stg.democompany.net/dicom/141/29182/53,1e229d1b9a7ee7"]'
callback= '{"printCallback":"","pushCallback":"https://toc-stg.democompany.net/aidiagnose/api/v1/openapi/push_case","stateCallback":""}'
method = 'md5'
nounce = '4dfbfce35e0a43f7bcd7627f7efde42f'
ts = '1595146990117'
serviceKey = 'coronary'
secret = '85479c4e03f9438cbed1e28f0f66a628'
seriesInstanceUid = '1.2.840.113619.2.359.3.209782018.950.1550132792.252'
urls='["/api/v1/openapi/files?resource=coronary/T20200716145210H1f4164c4/push_dcm/d6428a56-e6f8-4167-a238-0cbec0202dae/1.2.826.0.1.3680043.8.498.10213555740713481115175493332465473192.dcm"]'


def md5_func(string):
    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()

if __name__ == '__main__':
    args=sys.argv
    print(args)
    ticketid = args[1]
    source = secret + appid + callback + files + method + nounce + serviceKey + ticketid + ts + secret
    source2 = secret + appid + method + nounce + serviceKey+ticketid + ts +urls+ secret
    source3 = secret + appid + method + nounce + seriesInstanceUid + ticketid + ts + secret 
    print(source2)
    print(md5_func(source))
    print(md5_func(source2))
    print(md5_func(source3))
