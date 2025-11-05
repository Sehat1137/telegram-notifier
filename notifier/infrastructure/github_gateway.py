import re
import sys

import requests
import sulguk

from notifier.application import interfaces
from notifier.domain.entities import Issue, PullRequest


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


class GithubGateway(interfaces.Github):
    def __init__(self, token: str, event_url: str) -> None:
        self._token = token
        self._url = event_url

    def get_issue(self) -> Issue:
        headers = {
            "Accept": "application/vnd.github.v3.html+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self._token}",
        }

        response = requests.get(self._url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        return Issue(
            id=data["number"],
            title=data["title"],
            labels=[
                parse_label(label["name"])
                for label in data["labels"]
                if parse_label(label["name"])
            ],
            url=(data["html_url"] or "").strip(),
            user=data["user"]["login"],
            body=self._get_body(data),
        )

    def get_pull_request(self) -> PullRequest:
        headers = {
            "Accept": "application/vnd.github.v3.html+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self._token}",
        }

        response = requests.get(self._url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        return PullRequest(
            id=data["number"],
            title=data["title"],
            labels=[
                parse_label(label["name"])
                for label in data["labels"]
                if parse_label(label["name"])
            ],
            url=data["html_url"],
            user=data["user"]["login"],
            body=self._get_body(data),
            additions=data["additions"],
            deletions=data["deletions"],
            head_ref=data["head"]["label"],
            base_ref=data["base"]["ref"],
            repository=data["base"]["repo"]["full_name"],
        )

    def _get_body(self, data: dict) -> str:
        body = (data.get("body_html", "") or "").strip()
        print(body)

        try:
            sulguk.transform_html(body, base_url="https://github.com")
            return body
        except Exception as e:
            print(f"Error transforming HTML: {e}", file=sys.stderr)
            return "<p></p>"
