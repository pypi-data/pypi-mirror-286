import requests
import json


class WechatRobot:
    def __init__(
        self,
        key="",
        userid="",
        msgtype="text",
        qyapi="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=",
    ):
        self.headers = {"Content-Type": "application/json"}
        self.msgtype = msgtype
        self.qyapi = qyapi
        self.key = key
        self.userid = userid
        self.url = f"{self.qyapi}{self.key}"

    def do_post(self, payload):
        try:
            r = requests.post(self.url, data=payload, headers=self.headers)
            if r.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False

    def send_mes(self, mes_info):
        content = {}
        content["msgtype"] = self.msgtype
        msg_type = {"content": mes_info}
        content["text"] = msg_type
        print(content)
        data = json.dumps(content)
        try:
            status = self.do_post(data)
            if status:
                return 0
            else:
                return 1
        except Exception as e:
            return 1

    def send_custom_msg(self, msg, status=None, name=None, number=None):
        base_url = "http://bj.s1f.ren/gzh/sendMsg"
        query_params = {"userid": self.userid, "text": msg}

        if status is not None:
            query_params["status"] = status
        if name is not None:
            query_params["name"] = name
        if number is not None:
            query_params["number"] = number

        response = requests.get(base_url, params=query_params)

        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")
