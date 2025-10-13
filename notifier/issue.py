import sys
import typing

from notifier.telegram import Telegram
from notifier.github import Github
from notifier.entity import Issue
from notifier.base import BaseMDSender, BaseHTMLSender, RenderConfig


HTML_TEMPLATE: typing.Final = (
    "🚀 <b>New issue to <a href=/{repository}>{repository}</a> by <a href=/{user}>@{user}</a> </b><br/>"
    "📝 <b>{title}</b> (<a href='{url}'>#{id}</a>)<br/>"
    "{body}"
    "{labels}<br/>"
    "{promo}"
)
MD_TEMPLATE: typing.Final = (
    "🚀 **New issue to [{repository}](https://github.com/{repository}) by [@{user}](https://github.com/{user})**\n"
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
            body=self._format_body(body),
            repository=event.repository,
            promo="<a href='/reagento/relator'>sent via relator</a>",
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
            promo="[sent via relator](https://github.com/reagento/relator)",
        )


def send(
    *,
    html_template: str,
    md_template: str,
    github: Github,
    telegram: Telegram,
    render_config: RenderConfig,
) -> None:
    html = IssueHTMLSender(
        html_template or HTML_TEMPLATE, github, telegram, render_config
    )

    if html.send_message():
        sys.exit(0)

    md = IssueMDSender(md_template or MD_TEMPLATE, github, telegram, render_config)

    if md.send_message():
        sys.exit(0)

    sys.exit(1)
