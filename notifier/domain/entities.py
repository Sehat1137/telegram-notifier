import dataclasses


@dataclasses.dataclass(kw_only=True)
class Issue:
    id: int
    title: str
    labels: list[str]
    url: str
    user: str
    body: str

    @property
    def repository(self) -> str:
        return f"{self.url.split('/')[3]}/{self.url.split('/')[4]}"


@dataclasses.dataclass(kw_only=True)
class PullRequest:
    id: int
    title: str
    labels: list[str]
    url: str
    user: str
    body: str
    additions: int
    deletions: int
    head_ref: str
    base_ref: str
    repository: str
