import os
import re

import typing

from notifier import issue, pr
from notifier.telegram import Telegram
from notifier.github import Github
from notifier.entity import Event, Issue, PullRequest

MAX_TG_MESSAGE_LENGTH: typing.Final = 4096


class Handler(typing.Protocol):
    def send(
        self,
        html_template: str,
        md_template: str,
        github: Github,
        telegram: Telegram,
        limit: int,
    ) -> None: ...


def get_event_type(url: str) -> tuple[type[Event], Handler]:
    issue_pattern = (
        r"https://(?:api\.)?github\.com/repos/[\w\-\.]+/[\w\-\.]+/issues/\d+"
    )

    pr_pattern = r"https://(?:api\.)?github\.com/repos/[\w\-\.]+/[\w\-\.]+/pulls/\d+"

    if re.match(issue_pattern, url):
        return Issue, issue
    elif re.match(pr_pattern, url):
        return PullRequest, pr
    else:
        raise ValueError(f"Unknown event type for URL: {url}")


if __name__ == "__main__":
    html_template = os.environ.get("HTML_TEMPLATE", "").strip()
    md_template = os.environ.get("MD_TEMPLATE", "").strip()
    telegram_client = Telegram(
        chat_id=os.environ["TELEGRAM_CHAT_ID"],
        bot_token=os.environ["TELEGRAM_BOT_TOKEN"],
        attempt_count=int(os.environ["ATTEMPT_COUNT"]),
        message_thread_id=os.environ.get("TELEGRAM_MESSAGE_THREAD_ID"),
    )

    event_url = os.environ["EVENT_URL"]

    event_type, handler = get_event_type(os.environ["EVENT_URL"])

    github_client = Github(
        event_url=event_url,
        token=(os.environ.get("GITHUB_TOKEN") or "").strip(),
        event_type=event_type,
    )

    handler.send(
        html_template=md_template,
        md_template=md_template,
        github=github_client,
        telegram=telegram_client,
        limit=MAX_TG_MESSAGE_LENGTH,
    )
