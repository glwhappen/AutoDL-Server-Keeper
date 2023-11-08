import json
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import requests

import os
from dotenv import load_dotenv

load_dotenv()  # 这一行加载.env文件中的变量

authorization_token = os.getenv('AUTHORIZATION')

# 设置日志格式
logging.basicConfig(
    filename='app.log',
    filemode='a',  # 追加模式
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

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
    print(response.text)

@scheduler.scheduled_job(IntervalTrigger(minutes=5)) # minutes=5 hours=1
def change():
    logger.info("Powering on the instance...")
    manage_power('power_on', '9e6011ae3c-6effd328', 'non_gpu')
    # 这里记录一个日志，表示电源打开
    logger.info("Instance powered on. Waiting for 60 seconds before powering off...")
    time.sleep(60)  # 等待60秒后关闭电源
    # 这里记录一个日志，表示即将关闭电源
    logger.info("Powering off the instance...")
    manage_power('power_off', '9e6011ae3c-6effd328')
    # 这里记录一个日志，表示电源关闭
    logger.info("Instance powered off.")

if __name__ == '__main__':
    if os.getenv('RUN_CHANGE_FUNCTION'):
        change()
    else:
        scheduler.start()
        print('Scheduler started, press Ctrl+C to exit.')

    try:
        # 保持主线程活跃
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # 如果您运行的是长期进程，即使在守护模式下也应该执行此关闭操作
        scheduler.shutdown()  # 安全关闭调度器