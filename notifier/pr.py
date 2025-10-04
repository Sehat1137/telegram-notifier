import sys
import typing

from notifier.entity import PullRequest
from notifier.base import BaseMDSender, BaseHTMLSender
from notifier.github import Github
from notifier.telegram import Telegram


HTML_TEMPLATE: typing.Final = (
    "🎉 <b>New Pull Request to <a href=/{repository}>{repository}</a> by <a href=/{user}>@{user}</a></b><br/>"
    "✨ <b>{title}</b> (<a href='{url}'>#{id}</a>)<br/>"
    "📊 +{additions}/-{deletions}<br/>"
    "🌿 {head_ref} → {base_ref}<br/>"
    "{body}"
    "{labels}"
    "{promo}"
)

MD_TEMPLATE: typing.Final = (
    "🎉 **New Pull Request to [{repository}](https://github.com/{repository}) "
    "by [@{user}](https://github.com/{user})]**\n"
    "✨ **{title}** ([#{id}]({url}))\n"
    "📊 +{additions}/-{deletions}\n"
    "🌿 {head_ref} → {base_ref}\n\n"
    "{body}"
    "{labels}"
    "{promo}"
)


class PRHTMLSender(BaseHTMLSender):
    def _create_message(self, event: PullRequest, body: str, labels: str) -> str:
        return self._template.format(
            id=event.id,
            user=event.user,
            title=event.title,
            labels=labels,
            url=event.url,
            body=body,
            additions=event.additions,
            deletions=event.deletions,
            head_ref=event.head_ref,
            base_ref=event.base_ref,
            repository=event.repository,
            promo="<a href='/Sehat1137/telegram-notifier'>sent via telegram-notifier</a>",
        )


class PRMDSender(BaseMDSender):
    def _create_message(self, event: PullRequest, body: str, labels: str) -> str:
        return self._template.format(
            id=event.id,
            user=event.user,
            title=event.title,
            labels=labels,
            url=event.url,
            body=body,
            additions=event.additions,
            deletions=event.deletions,
            head_ref=event.head_ref,
            base_ref=event.base_ref,
            repository=event.repository,
            promo="[sent via telegram-notifier](https://github.com/Sehat1137/telegram-notifier)",
        )


def send(
    html_template: str,
    md_template: str,
    github: Github,
    telegram: Telegram,
    limit: int,
) -> None:
    html = PRHTMLSender(html_template or HTML_TEMPLATE, github, telegram, limit)

    if html.send_message():
        sys.exit(0)

    md = PRMDSender(md_template or MD_TEMPLATE, github, telegram, limit)

    if md.send_message():
        sys.exit(0)

    sys.exit(1)
