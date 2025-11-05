import requests

from notifier.application import interfaces
from notifier.domain.entities import Issue, PullRequest


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
            labels=[label["name"] for label in data["labels"]],
            url=(data["html_url"] or "").strip(),
            user=data["user"]["login"],
            body=(data.get("body_html", "") or "").strip(),
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
            labels=[label["name"] for label in data["labels"]],
            url=data["html_url"],
            user=data["user"]["login"],
            body=(data.get("body_html", "") or "").strip(),
            additions=data["additions"],
            deletions=data["deletions"],
            head_ref=data["head"]["label"],
            base_ref=data["base"]["ref"],
            repository=data["base"]["repo"]["full_name"],
        )
