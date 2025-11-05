import dataclasses

import bs4


@dataclasses.dataclass(frozen=True, kw_only=True)
class RenderService:
    custom_labels: list[str]
    join_input_with_list: bool

    def format_body(self, body: str) -> str:
        if not body:
            return body

        soup = bs4.BeautifulSoup(body)

        if self.join_input_with_list:
            for ul in soup.find_all("ul"):
                if ul.find("input"):
                    ul.name = "div"
                    for li in ul.find_all("li"):
                        li.name = "div"

        return str(soup)

    def format_labels(self, labels: list[str]):
        return f"{' '.join(f'#{label}' for label in labels + self.custom_labels)}<br/>"
