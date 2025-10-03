import typing
import os
from notifier.telegram import Telegram
from notifier.github import Github
from notifier import issue

# Maximum length of a message in Telegram - 512 bytes for metadata
MAX_TG_MESSAGE_LENGTH: typing.Final = 4096 - 512


if __name__ == "__main__":
    html_template = os.environ.get("HTML_TEMPLATE", "").strip()
    md_template = os.environ.get("MD_TEMPLATE", "").strip()
    telegram_client = Telegram(
        chat_id=os.environ["TELEGRAM_CHAT_ID"],
        bot_token=os.environ["TELEGRAM_BOT_TOKEN"],
        attempt_count=int(os.environ["ATTEMPT_COUNT"]),
        message_thread_id=os.environ.get("TELEGRAM_MESSAGE_THREAD_ID"),
    )
    github_client = Github(
        url=os.environ["ISSUE_URL"],
        token=os.environ["GITHUB_TOKEN"],
    )

    issue.send(
        html_template=md_template,
        md_template=md_template,
        telegram=telegram_client,
        github=github_client,
        limit=MAX_TG_MESSAGE_LENGTH,
    )
