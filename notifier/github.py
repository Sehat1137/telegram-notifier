import requests
import typing

from notifier.entity import Event, Issue, PullRequest, parse_label


class Github:
    def __init__(self, token: str, event_url: str, event_type: type[Event]) -> None:
        self._event_type = event_type
        self._token = token
        self._url = event_url
        self._html_events: dict[type[Event], typing.Callable[[], Event]] = {
            Issue: self._get_html_issue,
            PullRequest: self._get_html_pr,
        }
        self._md_events: dict[type[Event], typing.Callable[[], Event]] = {
            Issue: self._get_md_issue,
            PullRequest: self._get_md_pr,
        }

    def get_html_event(self) -> Event:
        return self._html_events[self._event_type]()

    def get_md_event(self) -> Event:
        return self._md_events[self._event_type]()

    def _get_html_issue(self) -> Issue:
        headers = self._get_headers({"Accept": "application/vnd.github.v3.html+json"})

        response = requests.get(self._url, headers=headers, timeout=30)
        response.raise_for_status()

        issue_data = response.json()
        return Issue(
            id=issue_data["number"],
            title=issue_data["title"],
            labels={
                parse_label(label["name"])
                for label in issue_data["labels"]
                if parse_label(label["name"])
            },
            url=(issue_data["html_url"] or "").strip(),
            user=issue_data["user"]["login"],
            body=issue_data["body_html"].strip(),
        )

    def _get_html_pr(self) -> PullRequest:
        headers = self._get_headers({"Accept": "application/vnd.github.v3.html+json"})

        response = requests.get(self._url, headers=headers, timeout=30)
        response.raise_for_status()

        pr_data = response.json()
        return PullRequest(
            id=pr_data["number"],
            title=pr_data["title"],
            labels={
                parse_label(label["name"])
                for label in pr_data["labels"]
                if parse_label(label["name"])
            },
            url=pr_data["html_url"],
            user=pr_data["user"]["login"],
            body=(pr_data["body_html"] or "").strip(),
            additions=pr_data["additions"],
            deletions=pr_data["deletions"],
            head_ref=pr_data["head"]["label"],
            base_ref=pr_data["base"]["ref"],
            repository=pr_data["base"]["repo"]["full_name"],
        )

    def _get_md_issue(self) -> Issue:
        headers = self._get_headers({"Accept": "application/vnd.github.v3.raw+json"})

        response = requests.get(self._url, headers=headers, timeout=30)
        response.raise_for_status()

        issue_data = response.json()
        return Issue(
            id=issue_data["number"],
            title=issue_data["title"],
            labels={
                parse_label(label["name"])
                for label in issue_data["labels"]
                if parse_label(label["name"])
            },
            url=issue_data["html_url"],
            user=issue_data["user"]["login"],
            body=(issue_data["body"] or "").strip(),
        )

    def _get_md_pr(self) -> PullRequest:
        headers = self._get_headers({"Accept": "application/vnd.github.v3.raw+json"})

        response = requests.get(self._url, headers=headers, timeout=30)
        response.raise_for_status()

        pr_data = response.json()
        return PullRequest(
            id=pr_data["number"],
            title=pr_data["title"],
            labels={
                parse_label(label["name"])
                for label in pr_data["labels"]
                if parse_label(label["name"])
            },
            url=pr_data["html_url"],
            user=pr_data["user"]["login"],
            body=(pr_data["body"] or "").strip(),
            additions=pr_data["additions"],
            deletions=pr_data["deletions"],
            head_ref=pr_data["head"]["label"],
            base_ref=pr_data["base"]["ref"],
            repository=pr_data["base"]["repo"]["full_name"],
        )

    def _get_headers(self, extra: dict) -> dict:
        headers = {
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return {**headers, **extra}
