import json
import logging
from datetime import datetime

import requests

import os
from dotenv import load_dotenv

load_dotenv()  # 这一行加载.env文件中的变量

authorization_token = os.getenv('AUTHORIZATION')
# 设置日志格式
logging.basicConfig(
    # filename='app.log',
    # filemode='a',  # 追加模式
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

headers = {
    'authority': 'www.autodl.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'appversion': 'v5.17.1',
    'authorization': authorization_token,
    'content-type': 'application/json;charset=UTF-8',
    'cookie': '_ga=GA1.1.2125540198.1687865255; Hm_lvt_e24036f31c6b8d171ce550a059a6f6fd=1699277821,1699283478,1699425008; Hm_lpvt_e24036f31c6b8d171ce550a059a6f6fd=1699425800; _ga_NDC1CJB7XZ=GS1.1.1699432949.19.0.1699432949.0.0.0',
    'origin': 'https://www.autodl.com',
    'referer': 'https://www.autodl.com/console/instance/list?_random_=1699432948862',
    'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
}

def manage_power(action, instance_uuid, payload=None):
    url = f"https://www.autodl.com/api/v1/instance/{action}"

    # Assuming that 'headers' should be passed and are defined outside this function.
    global headers

    # The payload is only necessary for the 'power_on' action.
    if action == 'power_on' and payload is not None:
        data = {
            "instance_uuid": instance_uuid,
            "payload": payload
        }
    else:
        data = {
            "instance_uuid": instance_uuid
        }

    # Convert the dictionary to a JSON string.
    data_json = json.dumps(data)

    # Make the POST request.
    response = requests.post(url, headers=headers, data=data_json)

    # Print the response text.
    # print(response.text)
    logger.info(response.text)
    return response.json()
def instance_list():


    url = "https://www.autodl.com/api/v1/instance"

    payload = "{\"date_from\":\"\",\"date_to\":\"\",\"page_index\":1,\"page_size\":10,\"status\":[],\"charge_type\":[]}"

    response = requests.request("POST", url, headers=headers, data=payload)
    data_list = response.json()['data']['list']
    return data_list
    # for data in data_list:
    #     print(data)
    #     print(data['uuid'], data['status'], data['gpu_idle_num'], data['stopped_at']['Time'])
    #     status = data['status']
    #     uuid = data['uuid']
    #     gpu_idle_num = data['gpu_idle_num']
    #     if status == 'shutdown':
    #         res = manage_power('power_on', uuid, 'non_gpu')
    #         if res['code'] == 'Success':
    #             logger.info(f'{uuid} power_on')
    #         else:
    #             logger.info(f'{uuid} power_on failed')
    #     elif status == 'running':
    #         res = manage_power('power_off', uuid)
    #         if res['code'] == 'Success':
    #             logger.info(f'{uuid} power_off')
    #         else:
    #             logger.info(f'{uuid} power_off failed')


def shutdown_all():
    instances = instance_list()
    for instance in instances:
        uuid = instance['uuid']
        status = instance['status']
        if status == 'running':
            res = manage_power('power_off', uuid)
            if res['code'] == 'Success':
                logger.info(f'{uuid} power_off')
            else:
                logger.info(f'{uuid} power_off failed')
        else:
            logger.info(f'{uuid} status is {status}, not running, no need to power_off')



def power_on_last():
    """
    启动最后一个关机的实例
    :return:
    """
    instances = instance_list()
    for data in instances:
        data['stop_time'] = datetime.fromisoformat(data['stopped_at']['Time']).timestamp()

    instances = sorted(instances, key=lambda x: x['stop_time'])
    data = instances[0]
    status = data['status']
    uuid = data['uuid']
    gpu_idle_num = data['gpu_idle_num']
    if status == 'shutdown':
        res = manage_power('power_on', uuid, 'non_gpu')
        if res['code'] == 'Success':
            logger.info(f'{uuid} power_on')
        else:
            logger.info(f'{uuid} power_on failed')




if __name__ == '__main__':
    # instances = instance_list()
    # for data in instances:
    #     data['stop_time'] = datetime.fromisoformat(data['stopped_at']['Time']).timestamp()
    #
    # instances = sorted(instances, key=lambda x: x['stop_time'], reverse=True)
    # for data in instances:
    #     print(data)
    #     print(data['uuid'], data['status'], data['gpu_idle_num'], data['stopped_at']['Time'], data['stop_time'])
    # shutdown_all(instances)
    # power_on_last()
    shutdown_all()