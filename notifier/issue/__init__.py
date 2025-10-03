import sys
import typing
from notifier.issue.md import MD
from notifier.issue.html import HTML
from notifier.telegram import Telegram
from notifier.github import Github

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


def send(
    html_template: str,
    md_template: str,
    github: Github,
    telegram: Telegram,
    limit: int,
) -> None:
    html = HTML(html_template or HTML_TEMPLATE, github, telegram, limit)

    if html.send_message():
        sys.exit(0)

    md = MD(md_template or MD_TEMPLATE, github, telegram, limit)

    if md.send_message():
        sys.exit(0)

    sys.exit(1)


__all__ = ("send",)
