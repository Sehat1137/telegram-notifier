from notifier.github import Github
from notifier.telegram import Telegram

import md2tgmd


class MD:
    def __init__(
        self, template: str, github: Github, telegram: Telegram, limit: int
    ) -> None:
        self._template = template
        self._github = github
        self._telegram = telegram
        self._limit = limit

    def send_message(self) -> bool:
        md_message = self._build_message()

        payload = {
            "text": md_message,
            "disable_web_page_preview": True,
            "parse_mode": "MarkdownV2",
        }

        return self._telegram.send_message(payload)

    def _build_message(self) -> str:
        issue = self._github.get_md_issue()

        if len(issue.body) > self._limit:
            issue.body = ""
        else:
            issue.body += "\n"

        labels = ""
        if issue.labels:
            labels = f"\n{' '.join(f'#{label}' for label in issue.labels)}"

        message = self._template.format(
            id=issue.id,
            user=issue.user,
            title=issue.title,
            labels=labels,
            url=issue.url,
            body=issue.body,
            promo="[sent via telegram-notifier](https://github.com/Sehat1137/telegram-notifier)",
        )
        return md2tgmd.escape(message)
