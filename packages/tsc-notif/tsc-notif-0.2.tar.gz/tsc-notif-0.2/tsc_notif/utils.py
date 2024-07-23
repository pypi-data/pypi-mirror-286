import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import Union, Optional, Literal
import json
from pydantic import BaseModel, Field
import os
import shutil
import time
import subprocess


def model_to_dict(model: Optional[Union[BaseModel, dict]], **kwargs) -> dict:
    """
    Convert a Pydantic model to a dictionary, compatible with both Pydantic 1.x and 2.x.
    """
    if isinstance(model, (dict, type(None))):
        return model
    try:
        # Try using Pydantic 2.x method
        return model.model_dump(**kwargs)
    except AttributeError:
        # Fallback to Pydantic 1.x method
        return model.dict(**kwargs)


class PushPlusSend(BaseModel):
    '''http://www.pushplus.plus/doc/guide/api.html#一、发送消息接口'''
    token: str = Field(..., description='用户令牌，可直接加到请求地址后，如：http://www.pushplus.plus/send/{token}')
    title: Optional[str] = Field(None, description='消息标题')
    content: str = Field(..., description='具体消息内容，根据不同template支持不同格式')
    topic: Optional[str] = Field(None, description='群组编码，不填仅发送给自己；channel为webhook时无效')
    template: Literal['html', 'txt', 'json', 'markdown', 'cloudMonitor', 'jenkins', 'route', 'pay'] = Field('html', description='发送模板')
    channel: Literal['wechat', 'webhook', 'cp', 'mail', 'sms'] = Field('wechat', description='发送渠道')
    webhook: Optional[str] = Field(None, description='webhook编码')
    callbackUrl: Optional[str] = Field(None, description='发送结果回调地址')
    timestamp: Optional[int] = Field(None, description='毫秒时间戳。格式如：1632993318000。服务器时间戳大于此时间戳，则消息不会发送')
    to: Optional[str] = Field(None, description='好友令牌，微信公众号渠道填写好友令牌，企业微信渠道填写企业微信用户id')


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def push_msg(params: Union[dict, PushPlusSend]) -> dict:
    '''推送消息'''
    params = model_to_dict(params)
    res = requests.get('https://www.pushplus.plus/send', params=params)
    res.raise_for_status()
    ret = res.json()
    if ret['code'] != 200:
        print(ret)
    return ret


def get_disk_usage(path) -> dict:
    '''获取磁盘使用情况'''
    if os.path.ismount(path):
        total, used, free = shutil.disk_usage(path)
        return {'total': total, 'used': used, 'free': free}
    else:
        raise ValueError(f"The path '{path}' is not a mounted disk.")


class LimitedNotifier:
    def __init__(self) -> None:
        self.notif_count_cont = 0  # 连续通知次数
        self.last_notif_time = 0  # 上次通知时间戳, 单位秒
    
    def should_notify(self) -> bool:
        '''是否应该通知，防止过于频繁通知'''
        if time.time() - self.last_notif_time < 3600 * min(24, self.notif_count_cont ** 1.5):
            return False
        return True

    def push_msg(self, params: Union[dict, PushPlusSend]) -> Union[dict, None]:
        '''推送消息'''
        if not self.should_notify():
            return None
        ret = push_msg(params)
        self.last_notif_time = time.time()
        self.notif_count_cont += 1
        return ret
    
    def reset_cont(self):
        '''重置连续通知次数'''
        self.notif_count_cont = 0
        self.last_notif_time = 0


def get_container_status(container_name) -> str:
    try:
        # 执行 Docker inspect 命令获取容器的详细信息
        result = subprocess.run(['docker', 'inspect', container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 检查是否成功执行命令
        if result.returncode != 0:
            raise ValueError(f"Error inspecting container {container_name}: {result.stderr.strip()}")
        # 解析输出的 JSON 数据
        container_info = json.loads(result.stdout)
        # pprint(container_info)
        # 检查容器的状态
        health_status = container_info[0]['State'].get('Health', {}).get('Status', 'unknown')
        return health_status
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError, IndexError) as e:
        raise ValueError(f"An error occurred while checking the health status of container {container_name}: {str(e)}")


if __name__ == '__main__':
    params = PushPlusSend(
        token=input('Token: '),
        title='测试消息标题',
        content=json.dumps({
            "event": "message_complate",
            "messageInfo": {
                "message": "你好",
                "shortCode": "88*********50fe",
                "sendStatus": 2,
            },
        }),
        template='json',
        channel='mail',
    )
    push_msg(params)
