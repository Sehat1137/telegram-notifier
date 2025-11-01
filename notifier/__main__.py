import os
import re
import sys

from notifier.application.interactors import SendIssue, SendPR
from notifier.application.services import RenderService
from notifier.infrastructure.github_gateway import GithubGateway
from notifier.infrastructure.telegram_gateway import TelegramGateway


def get_interactor(url: str) -> type[SendIssue] | type[SendPR]:
    issue_pattern = (
        r"https://(?:api\.)?github\.com/repos/[\w\-\.]+/[\w\-\.]+/issues/\d+"
    )

    pr_pattern = r"https://(?:api\.)?github\.com/repos/[\w\-\.]+/[\w\-\.]+/pulls/\d+"

    if re.match(issue_pattern, url):
        return SendIssue
    elif re.match(pr_pattern, url):
        return SendPR
    else:
        raise ValueError(f"Unknown event type for URL: {url}")


if __name__ == "__main__":
    html_template = os.environ.get("HTML_TEMPLATE", "").strip()

    telegram_gateway = TelegramGateway(
        chat_id=os.environ["TELEGRAM_CHAT_ID"],
        bot_token=os.environ["TELEGRAM_BOT_TOKEN"],
        attempt_count=int(os.environ["ATTEMPT_COUNT"]),
        message_thread_id=os.environ.get("TELEGRAM_MESSAGE_THREAD_ID"),
    )

    event_url = os.environ["EVENT_URL"]

    github_gateway = GithubGateway(
        token=(os.environ.get("GITHUB_TOKEN") or "").strip(),
        event_url=event_url,
    )

    custom_labels = os.environ.get("CUSTOM_LABELS", "").split(",")
    if custom_labels == [""]:
        custom_labels = []

    render_service = RenderService(
        custom_labels=custom_labels,
        join_input_with_list=os.environ.get("JOIN_INPUT_WITH_LIST") == "1",
    )

    interactor = get_interactor(event_url)(
        template=html_template,
        github=github_gateway,
        telegram=telegram_gateway,
        render_service=render_service,
    )

    try:
        interactor.handler()
    except Exception as e:
        print(f"Error processing event: {e}", file=sys.stderr)
        sys.exit(1)
