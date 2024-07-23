import sys
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import runpy
import os
import argparse
from typing import Optional
import socket


def write_stdout(s: str, flush: bool = True):
    '''写入stdout并刷新, 只能向 stdout 发送事件列表生成器协议信息'''
    sys.stdout.write(s)
    if flush:
        sys.stdout.flush()


def print(*values, sep=' ', end='\n', file=None, flush=True):
    '''重写print函数, 默认输出到stderr并刷新'''
    if file is None:
        file = sys.stderr
    file.write(sep.join(map(str, values)) + end)
    if flush:
        file.flush()


class SendEventlistenerMsg:
    '''发送事件侦听器消息
    参考： http://supervisord.org/events.html#event-listener-notification-protocol
    '''
    
    @staticmethod
    def ready():
        '''通知处于事件状态的事件侦听器，它已准备好接收事件'''
        write_stdout('READY\n')
    
    @staticmethod
    def ok():
        '''通知事件侦听器已成功处理事件'''
        write_stdout('RESULT 2\nOK')
    
    @staticmethod
    def fail():
        '''将假定侦听器未能处理该事件，并且该事件将在稍后重新缓冲并再次发送'''
        write_stdout('RESULT 2\nFAIL')


def parse_notif(line: str) -> Optional[dict]:
    '''解析事件通知'''  
    if not line or ':' not in line:
        return None
    notif = dict([ x.split(':') for x in line.split() ])
    for k, v in notif.items():
        try:
            notif[k] = int(v)
        except ValueError:
            try:
                notif[k] = float(v)
            except ValueError:
                pass
    return notif


def get_msg(tzinfo: ZoneInfo) -> dict:
    '''获取事件通知'''
    line = sys.stdin.readline()
    headers = parse_notif(line)
    data = payload = None
    if headers['len']:
        line = sys.stdin.read(headers['len'])
        if '\n' in line:
            line, data = line.split('\n', 1)
        payload = parse_notif(line)
    msg = {
        'hostname': socket.gethostname(),
        'time': datetime.now(tz=tzinfo).isoformat(),
        'time_zone': tzinfo.key,
        'headers': headers,
        'payload': payload,
        'data': data,
    }
    return msg


def handle_msg(msg: dict, run_path: str = None, context: dict = None) -> bool:
    '''处理事件通知
    eventname: http://supervisord.org/events.html#event-types'''
    print(json.dumps(msg))
    if run_path and os.path.exists(run_path):
        try:
            runpy.run_path(run_path, init_globals={
                'MSG': msg,
                'print': print,
                'CONTEXT': context,
            }, run_name=None)
        except BaseException as e:
            print(str(e))
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--handle_msg_py", default=None, help='处理消息的python文件，会传入全局变量MSG/CONTEXT，留空不执行')
    parser.add_argument("--time_zone", default='Asia/Shanghai', help='时区')
    args = parser.parse_args()
    
    tzinfo = ZoneInfo(args.time_zone)
    context = {}  # handle_msg_py 可用的全局变量
    while 1:
        SendEventlistenerMsg.ready()
        msg = get_msg(tzinfo)
        if handle_msg(msg, args.handle_msg_py, context):
            SendEventlistenerMsg.ok()
        else:
            SendEventlistenerMsg.fail()


if __name__ == '__main__':
    main()
