import sys
import typing

from notifier.telegram import Telegram
from notifier.github import Github
from notifier.entity import Issue
from notifier.base import BaseMDSender, BaseHTMLSender


HTML_TEMPLATE: typing.Final = (
    "🚀 <b>New issue by <a href=/{user}>@{user}</a> </b><br/>"
    "📝 <b>{title}</b> (<a href='{url}'>#{id}</a>)<br/>"
    "{body}"
    "{labels}<br/>"
    "{promo}"
)
MD_TEMPLATE: typing.Final = (
    "🚀 **New issue by [@{user}](https://github.com/{user})**\n"
    "📝 **{title}** ([#{id}]({url}))\n\n"
    "{body}"
    "{labels}\n"
    "{promo}"
)


class IssueHTMLSender(BaseHTMLSender):
    def _create_message(self, event: Issue, body: str, labels: str) -> str:
        return self._template.format(
            id=event.id,
            user=event.user,
            title=event.title,
            labels=labels,
            url=event.url,
            body=body,
            promo="<a href='/Sehat1137/telegram-notifier'>sent via telegram-notifier</a>",
        )


class IssueMDSender(BaseMDSender):
    def _create_message(self, event: Issue, body: str, labels: str) -> str:
        return self._template.format(
            id=event.id,
            user=event.user,
            title=event.title,
            labels=labels,
            url=event.url,
            body=body,
            promo="[sent via telegram-notifier](https://github.com/Sehat1137/telegram-notifier)",
        )


def send(
    html_template: str,
    md_template: str,
    github: Github,
    telegram: Telegram,
    limit: int,
) -> None:
    html = IssueHTMLSender(html_template or HTML_TEMPLATE, github, telegram, limit)

    if html.send_message():
        sys.exit(0)

    md = IssueMDSender(md_template or MD_TEMPLATE, github, telegram, limit)

    if md.send_message():
        sys.exit(0)

    sys.exit(1)
