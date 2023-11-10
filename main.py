# 创建解析器
import argparse

from autodl import power_on_last, shutdown_all

parser = argparse.ArgumentParser(description="Control the AutoDL system.")
# 添加参数
parser.add_argument('--power_on_last', action='store_true', help='Activate the power_on_last function')
parser.add_argument('--shutdown_all', action='store_true', help='Activate the shutdown_all function')

def add_parser():
    args = parser.parse_args()
    if args.power_on_last:
        power_on_last()
    elif args.shutdown_all:
        shutdown_all()

if __name__ == '__main__':
    add_parser()