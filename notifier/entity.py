import dataclasses
import re
import typing


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


@dataclasses.dataclass(kw_only=True)
class Issue:
    id: int
    title: str
    labels: typing.Collection[str]
    url: str
    user: str
    body: str
