import json
import logging
import time
from datetime import datetime, timezone, timedelta

import requests

import os
from dotenv import load_dotenv

from autodl.login import get_token
from ssh_tools import run_ssh

load_dotenv()  # 这一行加载.env文件中的变量

authorization_token = get_token()
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

    data = {
        "instance_uuid": instance_uuid
    }

    if payload is not None:
        data['payload'] = payload
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
    if response.json()['code'] != 'Success':
        logger.error(response.json())
        return None

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

def get_instance(uuid):
    instances = instance_list()
    for instance in instances:
        if instance['uuid'] == uuid:
            return instance
    return None

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
    logger.info('power_on_last')
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


def change_timestamp(time_str):
    if time_str == '0001-01-01T00:00:00Z':
        return 0
    # 将时间字符串解析为datetime对象
    dt = datetime.fromisoformat(time_str)

    # 如果时间字符串中包含时区信息，则可以将其保留在datetime对象中
    # 如果不包含时区信息，可以手动添加所需的时区信息
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))  # 时区信息表示+08:00
    return dt.timestamp()

def power_api():
    """
    开启服务器，并且运行程序
    :return:
    """
    instances = instance_list()
    for data in instances:
        data['stop_time'] = change_timestamp(data['stopped_at']['Time'])

    instances = sorted(instances, key=lambda x: x['stop_time'], reverse=True)
    # for data in instances:
    #     print(data)
    #     print(data['uuid'], data['status'], data['gpu_idle_num'], data['stopped_at']['Time'], data['stop_time'])

    # 过滤data['gpu_idle_num'] == 0的设备
    instances = filter(lambda x: x['gpu_idle_num'] > 0, instances)
    instances = list(instances)
    if len(instances) > 0:
        data = instances[0]
        status = data['status']
        uuid = data['uuid']
        gpu_idle_num = data['gpu_idle_num']
        root_password = data['root_password']
        proxy_host = data['proxy_host']
        ssh_port = data['ssh_port']

        if status == 'shutdown':
            res = manage_power('power_on', uuid)
            if res['code'] == 'Success':
                logger.info(f'{uuid} power_on')
                # 等待实例启动完成
                while True:
                    instance = get_instance(uuid)
                    if instance['status'] == 'running':
                        break
                    time.sleep(1)
                    print('wait for instance running')

                # 获取实例信息
                run_ssh(proxy_host, ssh_port, 'root', root_password, '/root/frp_me/frpc -c /root/frp_me/frpc.ini')
                run_ssh(proxy_host, ssh_port, 'root', root_password, '/root/miniconda3/bin/python /root/autodl-fs/codegen/app.py')

            else:
                logger.info(f'{uuid} power_on failed')
        else:
            logger.info(f'{uuid} status is {status}, not shutdown, no need to power_on')


if __name__ == '__main__':
    pass
    # instances = instance_list()
    # for data in instances:
    #     data['stop_time'] = change_timestamp(data['stopped_at']['Time'])
    #
    # instances = sorted(instances, key=lambda x: x['stop_time'], reverse=True)
    # for data in instances:
    #     print(data)
    #     print(data['uuid'], data['status'], data['gpu_idle_num'], data['stopped_at']['Time'], data['stop_time'])

    # 过滤data['gpu_idle_num'] == 0的设备
    # for data in instances:
    #     print(data)
    #     print(data['uuid'], data['status'], data['gpu_idle_num'], data['stopped_at']['Time'], data['stop_time'], data['root_password'], data['proxy_host'], data['ssh_port'])

    # shutdown_all(instances)
    # power_on_last()
    # 解析命令行参数
