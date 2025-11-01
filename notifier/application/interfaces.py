import abc
import typing

import sulguk

from notifier.domain.entities import PullRequest, Issue


class Github(typing.Protocol):
    @abc.abstractmethod
    def get_issue(self) -> Issue: ...

    @abc.abstractmethod
    def get_pull_request(self) -> PullRequest: ...


class Telegram(typing.Protocol):
    @abc.abstractmethod
    def send_message(self, render_result: sulguk.RenderResult) -> None: ...
