    }
    request=requests.post(roboturl,headers={"Content-Type": "text/plain"},json= data)
    print(request)

if __name__ == '__main__':


    #产品平台模拟登录token
    platform_data = {
        "username": platform_username,
        "password": platform_password
    }
    platform_login=requests.post(platform_login_url,headers={"Content-Type": "application/json","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"},json=platform_data)
    platform_token=platform_login.json().get("token")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Authorization": "Bearer "+platform_token
    }

    #交付平台模拟登录token
    deliver_data = {
        "username": deliver_username,
        "password": deliver_password
    }
    # deliver_login=requests.post(deliver_login_url,headers={"Content-Type": "application/json"},json=deliver_data)
    # print(deliver_login.status_code)
    # deliver_headers=deliver_login.json().get("token")