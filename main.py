import dataclasses
import os
import re
import sys
import time
import traceback
from pprint import pprint
import typing

import requests
import sulguk


@dataclasses.dataclass(kw_only=True)
class Issue:
    title: str
    labels: set[str]
    link: str
    user: str
    body: str


@dataclasses.dataclass(kw_only=True)
class TelegramConfig:
    chat_id: str
    bot_token: str
    attempt_count: int
    message_thread_id: str | int | None


MAGIC_SIZE_OF_META: typing.Final = 512
MAX_TG_MESSAGE_LENGTH: typing.Final = 4096


def parse_label(raw_label: str) -> str:
    """
    Bug Report -> bug_report
    high-priority -> high_priority
    Feature Request!!! -> feature_request
    Version 2.0 -> version_20
    Critical Bug - Urgent!!! -> critical_bug___urgent
    Багрепорт - ...
    already_normalized -> already_normalized
    Test@#$%^&*()Label -> testlabel
    ... -> ...
    """
    parsed_label = raw_label.lower().replace(" ", "_").replace("-", "_")
    return re.sub(r"[^a-zA-Z0-9_]", "", parsed_label)


def truncate_to_telegram_limit(body: str) -> str:
    if len(body) > MAX_TG_MESSAGE_LENGTH - MAGIC_SIZE_OF_META:
        return "Description too long, please see details inside the issue..."
    return body


def get_issue_html(issue_url: str, github_token: str) -> Issue:
    headers = {
        "Accept": "application/vnd.github.html+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(issue_url, headers=headers, timeout=30)
    response.raise_for_status()

    issue_data = response.json()
    return Issue(
        title=issue_data["title"],
        labels={
            parse_label(label["name"])
            for label in issue_data["labels"]
            if parse_label(label["name"])
        },
        link=issue_data["html_url"],
        user=issue_data["user"]["login"],
        body=issue_data["body_html"],
    )


def build_html_message(issue: Issue, template: str) -> sulguk.RenderResult:
    message = template.format(
        user=issue.user,
        title=issue.title,
        labels=" ".join(f"#{label}" for label in issue.labels),
        link=issue.link,
        body=truncate_to_telegram_limit(issue.body),
    )
    return sulguk.transform_html(message, base_url="https://github.com")


def build_markdown_message(issue: Issue, template: str) -> str:
    body = truncate_to_telegram_limit(issue.body)
    body = re.sub(r'[^\w\sа-яА-ЯёЁ.,!?;:()\-+=\*@#%&$/"\'<>\[\]{}`~|\\]', "", body)

    message = template.format(
        user=issue.user,
        title=issue.title,
        labels=" ".join(f"#{label}" for label in issue.labels),
        link=issue.link,
        body=truncate_to_telegram_limit(issue.body),
    )
    return message


def get_issue_markdown(issue_url: str, github_token: str) -> Issue:
    headers = {
        "Accept": "application/vnd.github.v3.raw+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(issue_url, headers=headers, timeout=30)
    response.raise_for_status()

    issue_data = response.json()

    return Issue(
        title=issue_data["title"],
        labels={
            parse_label(label["name"])
            for label in issue_data["labels"]
            if parse_label(label["name"])
        },
        link=issue_data["html_url"],
        user=issue_data["user"]["login"],
        body=issue_data["body"],
    )


def send_message_to_telegram(
    tg_bot_token: str, payload: dict, attempt_count: int
) -> bool:
    count = 0
    url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
    while count < attempt_count:
        try:
            response = requests.post(url, json=payload, timeout=30)
            pprint(response.json())
            response.raise_for_status()
            return True
        except Exception:
            count += 1
            traceback.print_exc()
            time.sleep(count * 2)

    return False


def send_html_message(html_issue: Issue, template: str, tg: TelegramConfig) -> bool:
    try:
        html_message = build_html_message(html_issue, template)
        for e in html_message.entities:
            e.pop("language", None)

        payload = {
            "chat_id": tg.chat_id,
            "text": html_message.text,
            "entities": html_message.entities,
            "disable_web_page_preview": True,
        }
        if tg.message_thread_id:
            payload["message_thread_id"] = tg.message_thread_id

        return send_message_to_telegram(tg.bot_token, payload, tg.attempt_count)
    except Exception:
        traceback.print_exc()
        return False


def send_md_message(md_issue: Issue, template: str, tg: TelegramConfig) -> bool:
    md_message = build_markdown_message(md_issue, template)

    payload = {
        "chat_id": tg.chat_id,
        "text": md_message,
        "disable_web_page_preview": True,
    }
    if tg.message_thread_id:
        payload["message_thread_id"] = tg.message_thread_id
    return send_message_to_telegram(tg.bot_token, payload, tg.attempt_count)


if __name__ == "__main__":
    TELEGRAM_CONFIG: typing.Final = TelegramConfig(
        chat_id=os.environ["TELEGRAM_CHAT_ID"],
        bot_token=os.environ["TELEGRAM_BOT_TOKEN"],
        attempt_count=int(os.environ["ATTEMPT_COUNT"]),
        message_thread_id=os.environ.get("TELEGRAM_MESSAGE_THREAD_ID"),
    )
    GITHUB_TOKEN: typing.Final = os.environ["GITHUB_TOKEN"]
    ISSUE_URL: typing.Final = os.environ["ISSUE_URL"]
    HTML_TEMPLATE: typing.Final = (
        os.environ.get("HTML_TEMPLATE", "").strip()
        or "🚀 <b>New issue created by {user}</b><br/><br/>"
        "📌 <b>Title:</b> {title}<br/><br/>"
        "🏷️ <b>Tags:</b> {labels}<br/><br/>"
        "🔗 <b>Link:</b> {link}<br/><br/>"
        "📝 <b>Description:</b><br/><br/>{body}"
        "<br/><br/><b>sent via</b> https://github.com/Sehat1137/telegram-notifier"
    )
    MD_TEMPLATE: typing.Final = (
        os.environ.get("MD_TEMPLATE", "").strip()
        or "🚀 New issue created by {user}\n\n"
        "📌 Title: {title}\n\n"
        "🏷️ Tags: {labels}\n\n"
        "🔗 Link: {link}\n\n"
        "📝 Description:\n\n{body}"
        "\n\nsent via https://github.com/Sehat1137/telegram-notifier"
    )
    TRIGGER_LABELS: typing.Final = {
        parse_label(raw_label)
        for raw_label in os.environ.get("TRIGGER_LABELS", "").split(";")
        if parse_label(raw_label)
    }

    html_issue = get_issue_html(ISSUE_URL, GITHUB_TOKEN)

    if len(TRIGGER_LABELS) > 0 and not TRIGGER_LABELS & html_issue.labels:
        sys.exit(0)

    if succes := send_html_message(html_issue, HTML_TEMPLATE, TELEGRAM_CONFIG):
        sys.exit(0)

    md_issue = get_issue_markdown(ISSUE_URL, GITHUB_TOKEN)

    if not send_md_message(md_issue, MD_TEMPLATE, TELEGRAM_CONFIG):
        sys.exit(1)
