import dataclasses
import os
import re
import sys
import time
import traceback
from pprint import pprint

import requests
import sulguk


@dataclasses.dataclass(kw_only=True)
class Issue:
    title: str
    labels: list[str]
    link: str
    user: str
    body: str


HTML_TEMPLATE = (
    "🚀 <b>New issue created by {user}</b><br/><br/>"
    "📌 <b>Title:</b> {title}<br/><br/>"
    "🏷️ <b>Tags:</b> {labels}<br/><br/>"
    "🔗 <b>Link:</b> {link}<br/><br/>"
    "📝 <b>Description:</b><br/><br/>{body}"
)

MD_TEMPLATE = (
    "🚀 New issue created by {user}\n\n"
    "📌 Title: {title}\n\n"
    "🏷️ Tags: {labels}\n\n"
    "🔗 Link: {link}\n\n"
    "📝 Description:\n\n{body}"
)

MAGIC_SIZE_OF_TITLE = 512
MAX_TG_MESSAGE_LENGTH = 4096


def truncate_to_telegram_limit(body: str) -> str:
    if len(body) > MAX_TG_MESSAGE_LENGTH - MAGIC_SIZE_OF_TITLE:
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
        labels=[label["name"] for label in issue_data["labels"]],
        link=issue_data["html_url"],
        user=issue_data["user"]["login"],
        body=issue_data["body_html"],
    )


def build_html_message(issue: Issue, template: str) -> str:
    labels = []
    for raw_label in issue.labels:
        parsed_label = raw_label.lower().replace(" ", "_").replace("-", "_")
        parsed_label = re.sub(r"[^a-zA-Z0-9_]", "", parsed_label)
        labels.append(f"#{parsed_label}")
    message = template.format(
        user=issue.user,
        title=issue.title,
        labels=" ".join(labels),
        link=issue.link,
        body=truncate_to_telegram_limit(issue.body),
    )
    return message


def build_markdown_message(issue: Issue, template: str) -> str:
    labels = []
    for raw_label in issue.labels:
        parsed_label = raw_label.lower().replace(" ", "_").replace("-", "_")
        parsed_label = re.sub(r"[^a-zA-Z0-9_]", "", parsed_label)
        labels.append(f"#{parsed_label}")

    message = template.format(
        user=issue.user,
        title=issue.title,
        labels=" ".join(labels),
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
        labels=[label["name"] for label in issue_data["labels"]],
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


if __name__ == "__main__":
    ATTEMPT_COUNT = int(os.environ["ATTEMPT_COUNT"])
    GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
    ISSUE_URL = os.environ["ISSUE_URL"]
    TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])
    HTML_TEMPLATE = os.environ.get("HTML_TEMPLATE", HTML_TEMPLATE)
    MD_TEMPLATE = os.environ.get("MD_TEMPLATE", MD_TEMPLATE)

    html_issue = get_issue_html(ISSUE_URL, GITHUB_TOKEN)
    html_message = sulguk.transform_html(
        build_html_message(html_issue, HTML_TEMPLATE), base_url="https://github.com"
    )
    for e in html_message.entities:
        e.pop("language", None)

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": html_message.text,
        "entities": html_message.entities,
        "disable_web_page_preview": True,
    }

    result = send_message_to_telegram(TELEGRAM_BOT_TOKEN, payload, ATTEMPT_COUNT)
    if result:
        sys.exit(0)

    md_issue = get_issue_markdown(ISSUE_URL, GITHUB_TOKEN)
    md_message = build_markdown_message(md_issue, MD_TEMPLATE)

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": md_message,
        "disable_web_page_preview": True,
    }
    result = send_message_to_telegram(TELEGRAM_BOT_TOKEN, payload, ATTEMPT_COUNT)
    if result:
        sys.exit(0)

    sys.exit(1)
