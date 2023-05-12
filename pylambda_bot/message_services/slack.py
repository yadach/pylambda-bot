import json
import logging
import os

import requests

from pylambda_bot.message_services.base import BaseMessageService
from pylambda_bot.message_services.base import MsgSrvRetryError

logger = logging.getLogger(__name__)


class Slack(BaseMessageService):
    def __init__(self) -> None:
        self.channel = None
        self.ts = None
        self.thread_ts = None
        self.headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": f"Bearer {os.environ.get('BotUserOAuthToken')}",
        }
        self.bot_user_id = ""

    def parse_event(self, event: dict):
        logger.debug(f"Received event: {json.dumps(event)}")
        body = json.loads(event["body"])

        # Avoid retries from slack
        if "x-slack-retry-num" in event["headers"].keys():
            slack_retry_num = event["headers"]["x-slack-retry-num"]
            reason = event["headers"]["x-slack-retry-reason"]
            error_msg = (
                f"Slack retry occurred. x-slack-retry-num: {slack_retry_num}, "
                f"x-slack-retry-reason: {reason}"
            )
            logger.error(error_msg)
            raise MsgSrvRetryError(f"{error_msg}")

        # parse info
        self.channel = body["event"]["channel"]
        self.ts = body["event"]["ts"]
        self.bot_user_id = body["authorizations"][0]["user_id"]
        logger.debug(
            f"[From Slack] bot_user_id: {self.bot_user_id}, channel: {self.channel}, ts: {self.ts}"
        )
        # Prepare text
        input_text = body["event"]["text"]
        input_text = input_text.replace(f"<@{self.bot_user_id}>", "")
        return input_text

    def gen_res(self, body: str):
        res = {
            "statusCode": "200",
            "body": json.dumps(body, ensure_ascii=False),
            "headers": {
                "Content-Type": "application/json",
            },
        }
        return res

    def get_conv_hist(self):
        url = "https://slack.com/api/conversations.replies"
        params = {
            "channel": self.channel,
            "ts": self.ts,
        }
        res = requests.get(url, headers=self.headers, params=params)
        conv_hist = []
        # get thread timestamp
        if "thread_ts" in res.json()["messages"][0].keys():
            self.thread_ts = res.json()["messages"][0]["thread_ts"]
            params["ts"] = self.thread_ts
            res = requests.get(url, headers=self.headers, params=params)
            for msg in res.json()["messages"][:-1]:
                role = "system" if "bot_id" in msg.keys() else "user"
                _msg = msg["text"].replace(f"<@{self.bot_user_id}>", "")
                conv_hist += [{"role": role, "content": _msg}]
        return conv_hist

    def post(self, message: str = None, in_thread: bool = True) -> requests.models.Response:
        assert type(self.channel) == str
        url = "https://slack.com/api/chat.postMessage"

        payload = {
            "text": message,
            "token": os.environ.get("PostToken"),
            "channel": self.channel,
        }
        if in_thread:
            assert type(self.ts) == str
            payload["thread_ts"] = self.ts

        logger.debug(f"[To Slack] headers: {json.dumps(self.headers)}, data: {json.dumps(payload)}")
        res = requests.post(url, data=json.dumps(payload).encode("utf-8"), headers=self.headers)
        logger.debug(f"[From Slack] status: {res.status_code}, content: {res.content}")
        return res

    def delete(self, target_info: requests.models.Response) -> requests.models.Response:
        """Delete message.

        Args:
            target_info (requests.models.Response): target message information

        Returns:
            requests.models.Response: response
        """
        target_dict = target_info.json()
        url = "https://slack.com/api/chat.delete"
        payload = {
            "token": os.environ.get("PostToken"),
            "channel": target_dict["channel"],
            "ts": target_dict["ts"],
        }
        logger.debug(f"[To Slack] headers: {json.dumps(self.headers)}, data: {json.dumps(payload)}")
        res = requests.post(url, data=json.dumps(payload).encode("utf-8"), headers=self.headers)
        logger.debug(f"[From Slack] status: {res.status_code}, content: {res.content}")
        return res
