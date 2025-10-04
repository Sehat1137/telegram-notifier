import abc
import typing
import traceback

import sulguk
import md2tgmd

from notifier.github import Github
from notifier.telegram import Telegram


class BaseSender(abc.ABC):
    def __init__(
        self,
        template: str,
        github: Github,
        telegram: Telegram,
        limit: int,
    ) -> None:
        self._template = template
        self._github = github
        self._telegram = telegram
        self._limit = limit

    @abc.abstractmethod
    def _create_message(self, event: typing.Any, body: str, labels: str) -> str: ...


class BaseHTMLSender(BaseSender):
    def send_message(self) -> bool:
        try:
            html_message = self._build_message()
            for e in html_message.entities:
                e.pop("language", None)

            payload = {
                "text": html_message.text,
                "entities": html_message.entities,
                "disable_web_page_preview": True,
            }
            return self._telegram.send_message(payload)
        except Exception:
            traceback.print_exc()
            return False

    def _build_message(self) -> sulguk.RenderResult:
        event = self._github.get_html_event()

        labels = ""
        if event.labels:
            labels = f"{' '.join(f'#{label}' for label in event.labels)}<br/>"

        message = self._create_message(event, event.body, labels)

        render_result = sulguk.transform_html(
            message,
            base_url="https://github.com",
        )
        if len(render_result.text) <= self._limit:
            return render_result

        message_without_description = self._create_message(event, "<br/>", labels)

        return sulguk.transform_html(
            message_without_description,
            base_url="https://github.com",
        )


class BaseMDSender(BaseSender):
    def send_message(self) -> bool:
        try:
            md_message = self._build_message()

            payload = {
                "text": md_message,
                "disable_web_page_preview": True,
                "parse_mode": "MarkdownV2",
            }

            return self._telegram.send_message(payload)
        except Exception:
            traceback.print_exc()
            return False

    def _build_message(self) -> str:
        event = self._github.get_md_event()

        labels = ""
        if event.labels:
            labels = f"\n{' '.join(f'#{label}' for label in event.labels)}\n"

        message = self._create_message(event, f"{event.body}\n", labels)
        result = md2tgmd.escape(message)
        if len(result) <= self._limit:
            return result

        message_with_body = self._create_message(event, "", labels)
        return md2tgmd.escape(message_with_body)
