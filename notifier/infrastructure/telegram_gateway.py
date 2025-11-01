import sys
import time

import requests
import sulguk

from notifier.application import interfaces


class TelegramGateway(interfaces.Telegram):
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

    def send_message(self, render_result: sulguk.RenderResult) -> None:
        count = 0
        payload = self._create_payload(render_result)
        url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"
        while count < self._attempt_count:
            response = requests.post(url, json=payload, timeout=30)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print(response.content, file=sys.stderr)
                count += 1
                time.sleep(count * 2)
            else:
                print(response.json(), file=sys.stdout)
                return

    def _create_payload(self, render_result: sulguk.RenderResult) -> dict:
        for e in render_result.entities:
            e.pop("language", None)

        payload = {
            "text": render_result.text,
            "entities": render_result.entities,
            "disable_web_page_preview": True,
        }
        payload["chat_id"] = self._chat_id

        if self._message_thread_id is not None:
            payload["message_thread_id"] = self._message_thread_id

        return payload
