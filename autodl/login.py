import json

import requests


def get_ticket():
    url = "https://www.autodl.com/api/v1/new_login"

    payload = "{\"phone\":\"17698397517\",\"password\":\"af8b2c5524912454f15bf236fc04477458cb978f\",\"v_code\":\"\",\"phone_area\":\"+86\",\"picture_id\":null}"
    headers = {
      'authority': 'www.autodl.com',
      'accept': '*/*',
      'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
      'appversion': 'v5.17.2',
      'authorization': 'null',
      'content-type': 'application/json;charset=UTF-8',
      'cookie': '_ga=GA1.1.2125540198.1687865255; Hm_lvt_e24036f31c6b8d171ce550a059a6f6fd=1699425008,1699454558,1699592637,1699891212; Hm_lpvt_e24036f31c6b8d171ce550a059a6f6fd=1699891212; _ga_NDC1CJB7XZ=GS1.1.1699891213.31.1.1699891222.0.0.0',
      'origin': 'https://www.autodl.com',
      'referer': 'https://www.autodl.com/login',
      'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['data']['ticket']



def get_token():
    ticket = get_ticket()

    url = "https://www.autodl.com/api/v1/passport"

    payload = {
        'ticket': ticket
    }
    data_json = json.dumps(payload)
    print(data_json)
    headers = {
        'authority': 'www.autodl.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'appversion': 'v5.17.2',
        'authorization': 'null',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://www.autodl.com',
        'referer': 'https://www.autodl.com/login',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }

    response = requests.request("POST", url, headers=headers, data=data_json)

    return response.json()['data']['token']


if __name__ == '__main__':
    print(get_token())
