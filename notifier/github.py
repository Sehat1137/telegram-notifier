import requests
from notifier.entity import Issue, parse_label


class Github:
    def __init__(self, token: str, url: str) -> None:
        self._token = token
        self._url = url

    def get_html_issue(self) -> Issue:
        headers = {
            "Accept": "application/vnd.github.html+json",
            "Authorization": f"Bearer {self._token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

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
            body=issue_data["body_html"].strip(),
        )

    def get_md_issue(self) -> Issue:
        headers = {
            "Accept": "application/vnd.github.v3.raw+json",
            "Authorization": f"Bearer {self._token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
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
            body=issue_data["body"].strip(),
        )
