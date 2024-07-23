import json
import re
from .utils import push_msg, PushPlusSend
from .supervisor_eventlistener import print


def msg_callback(
    msg: dict,
    context: dict = None,
    token: str = '',
    title: str = 'supervisor',
    search_eventname: str = r'^(PROCESS_STATE_FATAL|PROCESS_STATE_EXITED|PROCESS_COMMUNICATION)',
    **kwargs,
):
    """消息回调的例子

    Args:
        msg (dict): 消息
        context (dict, optional): 上下文
        token (str, optional): pushpush 用户令牌
        title (str, optional): 消息标题
        search_eventname (str, optional): 匹配 eventname 的正则表达式
            PROCESS_STATE,PROCESS_LOG,PROCESS_COMMUNICATION,SUPERVISOR_STATE_CHANGE,PROCESS_GROUP,TICK
    """
    if re.search(search_eventname, msg['headers']['eventname']):
        m = PushPlusSend(
            token=token,
            title=title,
            content=json.dumps(msg),
            template='json',
            **kwargs,
        )
        print('push_msg:', push_msg(m))


if __name__ == '__main__':
    MSG = {
        "hostname": "test",
        "time": "2024-07-22T18:06:40.177068+08:00",
        "time_zone": "Asia/Shanghai",
        "headers": {
            "ver": 3.0,
            "server": "supervisor",
            "serial": 482,
            "pool": "eventlistener-process",
            "poolserial": 1,
            "eventname": "PROCESS_STATE_EXITED",
            "len": 92
        },
        "payload": {
            "processname": "eventlistener-process",
            "groupname": "eventlistener-process",
            "from_state": "STOPPED",
            "tries": 0
        },
        "data": None
    }
    CONTEXT = {}
    
    msg_callback(MSG)
