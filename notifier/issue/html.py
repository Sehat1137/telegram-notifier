import sulguk

from notifier.github import Github
from notifier.telegram import Telegram
from notifier.entity import Issue


class HTML:
    def __init__(
        self, template: str, github: Github, telegram: Telegram, limit: int
    ) -> None:
        self._template = template
        self._github = github
        self._telegram = telegram
        self._limit = limit

    def send_message(self) -> bool:
        html_message = self._build_message()
        for e in html_message.entities:
            e.pop("language", None)

        payload = {
            "text": html_message.text,
            "entities": html_message.entities,
            "disable_web_page_preview": True,
        }
        return self._telegram.send_message(payload)

    def _build_message(self) -> sulguk.RenderResult:
        issue = self._github.get_html_issue()

        labels = ""
        if issue.labels:
            labels = f"{' '.join(f'#{label}' for label in issue.labels)}"

        message = self._create_message(issue, issue.body, labels)
        render_result = sulguk.transform_html(
            message,
            base_url="https://github.com",
        )
        if len(render_result.text) <= self._limit:
            return render_result

        message_without_description = self._create_message(issue, "<br/>", labels)

        return sulguk.transform_html(
            message_without_description,
            base_url="https://github.com",
        )

    def _create_message(self, issue: Issue, body: str, labels: str) -> str:
        return self._template.format(
            id=issue.id,
            user=issue.user,
            title=issue.title,
            labels=labels,
            url=issue.url,
            body=body,
            promo="<a href='/Sehat1137/telegram-notifier'>sent via telegram-notifier</a>",
        )
