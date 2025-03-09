import csv
import pathlib

import requests
import json
import re

def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

    payload = {}
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    post_json = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, headers=headers, json=post_json, data=payload)

    if json.loads(response.text).get("msg") == "ok":
        tenant_access_token = json.loads(response.text).get("tenant_access_token")
    else:
        tenant_access_token = ""

    return tenant_access_token



def csv_to_feishu(access_token, app_token, table_id, csv_path):
    B = {"records": []}
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            print(row)
            a = {"fields": {
                "用例编号": row[0],
                "用例标题": row[1],
                "提交人": row[2],
                "一级模块": row[3],
                "二级模块": row[4],
                "是否冒烟": row[5]
            }}
            B['records'].append(a)

    # print(B)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    print(url)
    print(B['records'])
    payload = json.dumps(B)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    # print(headers['Authorization'])
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

if __name__ == "__main__":
    app_id = "cli_a4747adaeafa900b"
    app_secret = "solIXhqwN8gq96LcFWMxGg6xtDJ0v1Cp"

    # access_token = get_tenant_access_token(app_id, app_secret)
    access_token = 'u-dFOgUgFgx19UCvHHXdKY9s0lmmLhllx1gMw0l0Kw02SV'
    print(access_token)

    csv_to_feishu(access_token, 'ZPJvw9KKXibg1ckmZtOcfp0HnCd', 'tblG0NKTaSBBgTRF', '/Users/xiaoyong/Documents/数据/test_cases.csv')
