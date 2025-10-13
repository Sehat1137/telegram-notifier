import sys
import requests
import time


class Telegram:
    def __init__(
        self,
        chat_id: str,
        bot_token: str,
        attempt_count: int,
        message_thread_id: str | int | None,
    ) -> None:
        self._chat_id = chat_id
        self._bot_token = bot_token
        self._attempt_count = attempt_count
        self._message_thread_id = message_thread_id

    def send_message(self, payload: dict) -> bool:
        count = 0
        url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"
        payload["chat_id"] = self._chat_id
        if self._message_thread_id is not None:
            payload["message_thread_id"] = self._message_thread_id
        while count < self._attempt_count:
            response = requests.post(url, json=payload, timeout=30, verify=False)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print(response.content, file=sys.stderr)
                count += 1
                time.sleep(count * 2)
            else:
                print(response.json())
                return True

        return False
